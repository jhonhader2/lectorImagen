from PIL import Image
import pytesseract
import re
import pandas as pd
import os

def lectorImagen(nombre_archivo):
    try:
        # Actualiza la ruta al ejecutable de Tesseract
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        
        # Abre la imagen
        image = Image.open(nombre_archivo)
        
        # Extrae el texto de la imagen (asegúrate de que el idioma 'spa' está disponible)
        texto = pytesseract.image_to_string(image, lang='spa')
        
        # Imprime el texto extraído
        print("Texto extraído de la imagen:")
        print(texto)
        
        # Reemplazar comas por puntos en números decimales si es necesario
        texto = texto.replace(',', '.')
        
        # Obtiene el nombre del archivo sin extensión
        nombre_sin_extension = os.path.splitext(nombre_archivo)[0]
        
        # Procesa el texto para extraer latitud, longitud y fecha/hora
        lat = None
        lon = None
        fecha_hora = None
        
        # Expresiones regulares ajustadas
        lat_pattern = r'Lat[:\s]*([-+]?\d+[\.,]?\d*)[°]?'
        lon_pattern = r'Long[:\s]*([-+]?\d+[\.,]?\d*)[°]?'
        fecha_hora_pattern = r'(\d{1,2}/\d{1,2}/\d{2,4}\s+\d{1,2}:\d{2}\s+[ap]\. m\.)'
        
        lat_match = re.search(lat_pattern, texto, re.IGNORECASE)
        lon_match = re.search(lon_pattern, texto, re.IGNORECASE)
        fecha_hora_match = re.search(fecha_hora_pattern, texto, re.IGNORECASE)
        
        if lat_match:
            lat = lat_match.group(1)
            print(f"Latitud encontrada: {lat}")
        else:
            print("No se encontró la latitud en el texto.")

        if lon_match:
            lon = lon_match.group(1)
            print(f"Longitud encontrada: {lon}")
        else:
            print("No se encontró la longitud en el texto.")

        if fecha_hora_match:
            fecha_hora = fecha_hora_match.group(1)
            print(f"Fecha y hora encontrada: {fecha_hora}")
        else:
            print("No se encontró la fecha y hora en el texto.")

        # Convierte las coordenadas a formato GMS si es necesario
        if lat and lon:
            lat_gms = decimal_a_gms(float(lat))
            lon_gms = decimal_a_gms(float(lon))
            lat = lat_gms
            lon = lon_gms

        # Guardar los datos en un archivo Excel
        guardar_en_excel(nombre_sin_extension, lat, lon, fecha_hora)

        return lat, lon, fecha_hora
    
    except FileNotFoundError:
        print("No se encontró el archivo de imagen. Verifica la ruta y el nombre del archivo.")
    except pytesseract.TesseractNotFoundError:
        print("No se encontró el ejecutable de Tesseract OCR. Verifica la ruta y la instalación.")
    except Exception as e:
        print(f"Ocurrió un error: {e}")

def decimal_a_gms(grados_decimales):
    grados = int(grados_decimales)
    minutos_decimales = abs(grados_decimales - grados) * 60
    minutos = int(minutos_decimales)
    segundos = (minutos_decimales - minutos) * 60
    return f"{grados}° {minutos}' {segundos:.2f}\""

def guardar_en_excel(nombre_archivo, latitud, longitud, fecha_hora):
    # Crear un DataFrame con los datos
    data = {
        'Nombre Archivo': [nombre_archivo],
        'Latitud': [latitud],
        'Longitud': [longitud],
        'Fecha y hora': [fecha_hora]
    }
    df = pd.DataFrame(data)
    
    # Guardar en un archivo Excel
    nombre_archivo_excel = 'datos_extraidos.xlsx'
    df.to_excel(nombre_archivo_excel, index=False)
    print(f"Los datos han sido guardados en el archivo {nombre_archivo_excel}")

# Ejemplo de uso:
latitud, longitud, fecha_hora = lectorImagen('image3.jpg')
print(f"Latitud: {latitud}")
print(f"Longitud: {longitud}")
print(f"Fecha y hora: {fecha_hora}")
