import time
import ffmpeg


def compress_audio(input_path: str, output_path: str, codec: str, bitrate="96k"):
    try:
        start_time = time.time()
        stream = ffmpeg.input(input_path)

        output_params = {
            "codec:a": codec,
            "b:a": bitrate,
        }

        stream = ffmpeg.output(stream, output_path, **output_params)
        ffmpeg.run(stream, overwrite_output=True)

        end_time = time.time()
        process_time = end_time - start_time

        return output_path, process_time
    except ffmpeg.Error as e:
        raise e


output_path, process_time = compress_audio("test.mp3", "output.aac", "aac")
print(output_path, process_time)
