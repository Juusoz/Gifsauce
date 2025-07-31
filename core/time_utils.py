from PyQt6.QtCore import QTime

def format_time(seconds: float) -> str:
    ms = int((seconds - int(seconds)) * 1000)
    t = QTime(0, 0, 0).addSecs(int(seconds))
    return t.toString("hh:mm:ss") + f".{ms:03}"

def parse_manual_time(h: str, m: str, s: str, ms: str) -> float:
    def to_int(value: str) -> int:
        return int(value) if value.strip().isdigit() else 0

    return (
        to_int(h) * 3600 +
        to_int(m) * 60 +
        to_int(s) +
        to_int(ms) / 1000
    )

