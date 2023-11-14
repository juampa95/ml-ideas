import cv2
import numpy as np
import urllib.request

def calcular_inclinacion_desde_camara(url):
    # Abrir la transmisión de la cámara
    cap = cv2.VideoCapture(url, cv2.CAP_ANY)  # Usa cv2.CAP_ANY en lugar de cv2.CAP_IMAGES

    while True:
        # Capturar un fotograma
        ret, frame = cap.read()
        if not ret:
            print("Error al leer el cuadro.")
            break

        ################# -filtrado por escala grises- ###################

        # Convertir el fotograma a escala de grises para filtrado por umbral
        gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Aplicar umbral
        _, umbral = cv2.threshold(gris, 170, 255, cv2.THRESH_BINARY)

        # Aplicar suavizado para reducir el ruido
        suavizado = cv2.GaussianBlur(umbral, (5, 5), 0)

        ################# -fin filtrado por escala grises- ###################

        ################# -filtrado por colores- ###################

        # Definir los rangos de color en BGR para filtrado por colores 
        # color_objetivo = (200, 200, 200)

        # Definir los rangos de color en BGR
        # bajo = np.array([color_objetivo[0] - 20, color_objetivo[1] - 20, color_objetivo[2] - 20])
        # alto = np.array([color_objetivo[0] + 20, color_objetivo[1] + 20, color_objetivo[2] + 20])

        # Crear una máscara para el rango de color deseado
        # mascara = cv2.inRange(frame, bajo, alto)

        # Aplicar la máscara a la imagen original
        # resultado = cv2.bitwise_and(frame, frame, mask=mascara)

        # Aplicar suavizado para reducir el ruido en la imagen resultante
        # suavizado = cv2.GaussianBlur(resultado, (5, 5), 0)

        ################# -fin filtrado por colores- ###################

        # Detectar bordes con Canny
        bordes = cv2.Canny(suavizado, 50, 150)

        # Encontrar contornos en la imagen
        contornos, _ = cv2.findContours(bordes, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contorno in contornos:
            # Aproximar el contorno a un polígono
            epsilon = 0.1 * cv2.arcLength(contorno, True)
            approx = cv2.approxPolyDP(contorno, epsilon, True)
            if len(approx) == 4:
                rectangulo = cv2.minAreaRect(contorno)
                inclinacion_rectangulo = round(rectangulo[-1],2)

                inclinacion_texto = f'DEG {inclinacion_rectangulo}'
                cv2.putText(frame, inclinacion_texto, tuple(approx[0][0]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        # Dibujar los contornos en la imagen original
        cv2.drawContours(frame, contornos, -1, (0, 255, 0), 2)

        # Mostrar el fotograma con los contornos
        cv2.imshow('Contornos detectados', frame)

        # Salir si se presiona la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Liberar la captura y cerrar la ventana
    cap.release()
    cv2.destroyAllWindows()

# Reemplaza 'tu_direccion_ip' y 'puerto' con la dirección IP y puerto de tu teléfono.
url_camara = 'http://192.168.18.15:4747/video'

# Llamar a la función
calcular_inclinacion_desde_camara(url_camara)
