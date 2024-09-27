from PIL import Image
import pytesseract
import re

def lectorImagen(nombre_archivo):
    try:
        # Actualiza la ruta al ejecutable de Tesseract
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        
        # Abre la imagen
        image = Image.open(nombre_archivo)

        # Preprocesamiento de la imagen (opcional)
        # Convertir a escala de grises y aplicar binarización
        image = image.convert('L')
        threshold = 130
        image = image.point(lambda p: p > threshold and 255)
        
        # Guardar imagen preprocesada (opcional, para verificar)
        # image.save('preprocessed_image.png')
        
        # Extrae el texto de la imagen
        texto = pytesseract.image_to_string(image, lang='eng')
        
        # Imprime el texto extraído
        print("Texto extraído de la imagen:")
        print(texto)
        
        # Procesa el texto para extraer latitud, longitud y fecha/hora
        lat = None
        lon = None
        fecha_hora = None
        
        # Expresiones regulares ajustadas con opciones flexibles
        lat_pattern = r'Lat[:\s]*([-+]?\d+[\.,]?\d*)[°]?'
        lon_pattern = r'Long[:\s]*([-+]?\d+[\.,]?\d*)[°]?'
        fecha_hora_pattern = r'(\d{1,2}/\d{1,2}/\d{2,4}\s+\d{1,2}:\d{2}\s+[ap]\. m\.)'

        # Reemplazar comas por puntos en números decimales si es necesario
        texto = texto.replace(',', '.')

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

# Ejemplo de uso:
latitud, longitud, fecha_hora = lectorImagen('image3.jpg')
print(f"Latitud: {latitud}")
print(f"Longitud: {longitud}")
print(f"Fecha y hora: {fecha_hora}")
