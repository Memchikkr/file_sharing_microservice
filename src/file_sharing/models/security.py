from beanie import Document

class SecurityDoc(Document):
    filename: str
    security_key: bytes

    class Settings:
        name = 'security'
