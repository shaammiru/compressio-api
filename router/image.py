from fastapi import APIRouter
from enum import Enum


class Algorithm(str, Enum):
    jpeg = "JPEG"
    webp = "WEBP"


router = APIRouter()


@router.get("/compress")
async def compress_image(algorithm: Algorithm):
    return {
        "data": {
            "type": "Image",
            "algorithm": algorithm,
            "url": "TODO (string)",
            "time": "TODO (string)",
        }
    }
