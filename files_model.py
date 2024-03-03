from beanie import Document


class FileModel(Document):
    id: int
    name: str
    extesnion: str
