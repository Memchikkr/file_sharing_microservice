from fastapi import APIRouter, UploadFile, File, Path
from api_responses import FileApiResponse
from service import FileService

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
    filename: str = Path(..., min_length=1, max_length=500)
):
    service = FileService()
    download_url = await service.download_file(filename=filename)
    return {"download_url": download_url}


@router.delete("/files/{filename}", status_code=204)
async def delete_file(
    filename: str = Path(..., min_length=1, max_length=500)
):
    service = FileService()
    await service.delete_file(filename=filename)
    return
