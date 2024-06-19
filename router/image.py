from fastapi import APIRouter, Query, File, UploadFile, HTTPException
from enum import Enum
from service import image, azure_storage


class Algorithm(str, Enum):
    jpeg = "jpeg"
    webp = "webp"


router = APIRouter()


@router.get("/compress")
async def compress_image(
    algorithm: Algorithm = Query(...), file: UploadFile = File(...)
):
    try:
        if algorithm == Algorithm.jpeg:
            output, compress_time = image.compress_image("test.mp3", "JPEG")
        elif algorithm == Algorithm.webp:
            output, compress_time = image.compress_image("test.mp3", "WEBP")

        url = azure_storage.upload_blob("image", file.filename, output)

        return {
            "data": {
                "type": "Image",
                "algorithm": algorithm,
                "url": url,
                "time": compress_time,
            }
        }
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
