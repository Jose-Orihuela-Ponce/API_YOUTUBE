# Descargador portable de videos

Aplicación de consola para Windows que descarga videos de YouTube, TikTok y Facebook. El programa principal es `descargar.py`; también se puede empaquetar como un ejecutable de un solo archivo para usarlo sin instalar Python en la PC de destino.

## Funciones

- Detecta la plataforma desde la URL.
- YouTube: descarga hasta 720p.
- TikTok: solicita la mejor calidad disponible y usa un encabezado de navegador.
- Facebook: solicita la mejor calidad disponible y genera un nombre de archivo único.
- Guarda los videos en la carpeta `Descargas` del usuario.
- Incluye un menú para descargar otro video, actualizar `yt-dlp` o cerrar.
- `main_2.py` se mantiene como script separado para YouTube en máxima calidad.

## Requisitos en otra PC

Para ejecutar `Descargar.exe` no hace falta instalar Python. Sí se necesita:

- Windows de 64 bits.
- FFmpeg, necesario para combinar audio y video. La aplicación lo busca en `PATH`, junto al ejecutable, en `ffmpeg\bin` junto al ejecutable y en `C:\ffmpeg\bin`.
- Node.js visible en `PATH` o `node.exe` junto a `Descargar.exe` para descargas de YouTube.

TikTok y Facebook no requieren Node.js, pero sí FFmpeg para combinar las pistas. Si se desea mover la aplicación como carpeta portable, se puede organizar así:

```text
Descargador/
├── Descargar.exe
├── node.exe                 # para YouTube, o instalar Node.js en el sistema
└── ffmpeg/
    └── bin/
        ├── ffmpeg.exe
        ├── ffprobe.exe
        └── archivos auxiliares de esa distribución de FFmpeg
```

También se pueden instalar FFmpeg y Node.js en el sistema y agregarlos a `PATH`. `yt-dlp.exe` viene incluido dentro de `Descargar.exe`; la primera ejecución lo copia al perfil local del usuario para que la opción de actualización pueda mantenerlo al día.

## Crear el ejecutable portable

En la PC de desarrollo se necesita Python 3.10 o superior y acceso a Internet para descargar el binario oficial de `yt-dlp`.

Desde PowerShell, en la carpeta del proyecto:

```powershell
powershell -ExecutionPolicy Bypass -File .\build_portable.ps1
```

El script crea el entorno `.venv`, instala las dependencias de construcción, descarga `yt-dlp.exe` desde los releases oficiales si aún no existe y genera:

```text
dist\Descargar.exe
```

Para volver a descargar la versión más reciente de `yt-dlp` antes de construir:

```powershell
powershell -ExecutionPolicy Bypass -File .\build_portable.ps1 -RefreshYtDlp
```

El ejecutable se puede copiar al Escritorio o a una carpeta portable. FFmpeg y Node.js no se incluyen en el `.exe`; deben instalarse en el equipo o colocarse junto al programa como se describe arriba.

## Ejecutar desde el código fuente

El script de empaquetado descarga `vendor\yt-dlp.exe`, que también permite ejecutar el menú directamente desde el código:

```powershell
powershell -ExecutionPolicy Bypass -File .\build_portable.ps1
python .\descargar.py
```

Para usar los scripts Python que llaman directamente a la biblioteca `yt-dlp`:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Luego se puede ejecutar, por ejemplo:

```powershell
python .\main.py "https://www.youtube.com/watch?v=VIDEO_ID"
python .\main_2.py "https://www.youtube.com/watch?v=VIDEO_ID"
python .\tiktok.py "URL_DE_TIKTOK"
python .\facebook.py "URL_DE_FACEBOOK"
```

`main.py`, `tiktok.py` y `facebook.py` son scripts antiguos separados; para el uso normal se recomienda `Descargar.exe` o `descargar.py`. `main_2.py` sigue siendo el script independiente de YouTube a máxima calidad.

## Archivos principales

| Archivo | Propósito |
| --- | --- |
| `descargar.py` | Menú unificado y lógica de empaquetado del descargador principal. |
| `build_portable.ps1` | Prepara el entorno, obtiene `yt-dlp.exe` y construye el ejecutable Windows. |
| `main_2.py` | Descarga independiente de YouTube a máxima calidad. |
| `main.py`, `tiktok.py`, `facebook.py` | Scripts previos de descarga por plataforma. |
| `requirements.txt` | Dependencias para ejecutar los scripts Python antiguos. |
| `requirements-build.txt` | PyInstaller requerido para generar el `.exe`. |
| `AGENTS.md` | Guía de arquitectura e instrucciones para agentes que mantengan el proyecto. |

## Uso responsable

Descarga contenido únicamente cuando tengas derecho a hacerlo. Respeta las condiciones de uso de cada plataforma y las leyes de derechos de autor aplicables.
