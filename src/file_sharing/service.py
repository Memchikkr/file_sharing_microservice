from fastapi import UploadFile, HTTPException
from io import BytesIO
from minio.error import S3Error
from minio_storage import client_minio
from files_model import FileModel


class FileService:

    def __init__(self) -> None:
        self.minio = client_minio
        self.bucket_name = 'data'

    async def upload_file(self, file: UploadFile):
        filename = file.filename
        if await FileModel.find_one(FileModel.filename == filename):
            raise HTTPException(status_code=409, detail='File already exist')
        try:
            self.minio.put_object(
                bucket_name=self.bucket_name,
                data=BytesIO(file.file.read()),
                object_name=filename,
                content_type=file.content_type,
                length=-1,
                part_size=10*1024*1024
            )
        except S3Error as exc:
            raise HTTPException(status_code=404, detail=f"Ошибка при загрузке файла: {exc}")
        mongo_model = FileModel(filename=filename, size_bytes=file.size)
        await mongo_model.insert()
        return mongo_model

    async def download_file(self, filename: str):
        await self.__check_file_exist(filename=filename)
        try:
            download_url = self.minio.presigned_get_object(
                bucket_name=self.bucket_name,
                object_name=filename
            )
        except S3Error as exc:
            raise HTTPException(status_code=404, detail=f"Ошибка при получении ссылки для скачивания: {exc}")
        return download_url


    async def delete_file(self, filename: str):
        try:
            self.minio.remove_object(self.bucket_name, object_name=filename)
        except S3Error as exc:
            raise HTTPException(status_code=404, detail=f"Ошибка при удалении файла: {exc}")
        file_model = await self.__check_file_exist(filename=filename)
        await file_model.delete()
        return


    async def __check_file_exist(self, filename: str):
        file_model = await FileModel.find_one(FileModel.filename == filename)
        if not file_model:
            raise HTTPException(status_code=404, detail='Not found')
        return file_model
    