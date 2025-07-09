# YouTube Video Downloader

Un script simple para descargar videos de YouTube en formato MP4 con calidad 720p.

## Requisitos

- Python 3.7 o superior
- FFmpeg instalado en tu sistema

## Instalación

1. Clona este repositorio:

```bash
git clone https://github.com/tu-usuario/youtube-downloader.git
cd youtube-downloader
```

2. Crea un entorno virtual:

```bash
python -m venv env
```

3. Activa el entorno virtual:

```bash
# Windows
env\Scripts\activate

# Linux/Mac
source env/bin/activate
```

4. Instala las dependencias:

```bash
pip install -r requirements.txt
```

## Configuración

Antes de usar el script, asegúrate de:

1. Tener FFmpeg instalado y configurado en tu PATH, o modificar la ruta en el código:

```python
"ffmpeg_location": "C:/ffmpeg/bin"  # Cambia esta ruta según tu instalación
```

2. Modificar la ruta de descarga en el código:

```python
output_filename = "C:/Users/jose/Downloads/video_10.%(ext)s"  # Cambia esta ruta
```

## Uso

```bash
python main.py 'https://www.youtube.com/watch?v=VIDEO_ID'
```

## Ejemplo

```bash
python main.py 'https://www.youtube.com/watch?v=nGsUV5sY1Ps'
```

## Características

- Descarga en calidad 720p
- Convierte automáticamente a MP4
- Combina video y audio de la mejor calidad disponible
- Manejo básico de errores

## Licencia

Este proyecto es de código abierto y está disponible bajo la [Licencia MIT](LICENSE).

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o envía un pull request.

## Nota

Este script es solo para uso educativo y personal. Respeta los términos de servicio de YouTube y las leyes de derechos de autor de tu país.
