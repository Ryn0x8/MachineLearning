import cv2
import matplotlib.pyplot as plt

image = cv2.imread("image.png")

image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

h, w, _ = image_rgb.shape

rect1_h, rect1_w = 150, 150
top_left1 = (20,20)
bottom_right1 = (top_left1[0] + rect1_w, top_left1[1] + rect1_h)
cv2.rectangle(image_rgb, top_left1, bottom_right1, (0,255,255), 3)

rect2_h, rect2_w = 150, 200
top_left2 = (w - rect2_w - 20, h - rect2_h - 20)
bottom_right2 = (top_left2[0] + rect2_w, top_left2[1] + rect2_h)
cv2.rectangle(image_rgb, top_left2, bottom_right2, (255,0,255), 3)

c1_x = top_left1[0] + rect1_w // 2
c1_y = top_left1[1] + rect1_h // 2
c2_x = top_left2[0] + rect2_w // 2
c2_y = top_left2[1] + rect2_h // 2
cv2.circle(image_rgb, (c1_x, c1_y), 15, (0,255,0), -1)
cv2.circle(image_rgb, (c2_x, c2_y), 15, (255,0,0), -1)

cv2.line(image_rgb, (c1_x, c1_y), (c2_x, c2_y), (0,255,0), 3)

font = cv2.FONT_HERSHEY_SIMPLEX
cv2.putText(image_rgb, "Region 1", (top_left1[0], top_left1[1]-10), font, 0.7, (0, 255,255, ), 2, cv2.LINE_AA)
cv2.putText(image_rgb, "Region 2", (top_left2[0], top_left2[1]-10), font, 0.7, (255,0, 255), 2, cv2.LINE_AA)
cv2.putText(image_rgb, "Center 1", (c1_x-40, c1_y+40), font, 0.6, (0,255, 0), 2, cv2.LINE_AA)
cv2.putText(image_rgb, "Center 2", (c2_x-40, c2_y+40), font, 0.6, (0, 0,255), 2, cv2.LINE_AA)

arrow_st = (w-100, 20)
arrow_ed = (w-100, h-20)

cv2.arrowedLine(image_rgb, arrow_st, arrow_ed, (255, 255, 0), 3, tipLength=0.05)
cv2.arrowedLine(image_rgb, arrow_ed,arrow_st,(255, 255, 0), 3, tipLength=0.05)

height_label_position = (arrow_st[0] - 150, (arrow_st[1] + arrow_ed[1])//2)
cv2.putText(image_rgb, f"Height: {h}px", height_label_position, font, 1, (255,255, 0), 2, cv2.LINE_AA)

plt.figure(figsize=(12, 8))
plt.imshow(image_rgb)
plt.title("Annotation")
plt.axis("off")
plt.show()

