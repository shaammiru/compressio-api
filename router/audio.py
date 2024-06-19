from fastapi import APIRouter, Query, File, UploadFile, HTTPException
from enum import Enum
from service import audio, azure_storage


class Algorithm(str, Enum):
    mp3 = "mp3"
    aac = "aac"


router = APIRouter()


@router.get("/compress")
async def compress_image(
    algorithm: Algorithm = Query(...), file: UploadFile = File(...)
):
    try:
        if algorithm == Algorithm.mp3:
            output, time = audio.compress_audio("test.mp3", "output.mp3", "mp3")
        elif algorithm == Algorithm.aac:
            output, time = audio.compress_audio("test.mp3", "output.aac", "aac")

        url = azure_storage.upload_blob("audio", file.filename, output)

        return {
            "data": {
                "type": "Audio",
                "algorithm": algorithm,
                "url": url,
                "time": time,
            }
        }
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
