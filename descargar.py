"""Descargador interactivo para YouTube, TikTok y Facebook."""

import os
import shutil
import subprocess
import sys
from datetime import datetime
from urllib.parse import urlparse


DOWNLOADS_PATH = os.path.join(os.path.expanduser("~"), "Downloads")
APP_DATA_PATH = os.path.join(
    os.environ.get("LOCALAPPDATA", os.path.join(os.path.expanduser("~"), "AppData", "Local")),
    "Descargar",
)
YT_DLP_PATH = os.path.join(APP_DATA_PATH, "yt-dlp.exe")


def detectar_plataforma(url):
    """Identifica la plataforma desde el dominio del enlace."""
    if "://" not in url:
        url = "https://" + url
    host = (urlparse(url).hostname or "").lower()

    if host == "youtu.be" or host == "youtube.com" or host.endswith(".youtube.com"):
        return "youtube"
    if host == "tiktok.com" or host.endswith(".tiktok.com"):
        return "tiktok"
    if (
        host == "facebook.com"
        or host.endswith(".facebook.com")
        or host == "fb.com"
        or host.endswith(".fb.com")
        or host == "fb.watch"
        or host.endswith(".fb.watch")
    ):
        return "facebook"
    return None


def ruta_yt_dlp_incluida():
    """Ubica la copia oficial de yt-dlp empaquetada dentro del ejecutable."""
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    candidatos = [
        os.path.join(base_path, "yt-dlp.exe"),
        os.path.join(base_path, "vendor", "yt-dlp.exe"),
    ]
    return next((ruta for ruta in candidatos if os.path.isfile(ruta)), candidatos[0])


def directorio_aplicacion():
    """Directorio del EXE o, en modo fuente, del script Python."""
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


def localizar_ffmpeg():
    """Busca FFmpeg junto a la app, en una carpeta portable o en PATH."""
    carpeta_app = directorio_aplicacion()
    candidatos = [
        carpeta_app,
        os.path.join(carpeta_app, "ffmpeg", "bin"),
        os.path.join(carpeta_app, "ffmpeg", "bin", "x64"),
        r"C:\ffmpeg\bin",  # Compatibilidad con la instalación usada en el equipo original.
    ]
    for carpeta in candidatos:
        if os.path.isfile(os.path.join(carpeta, "ffmpeg.exe")):
            return carpeta

    ffmpeg_en_path = shutil.which("ffmpeg.exe") or shutil.which("ffmpeg")
    return os.path.dirname(ffmpeg_en_path) if ffmpeg_en_path else None


def preparar_entorno():
    """Permite incluir node.exe junto al EXE en una carpeta portable."""
    entorno = os.environ.copy()
    node_local = os.path.join(directorio_aplicacion(), "node.exe")
    if os.path.isfile(node_local):
        entorno["PATH"] = os.path.dirname(node_local) + os.pathsep + entorno.get("PATH", "")
    return entorno


def asegurar_yt_dlp():
    """Instala la copia incluida en una ruta escribible por el usuario."""
    os.makedirs(APP_DATA_PATH, exist_ok=True)
    if not os.path.isfile(YT_DLP_PATH):
        bundled_path = ruta_yt_dlp_incluida()
        if not os.path.isfile(bundled_path):
            raise FileNotFoundError("No se encontró yt-dlp.exe dentro del paquete.")
        shutil.copy2(bundled_path, YT_DLP_PATH)
    return YT_DLP_PATH


