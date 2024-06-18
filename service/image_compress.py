import time
from PIL import Image
from io import BytesIO


def compress_image_jpeg(image_buffer):
    output_buffer = BytesIO()
    start_time = time.time()

    image = Image.open(image_buffer)
    image.save(output_buffer, "JPEG", quality=80)

    end_time = time.time()
    process_time = end_time - start_time
    output_buffer.seek(0)

    return output_buffer, process_time


def compress_image_webp(image_buffer):
    output_buffer = BytesIO()
    start_time = time.time()

    image = Image.open(image_buffer)
    image.save(output_buffer, "WEBP", quality=80)

    end_time = time.time()
    process_time = end_time - start_time
    output_buffer.seek(0)

    return output_buffer, process_time


buffer, total_time = compress_image_webp("test.png")
print(f"{total_time:.2f} Second")
