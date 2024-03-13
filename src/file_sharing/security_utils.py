import aiofiles

from fastapi import UploadFile
from cryptography.fernet import Fernet
from src.file_sharing.models.security import SecurityDoc
from src.file_sharing.models.file import FileDoc


async def encode_file(filename: str, file: UploadFile) -> tuple[bytes, SecurityDoc]:
    key = Fernet.generate_key()
    fernet = Fernet(key)
    read_file = file.file.read()
    encrypted_data = fernet.encrypt(read_file)
    security_document = SecurityDoc(filename=filename, security_key=key)
    await SecurityDoc.insert_one(document=security_document)
    return encrypted_data, security_document
    
async def decode_file(file_path: str, file_doc: FileDoc) -> None:
    fernet = Fernet(file_doc.security.security_key)
    async with aiofiles.open(file_path, 'rb') as encrypted_file:
        encrypted = await encrypted_file.read()
    decrypted = fernet.decrypt(encrypted)
    async with aiofiles.open(file_path, 'wb') as dec_file:
        await dec_file.write(decrypted)
    return
