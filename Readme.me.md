# Procesador de Imágenes OCR

## Descripción
Este proyecto es un procesador de imágenes que utiliza OCR (Reconocimiento Óptico de Caracteres) para extraer información de imágenes, incluyendo fecha, hora, latitud y longitud. Procesa múltiples imágenes en paralelo y guarda los resultados en un archivo Excel.

## Inspiración
Este proyecto se inspiró en parte en aplicaciones como [GPS Map Camera](https://gpsmapcamera.com/), que permite a los usuarios geoetiquetar fotos y añadir información GPS directamente en las imágenes. Mientras que GPS Map Camera se centra en la captura de imágenes con datos GPS en tiempo real, nuestro proyecto se enfoca en el procesamiento posterior de imágenes para extraer esta información.

## Características principales
- Procesamiento en lote de imágenes utilizando OCR.
- Extracción de fecha, hora, latitud y longitud de las imágenes.
- Procesamiento paralelo para mejorar la eficiencia.
- Generación de un archivo Excel con los datos extraídos.
- Interfaz de línea de comandos para fácil uso.
- Resumen detallado del proceso, incluyendo estadísticas de procesamiento.

## Requisitos
- Python 3.6+
- Tesseract OCR
- Bibliotecas Python:
  - opencv-python
  - pytesseract
  - pandas
  - colorama
  - tqdm

## Instalación
1. Clona este repositorio o descarga los archivos.
2. Instala Tesseract OCR en tu sistema.
3. Instala las dependencias de Python:
   ```
   pip install opencv-python pytesseract pandas colorama tqdm
   ```

## Uso
1. Ejecuta el script principal:
   ```
   python main.py
   ```
2. Sigue las instrucciones en pantalla:
   - Ingresa la ruta de la carpeta que contiene las imágenes a procesar.
   - Ingresa el nombre del archivo Excel donde se guardarán los resultados.

3. El programa procesará las imágenes y mostrará un resumen del proceso.
4. Los resultados se guardarán en el archivo Excel especificado.

## Estructura del proyecto
- `main.py`: Script principal para ejecutar el programa.
- `image_processor.py`: Contiene la lógica principal del procesamiento de imágenes.
- `ocr_processor.py`: Maneja la extracción de texto de las imágenes usando OCR.
- `models.py`: Define la estructura de datos para almacenar la información extraída.

## Resultados
El programa generará un archivo Excel con las siguientes columnas:
- Nombre del archivo
- Fecha
- Hora
- Latitud
- Longitud

Además, se mostrará un resumen en consola con:
- Total de archivos encontrados
- Total de archivos procesados
- Total de archivos con errores
- Total de archivos sin fecha/hora
- Número de registros guardados en el Excel

## Contribuciones
Las contribuciones son bienvenidas. Por favor, abre un issue para discutir cambios mayores antes de hacer un pull request.

## Licencia
[Incluye aquí la licencia de tu proyecto, por ejemplo MIT, GPL, etc.]