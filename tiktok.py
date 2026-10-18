import yt_dlp
import sys

if len(sys.argv) < 2:
    print("Uso: python main.py <URL_DEL_VIDEO>")
    sys.exit(1)

video_url = sys.argv[1]
print(f"Descargando video desde: {video_url}")

# Detectar si es TikTok
is_tiktok = "tiktok.com" in video_url

output_filename = "C:/Users/jose/Downloads/%(title)s.%(ext)s"

if is_tiktok:
    ydl_opts = {
        "format": "bestvideo+bestaudio/best",  # Sin límite de altura
        "merge_output_format": "mp4",
        "outtmpl": output_filename,
        "ffmpeg_location": "C:/ffmpeg/bin",
        "noplaylist": True,
        "quiet": False,
        "no_warnings": False,
        "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        },
    }
else:
    ydl_opts = {
        "format": "bestvideo[height<=720]+bestaudio/best[height<=720]",
        "merge_output_format": "mp4",
        "outtmpl": output_filename,
        "ffmpeg_location": "C:/ffmpeg/bin",
        "noplaylist": True,
        "quiet": False,
        "no_warnings": False,
        "postprocessors": [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }]
    }

try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=True)
        print(f"✅ Descarga completada: {info['title']}")
except Exception as e:
    print(f"❌ Error al descargar: {str(e)}")



# python tiktok.py "https://www.tiktok.com/@punoyork/video/7620668580887219464?_r=1&_t=ZS-94y63YUhD7a"