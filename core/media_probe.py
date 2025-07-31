import subprocess

def probe_video_properties(file_path):
    probe = subprocess.run([
        "ffprobe", "-v", "error", "-select_streams", "v:0",
        "-show_entries", "stream=width,height,r_frame_rate",
        "-of", "default=noprint_wrappers=1:nokey=1", file_path
    ], capture_output=True, text=True, check=True)

    w, h, fps = probe.stdout.strip().split("\n")
    return int(w), int(h), fps

def parse_fps(fps_string: str) -> float:
    try:
        num, denom = map(int, fps_string.split('/'))
        return round(num / denom)
    except ValueError:
        return None
