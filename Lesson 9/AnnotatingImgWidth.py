import cv2
import matplotlib.pyplot as plt

image = cv2.imread("image.png")

image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

h, w, _ = image_rgb.shape
arrow_st = (20, h-30)
arrow_ed = (w-20, h- 30)

cv2.arrowedLine(image_rgb, arrow_st, arrow_ed, (255, 255, 0), 3, tipLength=0.05)
cv2.arrowedLine(image_rgb, arrow_ed,arrow_st,(255, 255, 0), 3, tipLength=0.05)

font = cv2.FONT_HERSHEY_SIMPLEX

height_label_position = (arrow_st[0] - 20, (arrow_st[1] + arrow_ed[1])//2)
cv2.putText(image_rgb, f"Width: {w}px", height_label_position, font, 1, (255,255, 0), 2, cv2.LINE_AA)

plt.figure(figsize=(12, 8))
plt.imshow(image_rgb)
plt.title("Annotation")
plt.axis("off")
plt.show()