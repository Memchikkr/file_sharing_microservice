from fastapi import APIRouter, UploadFile, File, Path, BackgroundTasks, Depends
from fastapi.responses import FileResponse
from src.file_sharing.api_responses import FileApiResponse
from src.file_sharing.services.base_service import FileServiceBase
from src.file_sharing.dependencies.depends import minio_service
from src.file_sharing.tasks import remove_file

router = APIRouter(
    prefix="/files"
)

@router.post("", status_code=201, response_model=FileApiResponse)
async def upload_file(
    file: UploadFile = File(...),
    service: FileServiceBase = Depends(minio_service)
):
    result = await service.upload_file(file=file)
    return result

@router.get("/{filename}")
async def download_file(
    background_task: BackgroundTasks,
    service: FileServiceBase = Depends(minio_service),
    filename: str = Path(..., min_length=1, max_length=500)
):
    file_path, filename = await service.download_file(filename=filename)
    background_task.add_task(remove_file, file_path)
    return FileResponse(path=file_path, filename=filename)


@router.delete("/{filename}", status_code=204)
async def delete_file(
    filename: str = Path(..., min_length=1, max_length=500),
    service: FileServiceBase = Depends(minio_service)
):
    await service.delete_file(filename=filename)
    return
