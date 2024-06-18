from fastapi import APIRouter
from enum import Enum


class Algorithm(str, Enum):
    mp3 = "MP3"
    aac = "AAC"


router = APIRouter()


@router.get("/compress")
async def compress_image(algorithm: Algorithm):
    return {
        "data": {
            "type": "Audio",
            "algorithm": algorithm,
            "url": "TODO (string)",
            "time": "TODO (string)",
        }
    }
