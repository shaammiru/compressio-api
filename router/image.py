from io import BytesIO
from enum import Enum
from fastapi import APIRouter, Query, File, UploadFile, HTTPException
from service import image, azure_storage, model


class Algorithm(str, Enum):
    jpeg = "jpeg"
    webp = "webp"


router = APIRouter()


@router.post("/compress", response_model=model.CompressResponseModel)
async def compress_image(
    algorithm: Algorithm = Query(...), file: UploadFile = File(...)
):
    try:
        buffer_data = BytesIO(await file.read())

        if algorithm == Algorithm.jpeg:
            output, compress_time = image.compress_image(
                buffer_data, algorithm.value.upper()
            )
        elif algorithm == Algorithm.webp:
            output, compress_time = image.compress_image(
                buffer_data, algorithm.value.upper()
            )

        file_name = f"{file.filename.split('.')[0]}.{algorithm.value.lower()}"
        original_size = f"{file.size / 1024 / 1024:.2f}"
        compressed_size = f"{output.getbuffer().nbytes / 1024 / 1024:.2f}"
        url = azure_storage.upload_blob("image", file_name, output)

        return {
            "data": {
                "type": "Image",
                "algorithm": algorithm.value.upper(),
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
