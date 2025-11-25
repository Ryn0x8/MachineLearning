import cv2

image = cv2.imread('image.png')

cv2.namedWindow('Resized Image', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Resized Image', 800, 600)
cv2.imshow('Resized Image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()

print(f"Image dimensions: {image.shape}")