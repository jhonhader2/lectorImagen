from PIL import Image
import pytesseract
import re
import pandas as pd
import os
import glob

class ImageData:
    """
    Clase para almacenar los datos extraídos de una imagen.
    """
    def __init__(self, nombre_archivo, latitud='', longitud='', fecha='', hora=''):
        self.Archivo = nombre_archivo
        self.Latitud = latitud
        self.Longitud = longitud
        self.Fecha = fecha
        self.Hora = hora

class ImageProcessor:
    """
    Clase para procesar una imagen individual y extraer datos utilizando OCR.
    """
    def __init__(self, ruta_tesseract=r'C:\Program Files\Tesseract-OCR\tesseract.exe'):
        # Configura la ruta al ejecutable de Tesseract
        pytesseract.pytesseract.tesseract_cmd = ruta_tesseract

    def procesar_imagen(self, ruta_archivo, ruta_carpeta_base):
        try:
            # Obtiene la ruta relativa del archivo respecto a la carpeta base
            ruta_relativa = os.path.relpath(ruta_archivo, ruta_carpeta_base)
            # Reemplaza los separadores de directorio por guiones bajos para evitar problemas
            nombre_relativo = ruta_relativa.replace(os.sep, '_')
            nombre_sin_extension = os.path.splitext(nombre_relativo)[0]

            # Abre la imagen
            image = Image.open(ruta_archivo)

            # Extrae el texto de la imagen
            texto = pytesseract.image_to_string(image, lang='spa')

            # Reemplazar comas por puntos en números decimales si es necesario
            texto = texto.replace(',', '.')

            # Inicializa variables
            lat = ''
            lon = ''
            fecha = ''
            hora = ''

            # Expresiones regulares ajustadas
            lat_pattern = r'Lat[:\s]*([-+]?\d+[\.,]?\d*)[°]?'
            lon_pattern = r'Long[:\s]*([-+]?\d+[\.,]?\d*)[°]?'
            fecha_hora_pattern = r'(\d{1,2}/\d{1,2}/(\d{2}|\d{4})\s+\d{1,2}:\d{2}\s+[ap]\.? m\.?)'

            lat_match = re.search(lat_pattern, texto, re.IGNORECASE)
            lon_match = re.search(lon_pattern, texto, re.IGNORECASE)
            fecha_hora_match = re.search(fecha_hora_pattern, texto, re.IGNORECASE)

            if lat_match:
                lat = lat_match.group(1)
            else:
                print(f"No se encontró la latitud en el texto de {nombre_relativo}.")

            if lon_match:
                lon = lon_match.group(1)
            else:
                print(f"No se encontró la longitud en el texto de {nombre_relativo}.")

            if fecha_hora_match:
                fecha_hora = fecha_hora_match.group(1)
                # Limpiar la cadena por si hay espacios adicionales
                fecha_hora = ' '.join(fecha_hora.split())

                # Dividir la cadena en fecha y hora
                try:
                    # Dividir por el primer espacio
                    fecha_part, hora_part = fecha_hora.split(' ', 1)

                    # fecha_part contiene la fecha
                    fecha = fecha_part.strip()

                    # hora_part contiene la hora y el indicador 'a. m.' o 'p. m.'
                    hora = hora_part.strip()

                    # Verificar si el año es de dos dígitos y convertirlo a cuatro dígitos
                    dia, mes, anio = fecha.split('/')
                    if len(anio) == 2:
                        anio = '20' + anio
                        fecha = f"{dia}/{mes}/{anio}"

                except ValueError:
                    print(f"Error al separar la fecha y hora en {nombre_relativo}")
                    fecha = ''
                    hora = ''
            else:
                print(f"No se encontró la fecha y hora en el texto de {nombre_relativo}.")
                fecha = ''
                hora = ''

            # Convierte las coordenadas a formato GMS si es necesario
            if lat and lon:
                lat = self.decimal_a_gms(float(lat))
                lon = self.decimal_a_gms(float(lon))
            else:
                lat = ''
                lon = ''

            # Retorna un objeto ImageData con los datos extraídos
            return ImageData(nombre_sin_extension, lat, lon, fecha, hora)

        except FileNotFoundError:
            print(f"No se encontró el archivo de imagen {ruta_archivo}. Verifica la ruta y el nombre del archivo.")
            return None
        except pytesseract.TesseractNotFoundError:
            print("No se encontró el ejecutable de Tesseract OCR. Verifica la ruta y la instalación.")
            return None
        except Exception as e:
            print(f"Ocurrió un error procesando {ruta_archivo}: {e}")
            return None

    @staticmethod
    def decimal_a_gms(grados_decimales):
        grados = int(grados_decimales)
        minutos_decimales = abs(grados_decimales - grados) * 60
        minutos = int(minutos_decimales)
        segundos = (minutos_decimales - minutos) * 60
        return f"{grados}° {minutos}' {segundos:.2f}\""

class ImageBatchProcessor:
    """
    Clase para procesar múltiples imágenes en una carpeta y sus subcarpetas.
    """
    def __init__(self, ruta_carpeta, ruta_tesseract=r'C:\Program Files\Tesseract-OCR\tesseract.exe'):
        self.ruta_carpeta = ruta_carpeta
        self.extensiones_imagen = ('*.jpg', '*.jpeg', '*.png', '*.bmp', '*.tiff')
        self.image_processor = ImageProcessor(ruta_tesseract)
        self.datos_imagenes = []

    def procesar_imagenes(self):
        # Recorre cada patrón de extensión
        for extension in self.extensiones_imagen:
            # Usa glob para obtener la lista de archivos con la extensión actual de forma recursiva
            ruta_patron = os.path.join(self.ruta_carpeta, '**', extension)
            archivos = glob.glob(ruta_patron, recursive=True)

            for ruta_archivo in archivos:
                print(f"Procesando {ruta_archivo}...")
                datos = self.image_processor.procesar_imagen(ruta_archivo, self.ruta_carpeta)
                if datos:
                    self.datos_imagenes.append(datos)

    def guardar_datos_excel(self, nombre_archivo_excel='datos_extraidos.xlsx'):
        # Crear un DataFrame con todos los datos
        data = [vars(img_data) for img_data in self.datos_imagenes]
        df = pd.DataFrame(data)

        # Guardar en un archivo Excel
        ruta_excel = os.path.join(self.ruta_carpeta, nombre_archivo_excel)
        df.to_excel(ruta_excel, index=False)
        print(f"Los datos han sido guardados en el archivo {ruta_excel}")

# Ejemplo de uso:
if __name__ == "__main__":
    # Especifica la ruta de la carpeta que contiene las imágenes y subcarpetas
    ruta_carpeta_imagenes = r'C:\Users\jhonh\OneDrive - Instituto Colombiano de Bienestar Familiar\SFSC\2024\Repositorio_SFSC\Somos Familias, Somos Comunidad Guaviare'

    # Crea una instancia del procesador de lotes de imágenes
    batch_processor = ImageBatchProcessor(ruta_carpeta_imagenes)

    # Procesa todas las imágenes en la carpeta y sus subcarpetas
    batch_processor.procesar_imagenes()

    # Guarda los datos extraídos en un archivo Excel
    batch_processor.guardar_datos_excel()
