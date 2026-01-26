from yt_dlp import YoutubeDL
import os

def baixar_video(url, pasta="downloads"):
    os.makedirs(pasta, exist_ok=True)

    ydl_opts = {
        "outtmpl": os.path.join(pasta, "%(title)s.%(ext)s"),
        "format": "best"
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)

    return os.path.basename(filename)
