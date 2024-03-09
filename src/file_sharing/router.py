from fastapi import APIRouter, UploadFile, File, Path, BackgroundTasks
from fastapi.responses import FileResponse
from api_responses import FileApiResponse
from service import FileService
from tasks import remove_file

router = APIRouter(
    prefix="/home"
)

@router.post("/upload/files", status_code=201, response_model=FileApiResponse)
async def upload_file(
    file: UploadFile = File(...)
):
    service = FileService()
    result = await service.upload_file(file=file)
    return result

@router.get("/download/files/{filename}")
async def download_file(
    background_task: BackgroundTasks,
    filename: str = Path(..., min_length=1, max_length=500)
):
    service = FileService()
    file_path = await service.download_file(filename=filename)
    background_task.add_task(remove_file, file_path)
    return FileResponse(path=file_path, filename=filename)


@router.delete("/files/{filename}", status_code=204)
async def delete_file(
    filename: str = Path(..., min_length=1, max_length=500)
):
    service = FileService()
    await service.delete_file(filename=filename)
    return
