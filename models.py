from dataclasses import dataclass

@dataclass
class ImageData:
    """Clase para almacenar los datos extraídos de una imagen."""
    archivo: str
    latitud: str = ''
    longitud: str = ''
    fecha: str = ''
    hora: str = ''