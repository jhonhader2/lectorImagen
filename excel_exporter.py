import os
import pandas as pd
from colorama import Fore, Style

class ExcelExporter:
    def __init__(self, ruta_carpeta):
        self.ruta_carpeta = ruta_carpeta

    def solicitar_exportacion(self, datos):
        if not datos:
            print(f"{Fore.RED}No se encontraron datos para guardar en el Excel.{Style.RESET_ALL}")
            return

        if self._confirmar_exportacion():
            nombre_archivo = self._solicitar_nombre_archivo()
            self._guardar_datos_excel(datos, nombre_archivo)
        else:
            print(f"{Fore.YELLOW}Los datos no han sido guardados.{Style.RESET_ALL}")

    def _confirmar_exportacion(self):
        respuesta = input(f"\n{Fore.CYAN}¿Desea guardar los datos en un archivo Excel? (s/n): {Style.RESET_ALL}").lower()
        return respuesta == 's'

    def _solicitar_nombre_archivo(self):
        nombre_archivo = input(f"{Fore.CYAN}Por favor, ingrese el nombre del archivo Excel (sin extensión): {Style.RESET_ALL}")
        return f"{nombre_archivo}.xlsx"

    def _guardar_datos_excel(self, datos, nombre_archivo):
        df = pd.DataFrame([vars(img_data) for img_data in datos])
        ruta_excel = os.path.join(self.ruta_carpeta, nombre_archivo)
        
        print(f"{Fore.YELLOW}Guardando datos en Excel...{Style.RESET_ALL}")
        df.to_excel(ruta_excel, index=False)
        print(f"{Fore.GREEN}Los datos han sido guardados en el archivo {ruta_excel}{Style.RESET_ALL}")