### Instrucciones de Uso

1. **Instalar dependencias**:
   - Asegúrate de tener `pip` instalado.
   - Ejecuta el siguiente comando para instalar las bibliotecas necesarias:
     ```bash
     pip install -r requirements.txt
Instalar ffmpeg:
El proyecto utiliza ffmpeg para generar animaciones. Debes instalarlo en tu sistema:
Windows: Usa choco install ffmpeg (con Chocolatey) o descarga desde el sitio oficial de FFmpeg.
MacOS: Usa brew install ffmpeg (con Homebrew).
Linux: Usa sudo apt-get install ffmpeg (en Ubuntu) o el equivalente en tu distribución.
Ejecutar el simulador:
Ejecuta el archivo principal con:
bash

Collapse

Wrap

Run

Copy
python main.py
La interfaz de Gradio se abrirá en tu navegador en http://127.0.0.1:7860.
Visualizar animaciones:
Las animaciones de la simulación se guardan en el directorio animations/ dentro del proyecto.
Puedes verlas directamente en la interfaz de Gradio o abrir los archivos MP4 manualmente.
text

Collapse

Wrap

Copy
---

### Resumen

- **Modularidad**: Cada archivo tiene una responsabilidad clara y está diseñado para ser reutilizable.
- **Buenas prácticas**: Se siguen las convenciones de PEP 8, con comentarios claros y manejo de errores robusto.
- **Compatibilidad**: Las firmas de las funciones existentes se han mantenido, extendiendo su funcionalidad sin romper el código previo.
- **Funcionalidad completa**: Las animaciones se generan, se integran en la simulación y se muestran en la interfaz de usuario.

Esta solución está lista para ser implementada en el proyecto `simulacion-cinturon/`.