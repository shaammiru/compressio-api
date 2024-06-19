import time
from PIL import Image
from io import BytesIO


def compress_image(image_buffer: BytesIO, algorithm: str):
    output_buffer = BytesIO()
    start_time = time.time()

    image = Image.open(image_buffer)
    image.save(output_buffer, algorithm, quality=80)

    end_time = time.time()
    process_time = end_time - start_time
    output_buffer.seek(0)

    return output_buffer, process_time.__format__(".3f")
