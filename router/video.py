from fastapi import APIRouter
from enum import Enum


class Algorithm(str, Enum):
    avc = "AVC"
    hevc = "HEVC"


router = APIRouter()


@router.get("/compress")
async def compress_image(algorithm: Algorithm):
    return {
        "data": {
            "type": "Video",
            "algorithm": algorithm,
            "url": "TODO (string)",
            "time": "TODO (string)",
        }
    }
