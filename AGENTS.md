# Guía para agentes

## Propósito y arquitectura

- La aplicación principal es `descargar.py`: una consola interactiva que identifica YouTube, TikTok y Facebook a partir de la URL.
- `descargar.py` ejecuta el binario oficial independiente `yt-dlp.exe`. En una compilación PyInstaller, ese binario se incluye dentro del `.exe` principal y se copia a `%LOCALAPPDATA%\Descargar\yt-dlp.exe` al primer uso. El menú de actualización ejecuta `yt-dlp.exe --update`; actualizar un paquete Python con `pip` no actualizaría el binario que ya usa el ejecutable.
- `main_2.py` es intencionalmente independiente y descarga YouTube a máxima calidad. No lo combines con el flujo unificado salvo que el usuario lo solicite.
- `main.py`, `tiktok.py` y `facebook.py` son scripts anteriores que usan la biblioteca Python de `yt-dlp`. `requirements.txt` mantiene esa dependencia para esos scripts y para el modo fuente.
- `build_portable.ps1` prepara `.venv`, instala `requirements.txt` y `requirements-build.txt`, descarga el binario oficial de `yt-dlp` a `vendor\yt-dlp.exe` y compila `dist\Descargar.exe`.

## Requisitos y portabilidad

- El `.exe` no requiere Python en el equipo donde se ejecuta.
- FFmpeg es externo. `descargar.py` lo busca en `PATH`, al lado del ejecutable, en `ffmpeg\bin` junto al ejecutable y en `C:\ffmpeg\bin` para mantener compatibilidad con el equipo original. No reintroduzcas una ruta fija dependiente del usuario.
- YouTube requiere Node.js visible en `PATH` o `node.exe` junto a la aplicación. TikTok y Facebook no usan Node.js.
- Los archivos se guardan en la carpeta `Descargas` del usuario; no uses rutas absolutas del equipo de desarrollo.
- `vendor\yt-dlp.exe`, `.venv`, `env`, `build`, `dist`, los `.spec`, `.env` y los archivos descargados son artefactos locales y deben permanecer fuera de Git.

## Construcción e instalación

- Para construir en Windows con Python 3.10 o superior, ejecuta `powershell -ExecutionPolicy Bypass -File .\build_portable.ps1`.
- Para refrescar el binario incluido y reconstruir, agrega `-RefreshYtDlp`.
- El ejecutable se produce en `dist\Descargar.exe`. FFmpeg y Node.js no se empaquetan: el README explica cómo instalarlos o colocarlos junto al `.exe`.
- Al modificar argumentos de `yt-dlp`, conserva la configuración específica de cada plataforma y la detección de herramientas portables.

## Cambios y seguridad del repositorio

- No leas, imprimas, registres ni confirmes `.env` ni credenciales.
- Conserva `.gitignore` para excluir entornos virtuales, binarios descargados, compilaciones, medios descargados y archivos privados.
- No confirmes `vendor\yt-dlp.exe` ni ejecutables construidos; el script de construcción los obtiene cuando hacen falta.
- Mantén el README y esta guía sincronizados con los requisitos reales y la ubicación del ejecutable construido.
