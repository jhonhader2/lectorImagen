import os
from PIL import Image
import pytesseract
import re
from colorama import Fore, Style
from models import ImageData
from utils import decimal_a_gms

class OCRProcessor:
    def __init__(self, ruta_tesseract):
        pytesseract.pytesseract.tesseract_cmd = ruta_tesseract
        self.lat_pattern = re.compile(r'Lat[:\s]*([-+]?\d+[\.,]?\d*)[°]?', re.IGNORECASE)
        self.lon_pattern = re.compile(r'Long[:\s]*([-+]?\d+[\.,]?\d*)[°]?', re.IGNORECASE)
        self.fecha_hora_pattern = re.compile(r'(\d{1,2}/\d{1,2}/(\d{2}|\d{4})\s+\d{1,2}:\d{2}\s+[ap]\.? m\.?)', re.IGNORECASE)

    def procesar_imagen(self, ruta_archivo, ruta_carpeta_base):
        try:
            nombre_sin_extension = self._obtener_nombre_archivo(ruta_archivo, ruta_carpeta_base)
            texto = self._extraer_texto(ruta_archivo)
            
            lat = self._extraer_coordenada(self.lat_pattern, texto, "latitud", nombre_sin_extension)
            if not lat:
                print(f"{Fore.YELLOW}No se encontró la latitud en {nombre_sin_extension}. Omitiendo esta imagen.{Style.RESET_ALL}")
                return None

            lon = self._extraer_coordenada(self.lon_pattern, texto, "longitud", nombre_sin_extension)
            fecha, hora = self._extraer_fecha_hora(texto, nombre_sin_extension)

            return ImageData(nombre_sin_extension, lat, lon, fecha, hora)
        except Exception as e:
            print(f"{Fore.RED}Error procesando {ruta_archivo}: {e}{Style.RESET_ALL}")
            return None

    def _obtener_nombre_archivo(self, ruta_archivo, ruta_carpeta_base):
        ruta_relativa = os.path.relpath(ruta_archivo, ruta_carpeta_base)
        nombre_relativo = ruta_relativa.replace(os.sep, '_')
        return os.path.splitext(nombre_relativo)[0]

    def _extraer_texto(self, ruta_archivo):
        with Image.open(ruta_archivo) as image:
            texto = pytesseract.image_to_string(image, lang='spa')
        return texto.replace(',', '.')

    def _extraer_coordenada(self, pattern, texto, tipo, nombre_archivo):
        match = pattern.search(texto)
        if match:
            return decimal_a_gms(float(match.group(1)))
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