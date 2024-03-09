import aiofiles

from fastapi import UploadFile, File
from cryptography.fernet import Fernet
from mongo_models import Security


class SecurityUtils:

    @staticmethod
    async def encode_file(filename: str, file: UploadFile):
        key = Fernet.generate_key()
        fernet = Fernet(key)
        read_file = file.file.read()
        encrypted_data = fernet.encrypt(read_file)
        mongo_model = Security(filename=filename, security_key=key)
        await mongo_model.insert()
        return encrypted_data
    
    @staticmethod
    async def decode_file(file_path: str, filename: str):
        security_doc = await Security.find_one(Security.filename == filename)
        fernet = Fernet(security_doc.security_key)
        async with aiofiles.open(file_path, 'rb') as encrypted_file:
            encrypted = await encrypted_file.read()
            print(len(encrypted))
        decrypted = fernet.decrypt(encrypted)
        async with aiofiles.open(file_path, 'wb') as dec_file:
            await dec_file.write(decrypted)
        await security_doc.delete()
        return
