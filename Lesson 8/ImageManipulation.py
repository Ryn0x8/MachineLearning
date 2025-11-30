import cv2
import numpy as np
import matplotlib.pyplot as plt

image = cv2.imread("image.png")

gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
plt.imshow(gray_image, cmap="gray")
plt.title("Grayscale Image")
plt.show()

cropped_image = image[100:300, 200:400]
cropped_rgb = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB)
plt.imshow(cropped_rgb)
plt.title("CROPPED RGB Image")
plt.show()

image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
(h, w)  = image.shape[:2]
c = (w//2, h//2)
M = cv2.getRotationMatrix2D(c, 45, 1.0)
rotated = cv2.warpAffine(image, M, (w,h))

rotated_rgb = cv2.cvtColor(rotated, cv2.COLOR_BGR2RGB)
plt.imshow(rotated_rgb)
plt.title("ROTATED RGB")
plt.show()

brightness_matrix = np.ones(image.shape, dtype="uint8") * 50
brighter = cv2.add(image, brightness_matrix)
brigher_rgb = cv2.cvtColor(brighter, cv2.COLOR_BGR2RGB)
plt.imshow(brighter)
plt.title("Brighter RGB IMAGE")
plt.show()
