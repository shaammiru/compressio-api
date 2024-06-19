from fastapi import APIRouter
from enum import Enum
from service import text, azure_storage


class Algorithm(str, Enum):
    brotli = "brotli"
    todo = "todo"


router = APIRouter()


@router.get("/compress")
async def compress_text(algorithm: Algorithm):
    try:
        if algorithm == Algorithm.jpeg:
            compressed_output, compressed_time = text.compress_text("test.mp3", "JPEG")
            decompressed_output, decompressed_time = text.decompress_text()
        elif algorithm == Algorithm.webp:
            compressed_output, time = text.compress_text("test.mp3", "WEBP")
            decompressed_output, decompressed_time = text.decompress_text()

        compressed_url = azure_storage.upload_blob(
            "text/compressed", "TODO", compressed_output
        )
        decompressed_url = azure_storage.upload_blob(
            "text/decompressed", "TODO", decompressed_output
        )

        return {
            "data": {
                "type": "Text",
                "algorithm": algorithm,
                "url": {"compressed": compressed_url, "decompressed": decompressed_url},
                "time": {
                    "compressed": compressed_time,
                    "decompressed": decompressed_time,
                },
            }
        }
    except Exception:
        return {"message": "Internal Server Error"}
