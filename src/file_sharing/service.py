import uuid

from beanie import DeleteRules
from fastapi import UploadFile, HTTPException
from io import BytesIO
from minio.error import S3Error
from src.minio_storage import client_minio
from src.file_sharing.models.file import FileDoc
from src.file_sharing.security_utils import SecurityUtils


class FileService:

    def __init__(self) -> None:
        self.minio = client_minio
        self.bucket_name = 'data'

    async def upload_file(self, file: UploadFile):
        extension = file.filename.split('.')[1]
        new_filename = f'{uuid.uuid4()}.{extension}'
        file_data, security_document = await SecurityUtils.encode_file(file=file, filename=file.filename)
        try:
            self.minio.put_object(
                bucket_name=self.bucket_name,
                data=BytesIO(file_data),
                object_name=new_filename,
                content_type=file.content_type,
                length=-1,
                part_size=10*1024*1024
            )
        except S3Error as exc:
            raise HTTPException(status_code=400, detail=f"Ошибка при загрузке файла: {exc}")
        file_document = FileDoc(filename=new_filename, size_bytes=file.size, security=security_document)
        await FileDoc.insert_one(document=file_document)
        return file_document

    async def download_file(self, filename: str):
        file_doc = await self.__check_file_exist(filename=filename)
        file_path = 'files/' + f'{filename}'
        try:
            self.minio.fget_object(
                bucket_name=self.bucket_name,
                object_name=filename,
                file_path=file_path
            )
        except S3Error as exc:
            raise HTTPException(status_code=400, detail=f"Ошибка при получении ссылки для скачивания: {exc}")
        orig_filename = await self.delete_file(filename=filename)
        await SecurityUtils.decode_file(file_path=file_path, file_doc=file_doc)
        return file_path, orig_filename


    async def delete_file(self, filename: str):
        try:
            self.minio.remove_object(self.bucket_name, object_name=filename)
        except S3Error as exc:
            raise HTTPException(status_code=400, detail=f"Ошибка при удалении файла: {exc}")
        file_doc = await self.__check_file_exist(filename=filename)
        orig_filename = file_doc.security.filename
        await file_doc.delete(link_rule=DeleteRules.DELETE_LINKS)
        return orig_filename


    async def __check_file_exist(self, filename: str):
        file_doc = await FileDoc.find_one(FileDoc.filename == filename, fetch_links=True)
        if not file_doc:
            raise HTTPException(status_code=404, detail='Not found')
        return file_doc
