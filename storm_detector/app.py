import cv2
import requests
import numpy as np
from PIL import Image
from io import BytesIO

# URL de la imagen
url = "https://www2.contingencias.mendoza.gov.ar/radar/latest.gif"

# Obtener el contenido de la imagen
response = requests.get(url)
response.raise_for_status()

# Convertir el contenido a una matriz NumPy usando OpenCV
image_array = np.asarray(bytearray(response.content), dtype=np.uint8)

# Convertir la imagen a formato RGB usando Pillow
image_pillow = Image.open(BytesIO(response.content)).convert("RGB")

# Convertir la imagen a un espacio de color adecuado (BGR en este caso)
image_bgr = cv2.cvtColor(np.array(image_pillow), cv2.COLOR_RGB2BGR)

# Verificar si la decodificación fue exitosa y la imagen tiene dimensiones válidas
if image_bgr is not None and image_bgr.shape[0] > 0 and image_bgr.shape[1] > 0:
    # Mostrar la imagen con OpenCV
    cv2.imshow("Imagen del Radar", image_bgr)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("Error al decodificar la imagen o dimensiones inválidas.")
