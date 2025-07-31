import os
import subprocess

def convert_video_to_gif(input_file, output_file, width, height, start_time, end_time, fps, max_colors):
    palette_file = ".temp_palette.png"
    trim_args = ["-ss", str(start_time), "-to", str(end_time)]

    # First, generate palette
    palette_cmd = [
        "ffmpeg", "-y", *trim_args, "-i", input_file,
        "-vf", f"fps={fps},scale={width}:{height}:flags=lanczos,palettegen=max_colors={max_colors}",
        palette_file
    ]
    subprocess.run(palette_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    # Then, create gif using palette
    gif_cmd = [
        "ffmpeg", "-y", *trim_args, "-i", input_file, "-i", palette_file,
        "-filter_complex",
        f"[0:v]mpdecimate,scale={width}:{height}:flags=lanczos,fps={fps},setpts=PTS-STARTPTS[clean];[clean][1:v]paletteuse",
        output_file
    ]
    subprocess.run(gif_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    if os.path.exists(palette_file):
        os.remove(palette_file)