def argumentos_descarga(plataforma, url, ffmpeg_location):
    """Construye los argumentos de yt-dlp según la plataforma."""
    os.makedirs(DOWNLOADS_PATH, exist_ok=True)

    argumentos = [
        "--no-playlist",
        "--ffmpeg-location", ffmpeg_location,
        "--merge-output-format", "mp4",
    ]

    if plataforma == "youtube":
        argumentos += [
            "--format", "bv*[height<=720]+ba/b[height<=720]",
            "--js-runtimes", "node",
            "--recode-video", "mp4",
            "--output", os.path.join(DOWNLOADS_PATH, "%(title)s.%(ext)s"),
        ]
    elif plataforma == "tiktok":
        argumentos += [
            "--format", "bestvideo+bestaudio/best",
            "--user-agent",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "--output", os.path.join(DOWNLOADS_PATH, "%(title)s.%(ext)s"),
        ]
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        argumentos += [
            "--format", "bestvideo+bestaudio/best",
            "--restrict-filenames",
            "--windows-filenames",
            "--recode-video", "mp4",
            "--output", os.path.join(
                DOWNLOADS_PATH, f"facebook_{timestamp}_%(id)s.%(ext)s"
            ),
        ]

    argumentos.append(url)
    return argumentos


def descargar_video(url):
    url = url.strip()
    plataforma = detectar_plataforma(url)
    if not plataforma:
        print("URL no reconocida. Pega un enlace de YouTube, TikTok o Facebook.")
        return

    print(f"\nDescargando desde {plataforma.capitalize()}...\n")
    try:
        ffmpeg_location = localizar_ffmpeg()
        if not ffmpeg_location:
            print(
                "No encontré FFmpeg. Instálalo y agrégalo a PATH, o coloca "
                "ffmpeg.exe en la misma carpeta del programa o dentro de ffmpeg\\bin."
            )
            return

        entorno = preparar_entorno()
        if plataforma == "youtube" and not shutil.which("node", path=entorno.get("PATH")):
            print(
                "YouTube necesita Node.js para la extracción actual. Instálalo y "
                "agrégalo a PATH, o coloca node.exe junto a Descargar.exe."
            )
            return

        yt_dlp_path = asegurar_yt_dlp()
        resultado = subprocess.run(
            [yt_dlp_path, *argumentos_descarga(plataforma, url, ffmpeg_location)],
            check=False,
            env=entorno,
        )
        if resultado.returncode == 0:
            print(f"\nDescarga completada. Archivo guardado en: {DOWNLOADS_PATH}")
        else:
            print(f"\nLa descarga terminó con un error (código {resultado.returncode}).")
    except FileNotFoundError as error:
        print(f"\nNo se encontró una herramienta necesaria: {error}")
    except Exception as error:
        print(f"\nError al descargar: {error}")


def actualizar_yt_dlp():
    """Actualiza el binario oficial de yt-dlp para próximas descargas."""
    print("\nBuscando actualizaciones de yt-dlp...\n")
    try:
        yt_dlp_path = asegurar_yt_dlp()
        resultado = subprocess.run([yt_dlp_path, "--update"], check=False)
        if resultado.returncode == 0:
            print("Actualización de yt-dlp completada.")
        else:
            print(f"La actualización terminó con un error (código {resultado.returncode}).")
    except Exception as error:
        print(f"No se pudo actualizar yt-dlp: {error}")
    input("Presiona Enter para volver al menú...")


def menu():
    while True:
        print("\n=== DESCARGADOR DE VIDEOS ===")
        print("1. Descargar un video")
        print("2. Actualizar yt-dlp (librería de descargas)")
        print("3. Cerrar")

        try:
            opcion = input("Elige una opción (1, 2 o 3): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nCerrando descargador.")
            return

        if opcion == "1":
            try:
                url = input("Pega la URL del video y presiona Enter: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nVolviendo al menú.")
                continue
            if url:
                descargar_video(url)
            else:
                print("No ingresaste ninguna URL.")
        elif opcion == "2":
            actualizar_yt_dlp()
        elif opcion == "3":
            print("Cerrando descargador.")
            return
        else:
            print("Opción no válida. Elige 1, 2 o 3.")


def main():
    # También permite usar el programa desde una terminal con: descargar.py URL
    if len(sys.argv) > 1:
        descargar_video(sys.argv[1])
    else:
        menu()


if __name__ == "__main__":
    main()
