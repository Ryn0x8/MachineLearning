import cv2
import numpy as np

img = cv2.imread("image.png")

h, w = img.shape[:2]
center = (w // 2, h // 2)
matrix = cv2.getRotationMatrix2D(center, 0, 1.0)
rotated = cv2.warpAffine(img, matrix, (w, h))

bright = cv2.convertScaleAbs(rotated, alpha=1.2, beta=30)

crop = bright[int(h*0.15):int(h*0.85), int(w*0.1):int(w*0.9)]

cv2.imwrite("final_image.png", crop)
