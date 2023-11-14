import cv2
import urllib.request
import numpy as np

url = 'http://192.168.18.15:4747/video'

cap = cv2.VideoCapture(url)

while True:
    ret, frame = cap.read()
    cv2.imshow('Camera Feed', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
