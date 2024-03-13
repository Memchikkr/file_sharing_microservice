from beanie import Document, Link
from src.file_sharing.models.security import SecurityDoc

class FileDoc(Document):
    filename: str
    size_bytes: int
    security: Link[SecurityDoc]

    class Settings:
        name = 'files'
