import os
import pandas as pd
from colorama import Fore, Style

class ExcelExporter:
    def __init__(self, ruta_carpeta):
        self.ruta_carpeta = ruta_carpeta

    def exportar_a_excel(self, datos):
        if not datos:
            print(f"{Fore.RED}No se encontraron datos para guardar en el Excel.{Style.RESET_ALL}")
            return

        respuesta = input(f"\n{Fore.CYAN}¿Desea guardar los datos en un archivo Excel? (s/n): {Style.RESET_ALL}").lower()
        
        if respuesta == 's':
            nombre_archivo = input(f"{Fore.CYAN}Por favor, ingrese el nombre del archivo Excel (sin extensión): {Style.RESET_ALL}")
            nombre_archivo_excel = f"{nombre_archivo}.xlsx"
            
            df = pd.DataFrame([vars(img_data) for img_data in datos])
            ruta_excel = os.path.join(self.ruta_carpeta, nombre_archivo_excel)
            
            print(f"{Fore.YELLOW}Guardando datos en Excel...{Style.RESET_ALL}")
            df.to_excel(ruta_excel, index=False)
            print(f"{Fore.GREEN}Los datos han sido guardados en el archivo {ruta_excel}{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}Los datos no han sido guardados.{Style.RESET_ALL}")