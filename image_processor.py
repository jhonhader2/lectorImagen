import os
import glob
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from colorama import Fore, Style
import pandas as pd
from ocr_processor import OCRProcessor
from models import ImageData

class ImageBatchProcessor:
    def __init__(self, ruta_carpeta, ruta_tesseract=r'C:\Program Files\Tesseract-OCR\tesseract.exe'):
        self.ruta_carpeta = ruta_carpeta
        self.extensiones_imagen = ('*.jpg', '*.jpeg', '*.png', '*.bmp', '*.tiff')
        self.ocr_processor = OCRProcessor(ruta_tesseract)
        self.datos_imagenes = []
        self.archivos_con_error = []
        self.archivos_sin_fecha_hora = []
        self.total_archivos = 0
        self.mensajes_procesamiento = []

    def procesar_imagenes(self):
        archivos = self._obtener_archivos()
        self.total_archivos = len(archivos)
        
        with ThreadPoolExecutor() as executor:
            resultados = list(tqdm(executor.map(self._procesar_archivo, archivos), total=self.total_archivos, desc="Procesando imágenes"))
        
        self.datos_imagenes = [r for r in resultados if r is not None]       

        print("\n" + "="*50)
        print("\nResumen del procesamiento:")
        for mensaje in self.mensajes_procesamiento:
            print(mensaje)
        
        if self.archivos_con_error:
            print(f"\n{Fore.RED}Los siguientes archivos no se pudieron procesar:{Style.RESET_ALL}")
            for archivo in self.archivos_con_error:
                print(f"{Fore.RED}- {archivo}{Style.RESET_ALL}")
        
        if self.archivos_sin_fecha_hora:
            print(f"\n{Fore.YELLOW}No se encontró la fecha y hora en el texto de los siguientes archivos:{Style.RESET_ALL}")
            for archivo in self.archivos_sin_fecha_hora:
                print(f"{Fore.YELLOW}- {archivo}{Style.RESET_ALL}")
        
        print("\n" + "="*50)

    def _obtener_archivos(self):
        return [
            archivo
            for extension in self.extensiones_imagen
            for archivo in glob.glob(os.path.join(self.ruta_carpeta, '**', extension), recursive=True)
        ]

    def _procesar_archivo(self, ruta_archivo):
        resultado = self.ocr_processor.procesar_imagen(ruta_archivo, self.ruta_carpeta)
        mensaje = f"Procesado: {os.path.basename(ruta_archivo)}"
        if resultado is None:
            self.archivos_con_error.append(ruta_archivo)
            mensaje += f" - {Fore.RED}Error al procesar{Style.RESET_ALL}"
        elif not resultado.fecha or not resultado.hora:
            self.archivos_sin_fecha_hora.append(ruta_archivo)
            mensaje += f" - {Fore.YELLOW}Sin fecha/hora{Style.RESET_ALL}"
        else:
            mensaje += f" - {Fore.GREEN}OK{Style.RESET_ALL}"
        self.mensajes_procesamiento.append(mensaje)
        return resultado

    def guardar_datos_excel(self):
        datos_a_guardar = self.datos_imagenes
        
        if not datos_a_guardar:
            print(f"{Fore.RED}No se encontraron datos para guardar en el Excel.{Style.RESET_ALL}")
            return

        print(f"\n{Fore.CYAN}Resumen del proceso:{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Total de archivos encontrados: {self.total_archivos}{Style.RESET_ALL}")
        print(f"{Fore.RED}Total de archivos no procesados: {len(self.archivos_con_error)}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Total de archivos sin fecha y hora: {len(self.archivos_sin_fecha_hora)}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Total de archivos procesados: {len(self.datos_imagenes)}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Se pueden guardar {len(datos_a_guardar)} registros en el archivo Excel.{Style.RESET_ALL}")

        # Preguntar al usuario si desea guardar el archivo
        respuesta = input(f"\n{Fore.CYAN}¿Desea guardar los datos en un archivo Excel? (s/n): {Style.RESET_ALL}").lower()
        
        if respuesta == 's':
            nombre_archivo = input(f"{Fore.CYAN}Por favor, ingrese el nombre del archivo Excel (sin extensión): {Style.RESET_ALL}")
            nombre_archivo_excel = f"{nombre_archivo}.xlsx"
            
            df = pd.DataFrame([vars(img_data) for img_data in datos_a_guardar])
            ruta_excel = os.path.join(self.ruta_carpeta, nombre_archivo_excel)
            
            print(f"{Fore.YELLOW}Guardando datos en Excel...{Style.RESET_ALL}")
            df.to_excel(ruta_excel, index=False)
            print(f"{Fore.GREEN}Los datos han sido guardados en el archivo {ruta_excel}{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}Los datos no han sido guardados.{Style.RESET_ALL}")