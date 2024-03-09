from beanie import Document

class FileModel(Document):
    filename: str
    size_bytes: int

    class Settings:
        name = 'files'


class Security(Document):
    filename: str
    security_key: bytes

    class Settings:
        name = 'security'
