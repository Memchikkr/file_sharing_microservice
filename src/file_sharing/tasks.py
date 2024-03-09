import os


async def remove_file(file_path: str) -> None:
    os.unlink(file_path)
