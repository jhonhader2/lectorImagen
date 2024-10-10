import os
from colorama import init, Fore, Style
from image_processor import ImageBatchProcessor
from excel_exporter import ExcelExporter

init(autoreset=True)

def obtener_ruta_valida():
    while True:
        ruta = input("Por favor, ingrese la ruta de la carpeta que contiene las imágenes: ").strip()
        if os.path.isdir(ruta):
            return ruta
        else:
            print(f"{Fore.RED}La ruta ingresada no es válida o no existe. Por favor, intente de nuevo.{Style.RESET_ALL}")

def main():
    ruta_carpeta = obtener_ruta_valida()
    
    batch_processor = ImageBatchProcessor(ruta_carpeta)
    batch_processor.procesar_imagenes()

    excel_exporter = ExcelExporter(ruta_carpeta)
    excel_exporter.solicitar_exportacion(batch_processor.datos_imagenes)

    print(f"{Fore.GREEN}Proceso completado.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()