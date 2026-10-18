import yt_dlp
import sys

# Obtener la URL como argumento de línea de comandos
if len(sys.argv) < 2:
    print("Uso: python main.py <URL_DEL_VIDEO>")
    sys.exit(1)

video_url = sys.argv[1]
print(f"Descargando video desde: {video_url}")

# Configuración de descarga para 720p
output_filename = "C:/Users/jose/Downloads/%(title)s.%(ext)s"
ydl_opts = {
    "format": "bv*[height<=720]+ba/b[height<=720]",
    "merge_output_format": "mp4",
    "outtmpl": output_filename,
    "js_runtimes": {"node": {}},
    "ffmpeg_location": "C:/ffmpeg/bin",
    "noplaylist": True,  # Solo descargar el video individual, no la playlist
    "quiet": False,      # Cambiar a True para menos mensajes
    "no_warnings": False, # Cambiar a True para ocultar advertencias
    "postprocessors": [{
        'key': 'FFmpegVideoConvertor',
        'preferedformat': 'mp4',
    }]
}

# Realizar la descarga directamente
try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=True)
        print(f"✅ Descarga completada: {info['title']}")
except Exception as e:
    print(f"❌ Error al descargar: {str(e)}")

# Si quieres también iniciar la API después de descargar, descomenta las siguientes líneas:
"""
from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "API de descarga de videos está activa"}

if __name__ == "__main__":
    # Inicia la API en un puerto diferente para no bloquear la aplicación principal
    uvicorn.run(app, host="127.0.0.1", port=8000)
"""

# Comando para ejecutar:
# python main.py 'https://www.youtube.com/watch?v=yOjuwDZh_q0'