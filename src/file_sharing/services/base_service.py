from abc import ABC, abstractmethod
from fastapi import UploadFile
from src.file_sharing.models.file import FileDoc


class FileServiceBase(ABC):

    @abstractmethod
    async def upload_file(
        self, file: UploadFile
    ) -> FileDoc:
        ...

    @abstractmethod
    async def download_file(
        self, filename: str
    ) -> tuple[str, str]:
        ...
        
    @abstractmethod
    async def delete_file(
        self, filename: str
    ) -> str:
        ...
