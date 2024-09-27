from PIL import Image
import pytesseract
import re
import pandas as pd
import os
import glob

def lectorImagen(ruta_archivo):
    try:
        # Actualiza la ruta al ejecutable de Tesseract
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        
        # Obtiene el nombre del archivo sin extensión
        nombre_archivo = os.path.basename(ruta_archivo)
        nombre_sin_extension = os.path.splitext(nombre_archivo)[0]
        
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
        fecha_hora_pattern = r'(\d{1,2}/\d{1,2}/\d{2,4}\s+\d{1,2}:\d{2}\s+[ap]\. m\.)'
        
        lat_match = re.search(lat_pattern, texto, re.IGNORECASE)
        lon_match = re.search(lon_pattern, texto, re.IGNORECASE)
        fecha_hora_match = re.search(fecha_hora_pattern, texto, re.IGNORECASE)
        
        if lat_match:
            lat = lat_match.group(1)
        else:
            print(f"No se encontró la latitud en el texto de {nombre_archivo}.")
        
        if lon_match:
            lon = lon_match.group(1)
        else:
            print(f"No se encontró la longitud en el texto de {nombre_archivo}.")
        
        if fecha_hora_match:
            fecha_hora = fecha_hora_match.group(1)
            # Primero, limpiamos la cadena por si hay espacios adicionales
            fecha_hora = ' '.join(fecha_hora.split())

            # Luego, dividimos la cadena en fecha y hora
            try:
                # Dividimos por el primer espacio
                fecha_part, hora_part = fecha_hora.split(' ', 1)
                
                # fecha_part contiene la fecha
                fecha = fecha_part.strip()
                
                # hora_part contiene la hora y el indicador 'a. m.' o 'p. m.'
                hora = hora_part.strip()
                
                # Ahora, verificamos si el año es de dos dígitos y lo convertimos a cuatro dígitos
                dia, mes, anio = fecha.split('/')
                if len(anio) == 2:
                    # Puedes ajustar este código si necesitas manejar años anteriores al 2000
                    anio = '20' + anio
                    fecha = f"{dia}/{mes}/{anio}"
                
            except ValueError:
                print(f"Error al separar la fecha y hora en {nombre_archivo}")
                fecha = ''
                hora = ''
        else:
            print(f"No se encontró la fecha y hora en el texto de {nombre_archivo}.")
            fecha = ''
            hora = ''
        
        # Convierte las coordenadas a formato GMS si es necesario
        if lat and lon:
            lat_gms = decimal_a_gms(float(lat))
            lon_gms = decimal_a_gms(float(lon))
            lat = lat_gms
            lon = lon_gms
        else:
            lat = ''
            lon = ''
    
        # Retorna los datos y el nombre del archivo
        return {
            'Archivo': nombre_sin_extension,
            'Latitud': lat,
            'Longitud': lon,
            'Fecha': fecha,
            'Hora': hora
        }
        
    except FileNotFoundError:
        print(f"No se encontró el archivo de imagen {ruta_archivo}. Verifica la ruta y el nombre del archivo.")
        return None
    except pytesseract.TesseractNotFoundError:
        print("No se encontró el ejecutable de Tesseract OCR. Verifica la ruta y la instalación.")
        return None
    except Exception as e:
        print(f"Ocurrió un error procesando {ruta_archivo}: {e}")
        return None

def decimal_a_gms(grados_decimales):
    grados = int(grados_decimales)
    minutos_decimales = abs(grados_decimales - grados) * 60
    minutos = int(minutos_decimales)
    segundos = (minutos_decimales - minutos) * 60
    return f"{grados}° {minutos}' {segundos:.2f}\""

# Función principal para procesar todas las imágenes en una carpeta
def procesar_imagenes_en_carpeta(ruta_carpeta):
    # Lista para almacenar los datos extraídos de cada imagen
    datos_imagenes = []
    
    # Patrones de archivos de imagen (puedes agregar más extensiones si es necesario)
    extensiones_imagen = ('*.jpg', '*.jpeg', '*.png', '*.bmp', '*.tiff')
    
    # Recorre cada patrón de extensión
    for extension in extensiones_imagen:
        # Usa glob para obtener la lista de archivos con la extensión actual
        ruta_patron = os.path.join(ruta_carpeta, extension)
        archivos = glob.glob(ruta_patron)
        
        for ruta_archivo in archivos:
            print(f"Procesando {ruta_archivo}...")
            datos = lectorImagen(ruta_archivo)
            if datos:
                datos_imagenes.append(datos)
    
    # Crear un DataFrame con todos los datos
    df = pd.DataFrame(datos_imagenes)
    
    # Guardar en un archivo Excel
    nombre_archivo_excel = os.path.join(ruta_carpeta, 'datos_extraidos.xlsx')
    df.to_excel(nombre_archivo_excel, index=False)
    print(f"Los datos han sido guardados en el archivo {nombre_archivo_excel}")

# Ejemplo de uso:
# Especifica la ruta de la carpeta que contiene las imágenes
ruta_carpeta_imagenes = r'C:\images'

# Procesa todas las imágenes en la carpeta
procesar_imagenes_en_carpeta(ruta_carpeta_imagenes)
