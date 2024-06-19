from io import BytesIO
from enum import Enum
from fastapi import APIRouter, Query, File, UploadFile, HTTPException
from service import image, azure_storage


class Algorithm(str, Enum):
    jpeg = "jpeg"
    webp = "webp"


router = APIRouter()


@router.post("/compress")
async def compress_image(
    algorithm: Algorithm = Query(...), file: UploadFile = File(...)
):
    try:
        buffer_data = BytesIO(await file.read())

        if algorithm == Algorithm.jpeg:
            media_type = "JPEG"
            output, compress_time = image.compress_image(buffer_data, media_type)
        elif algorithm == Algorithm.webp:
            media_type = "WEBP"
            output, compress_time = image.compress_image(buffer_data, media_type)

        file_name = f"{file.filename.split(".")[0]}.{media_type.lower()}"
        original_size = f"{file.size / 1024 / 1024:.2f}"
        compressed_size = f"{output.getbuffer().nbytes / 1024 / 1024:.2f}"
        url = azure_storage.upload_blob("image", file_name, output)

        return {
            "data": {
                "type": "Image",
                "algorithm": algorithm,
                "url": url,
                "size": {
                    "original": original_size,
                    "compressed": compressed_size,
                },
                "time": compress_time,
            }
        }
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
