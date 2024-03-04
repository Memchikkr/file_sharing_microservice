from beanie import Document


class FileModel(Document):
    id: int
    name: str

    class Settings:
        name = 'files'
