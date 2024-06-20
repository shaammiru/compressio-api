import time
import brotli
import zstandard


cctx = zstandard.ZstdCompressor()
dctx = zstandard.ZstdDecompressor()


def compress_text(data: bytes, algorithm: str):
    start_time = time.time()

    if algorithm == "brotli":
        compressed_data = brotli.compress(data, quality=11)
    else:
        compressed_data = cctx.compress(data)

    end_time = time.time()
    process_time = end_time - start_time

    if not isinstance(compressed_data, bytes):
        raise ValueError("Compressed data is not of type bytes")

    return compressed_data, process_time.__format__(".5f")


def decompress_text(data: bytes, algorithm: str):
    start_time = time.time()

    if algorithm == "brotli":
        decompressed_data = brotli.decompress(data)
    else:
        decompressed_data = dctx.decompress(data)

    end_time = time.time()
    process_time = end_time - start_time

    if not isinstance(decompressed_data, bytes):
        raise ValueError("Compressed data is not of type bytes")

    return decompressed_data, process_time.__format__(".5f")
