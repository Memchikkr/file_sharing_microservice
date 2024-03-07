from beanie import Document

class FileModel(Document):
    filename: str
    size_bytes: int

    class Settings:
        name = 'files'
