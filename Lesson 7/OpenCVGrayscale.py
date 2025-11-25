import cv2

image = cv2.imread("image.png")
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
resized_image  = cv2.resize(gray_image, (800, 600))
cv2.imshow("Grayscale Resized Image", resized_image)
key = cv2.waitKey(0)
if key == ord("s"):
    cv2.imwrite("grayscale_resized_image.png", resized_image)
    print("Image saved as grayscale_resized_image.png")
else:
    print("Image not saved.")

cv2.destroyAllWindows()
print(f"Grayscale image dimensions: {resized_image.shape}")