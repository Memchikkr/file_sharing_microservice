from fastapi import APIRouter

router = APIRouter(
    prefix="/home"
)

@router.get("")
async def get():
    return "Hellow world"
