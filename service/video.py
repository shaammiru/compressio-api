import time
import ffmpeg


def compress_video(
    input_path: str, output_path: str, codec: str, crf=30, preset="faster", bitrate=None
):
    try:
        start_time = time.time()
        stream = ffmpeg.input(input_path)

        output_params = {
            "vcodec": codec,
            "acodec": "aac",
            "crf": crf,
            "preset": preset,
        }

        if bitrate:
            output_params["video_bitrate"] = bitrate

        stream = ffmpeg.output(stream, output_path, **output_params)
        ffmpeg.run(stream, overwrite_output=True)

        end_time = time.time()
        process_time = end_time - start_time

        return output_path, process_time
    except ffmpeg.Error as e:
        raise e


output_path, process_time = compress_video("test.mp4", "output.mp4", "libx264")
print(output_path, process_time)
