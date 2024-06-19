import os
import uuid
from enum import Enum
from fastapi import APIRouter, Query, File, UploadFile, HTTPException
from service import video, azure_storage, model


class Algorithm(str, Enum):
    avc = "avc"
    hevc = "hevc"


router = APIRouter()


@router.post("/compress", response_model=model.CompressResponseModel)
async def compress_image(
    algorithm: Algorithm = Query(...), file: UploadFile = File(...)
):
    input_path = os.path.join("tmp", f"{uuid.uuid4()}-{file.filename}")
    output_path = os.path.join("tmp", f"{uuid.uuid4()}.mp4")

    try:
        os.makedirs("tmp", exist_ok=True)

        with open(input_path, "wb") as f:
            f.write(await file.read())

        if algorithm == Algorithm.avc:
            output, compress_time = video.compress_video(
                input_path, output_path, "libx264"
            )
        elif algorithm == Algorithm.hevc:
            output, compress_time = video.compress_video(
                input_path, output_path, "libx265"
            )

        file_name = f"{file.filename.split('.')[0]}.mp4"
        original_size = f"{file.size / 1024 / 1024:.2f}"
        compressed_size = f"{os.path.getsize(output_path) / 1024 / 1024:.2f}"

        with open(output_path, "rb") as f:
            output = f.read()

        url = azure_storage.upload_blob("video", file_name, output)

        os.remove(input_path)
        os.remove(output_path)

        return {
            "data": {
                "type": "Video",
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
        if os.path.exists(input_path):
            os.remove(input_path)

        if os.path.exists(output_path):
            os.remove(output_path)

        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
