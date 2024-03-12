from minio import Minio
from src.config import ProjectConfig


client_minio = Minio(
    ProjectConfig.MINIO_URL,
    access_key=ProjectConfig.MINIO_ROOT_USER,
    secret_key=ProjectConfig.MINIO_ROOT_PASSWORD,
    secure=False
)
