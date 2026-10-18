import yt_dlp
import sys
import os
import re
from datetime import datetime

# --- Obtener la URL desde argumentos ---
if len(sys.argv) < 2:
    print("Uso: python facebook.py <URL_DEL_VIDEO_DE_FACEBOOK>")
    sys.exit(1)

video_url = sys.argv[1]

# Validar que la URL sea de Facebook
if not re.search(r'facebook\.com|fb\.watch|fb\.com', video_url, re.IGNORECASE):
    print("❌ Error: La URL no parece ser de Facebook")
    print("Asegúrate de usar una URL válida de Facebook (facebook.com, fb.watch, fb.com)")
    sys.exit(1)

print(f"Descargando video desde Facebook: {video_url}")

# --- Configuración de descarga ---
downloads_path = os.path.expanduser("~/Downloads")

# 🔹 CAMBIO PRINCIPAL: Usa ID + fecha en lugar del título
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_filename = os.path.join(downloads_path, f"facebook_{timestamp}_%(id)s.%(ext)s")

# 🔹 ALTERNATIVA: Si quieres parte del título pero seguro
# output_filename = os.path.join(downloads_path, "%(id)s_%(title).50s.%(ext)s")

ydl_opts = {
    "format": "bestvideo+bestaudio/best",
    "merge_output_format": "mp4",
    "outtmpl": output_filename,
    "restrictfilenames": True,
    "windowsfilenames": True,  # 🔹 AÑADIDO: Fuerza compatibilidad con Windows
    "ffmpeg_location": "C:/ffmpeg/bin",
    "noplaylist": True,
    "quiet": False,
    "no_warnings": False,
    "postprocessors": [{
        'key': 'FFmpegVideoConvertor',
        'preferedformat': 'mp4',
    }]
}

# --- Descargar el video ---
try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=True)
        print(f"✅ Descarga completada: {info.get('title', 'Video de Facebook')}")
        print(f"📁 Guardado en: {downloads_path}")
except yt_dlp.DownloadError as e:
    print(f"❌ Error de descarga: {str(e)}")
except yt_dlp.ExtractorError as e:
    print(f"❌ Error al extraer información del video: {str(e)}")
except FileNotFoundError as e:
    print(f"❌ Error: No se encontró el archivo o directorio: {str(e)}")
except PermissionError as e:
    print(f"❌ Error de permisos: {str(e)}")
except Exception as e:
    print(f"❌ Error inesperado: {str(e)}")


# ------------COMO USAR----------
#   env\Scripts\activate
#   python facebook.py "https://www.facebook.com/watch/live/?ref=watch_permalink&v=668897179202084"