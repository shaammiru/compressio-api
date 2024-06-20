from enum import Enum
from fastapi import APIRouter, Query, File, UploadFile, HTTPException
from service import text, azure_storage, model


class Algorithm(str, Enum):
    brotli = "brotli"
    zstandard = "zstandard"


router = APIRouter()


@router.post(
    "/compress",
    response_model=model.DecompressResponseModel,
    name="Compress Text",
    description="Compress Text",
)
async def compress_text(
    algorithm: Algorithm = Query(...), file: UploadFile = File(...)
):
    try:
        binary_data = await file.read()

        if algorithm == Algorithm.brotli:
            extension = "br"
        elif algorithm == Algorithm.zstandard:
            extension = "zst"

        compressed_output, compressed_time = text.compress_text(
            binary_data, algorithm.value.lower()
        )
        decompressed_output, decompressed_time = text.decompress_text(
            compressed_output, algorithm.value.lower()
        )

        original_size = f"{file.size / 1024 / 1024:.2f}"
        compressed_filename = f"{file.filename.split('.')[0]}.{extension}"
        compressed_size = f"{len(compressed_output) / 1024 / 1024:.2f}"
        compressed_url = azure_storage.upload_blob(
            "text/compressed", compressed_filename, compressed_output
        )
        decompressed_size = f"{len(decompressed_output) / 1024 / 1024:.2f}"
        decompressed_url = azure_storage.upload_blob(
            "text/decompressed", file.filename, decompressed_output
        )

        return {
            "data": {
                "type": "Text",
                "algorithm": algorithm.value.upper(),
                "url": {"compressed": compressed_url, "decompressed": decompressed_url},
                "size": {
                    "original": original_size,
                    "compressed": compressed_size,
                    "decompressed": decompressed_size,
                },
                "time": {
                    "compressed": compressed_time,
                    "decompressed": decompressed_time,
                },
            }
        }
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
