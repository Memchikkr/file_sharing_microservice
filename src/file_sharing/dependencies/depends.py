from src.file_sharing.services.base_service import FileServiceBase
from src.file_sharing.services.minio_service import MinioFileService

def minio_service() -> FileServiceBase:
    return MinioFileService()
