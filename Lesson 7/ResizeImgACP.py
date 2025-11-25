import cv2

image_path = "image.png"
img = cv2.imread(image_path)

small = cv2.resize(img, (200, 200))
medium = cv2.resize(img, (400, 400))
large = cv2.resize(img, (600, 600))

cv2.imshow("Small 200x200", small)
cv2.imshow("Medium 400x400", medium)
cv2.imshow("Large 600x600", large)

cv2.imwrite("input_image_small.jpg", small)
cv2.imwrite("input_image_medium.jpg", medium)
cv2.imwrite("input_image_large.jpg", large)

cv2.waitKey(0)
cv2.destroyAllWindows()
