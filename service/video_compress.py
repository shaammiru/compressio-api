import time
import ffmpeg


def compress_video(
    input_path: str, output_path: str, codec: str, crf=30, preset="faster"
):
    start_time = time.time()

    try:
        (
            ffmpeg.input(input_path)
            .output(output_path, vcodec=codec, acodec="aac", crf=crf, preset=preset)
            .run(overwrite_output=True)
        )
        print(f"Video successfully compressed and saved to {output_path}")
    except ffmpeg.Error as e:
        print(f"An error occurred: {e.stderr.decode()}")

    end_time = time.time()
    process_time = end_time - start_time

    return output_path, process_time


output_path, process_time = compress_video("test.mp4", "output_test.mp4", "libx265")
print(output_path, process_time)
