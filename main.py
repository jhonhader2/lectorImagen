from PIL import Image
import pytesseract
import re
import pandas as pd
import os
import glob
from dataclasses import dataclass
from typing import List, Optional
from concurrent.futures import ThreadPoolExecutor
from colorama import init, Fore, Style

# Inicializar colorama
init(autoreset=True)

@dataclass
class ImageData:
    """Clase para almacenar los datos extraídos de una imagen."""
    Archivo: str
    Latitud: str = ''
    Longitud: str = ''
    Fecha: str = ''
    Hora: str = ''

class ImageProcessor:
    """Clase para procesar una imagen individual y extraer datos utilizando OCR."""
    def __init__(self, ruta_tesseract=r'C:\Program Files\Tesseract-OCR\tesseract.exe'):
        pytesseract.pytesseract.tesseract_cmd = ruta_tesseract
        self.lat_pattern = re.compile(r'Lat[:\s]*([-+]?\d+[\.,]?\d*)[°]?', re.IGNORECASE)
        self.lon_pattern = re.compile(r'Long[:\s]*([-+]?\d+[\.,]?\d*)[°]?', re.IGNORECASE)
        self.fecha_hora_pattern = re.compile(r'(\d{1,2}/\d{1,2}/(\d{2}|\d{4})\s+\d{1,2}:\d{2}\s+[ap]\.? m\.?)', re.IGNORECASE)

    def procesar_imagen(self, ruta_archivo: str, ruta_carpeta_base: str) -> Optional[ImageData]:
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

            lat = self._extraer_coordenada(self.lat_pattern, texto, "latitud", nombre_relativo)
            if not lat:
                print(f"{Fore.YELLOW}No se encontró la latitud en {nombre_relativo}. Omitiendo esta imagen.{Style.RESET_ALL}")
                return None

            lon = self._extraer_coordenada(self.lon_pattern, texto, "longitud", nombre_relativo)
            fecha, hora = self._extraer_fecha_hora(texto, nombre_relativo)

            return ImageData(nombre_sin_extension, lat, lon, fecha, hora)

        except Exception as e:
            print(f"{Fore.RED}Error procesando {ruta_archivo}: {e}{Style.RESET_ALL}")
            return None

    def _extraer_coordenada(self, pattern, texto, tipo, nombre_archivo):
        match = pattern.search(texto)
        if match:
            return self.decimal_a_gms(float(match.group(1)))
        print(f"{Fore.YELLOW}No se encontró la {tipo} en el texto de {nombre_archivo}.{Style.RESET_ALL}")
        return ''

    def _extraer_fecha_hora(self, texto, nombre_archivo):
        match = self.fecha_hora_pattern.search(texto)
        if match:
            fecha_hora = ' '.join(match.group(1).split())
            fecha_part, hora_part = fecha_hora.split(' ', 1)
            dia, mes, anio = fecha_part.split('/')
            if len(anio) == 2:
                anio = '20' + anio
            return f"{dia}/{mes}/{anio}", hora_part.strip()
        print(f"{Fore.YELLOW}No se encontró la fecha y hora en el texto de {nombre_archivo}.{Style.RESET_ALL}")
        return '', ''

    @staticmethod
    def decimal_a_gms(grados_decimales):
        grados = int(grados_decimales)
        minutos_decimales = abs(grados_decimales - grados) * 60
        minutos = int(minutos_decimales)
        segundos = (minutos_decimales - minutos) * 60
        return f"{grados}° {minutos}' {segundos:.2f}\""

class ImageBatchProcessor:
    """Clase para procesar múltiples imágenes en una carpeta y sus subcarpetas."""
    def __init__(self, ruta_carpeta, ruta_tesseract=r'C:\Program Files\Tesseract-OCR\tesseract.exe'):
        self.ruta_carpeta = ruta_carpeta
        self.extensiones_imagen = ('*.jpg', '*.jpeg', '*.png', '*.bmp', '*.tiff')
        self.image_processor = ImageProcessor(ruta_tesseract)
        self.datos_imagenes: List[ImageData] = []

    def procesar_imagenes(self):
        archivos = self._obtener_archivos()
        with ThreadPoolExecutor() as executor:
            resultados = list(executor.map(self._procesar_archivo, archivos))
        self.datos_imagenes = [r for r in resultados if r]

    def _obtener_archivos(self):
        archivos = []
        for extension in self.extensiones_imagen:
            ruta_patron = os.path.join(self.ruta_carpeta, '**', extension)
            archivos.extend(glob.glob(ruta_patron, recursive=True))
        return archivos

    def _procesar_archivo(self, ruta_archivo):
        print(f"{Fore.CYAN}Procesando {ruta_archivo}...{Style.RESET_ALL}")
        return self.image_processor.procesar_imagen(ruta_archivo, self.ruta_carpeta)

    def guardar_datos_excel(self, nombre_archivo_excel='datos_extraidos.xlsx'):
        datos_validos = [img_data for img_data in self.datos_imagenes if img_data.Latitud]
        
        if not datos_validos:
            print(f"{Fore.RED}No se encontraron datos válidos para guardar en el Excel.{Style.RESET_ALL}")
            return

        df = pd.DataFrame([vars(img_data) for img_data in datos_validos])
        ruta_excel = os.path.join(self.ruta_carpeta, nombre_archivo_excel)
        df.to_excel(ruta_excel, index=False)
        print(f"{Fore.GREEN}Los datos han sido guardados en el archivo {ruta_excel}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Se guardaron {len(datos_validos)} registros de un total de {len(self.datos_imagenes)} imágenes procesadas.{Style.RESET_ALL}")

# Ejemplo de uso:
if __name__ == "__main__":
    ruta_carpeta_imagenes = input("Por favor, ingrese la ruta de la carpeta que contiene las imágenes: ")

    batch_processor = ImageBatchProcessor(ruta_carpeta_imagenes)

    print(f"{Fore.CYAN}Iniciando procesamiento de imágenes...{Style.RESET_ALL}")
    batch_processor.procesar_imagenes()

    print(f"{Fore.CYAN}Guardando datos en Excel...{Style.RESET_ALL}")
    batch_processor.guardar_datos_excel()

    print(f"{Fore.GREEN}Proceso completado.{Style.RESET_ALL}")