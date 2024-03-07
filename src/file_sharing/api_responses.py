from pydantic import BaseModel


class FileApiResponse(BaseModel):

    filename: str
    size_bytes: int
