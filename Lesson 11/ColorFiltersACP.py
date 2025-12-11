import cv2
import numpy as np
import os

red_adj = 0
green_adj = 0
blue_adj = 0
tint_mode = "none"

def apply_adjustments(image):
    global red_adj, green_adj, blue_adj, tint_mode
    output = image.copy()

    if tint_mode == "red":
        output[:, :, 0] = 0
        output[:, :, 1] = 0
    elif tint_mode == "green":
        output[:, :, 0] = 0
        output[:, :, 2] = 0
    elif tint_mode == "blue":
        output[:, :, 1] = 0
        output[:, :, 2] = 0

    output[:, :, 2] = cv2.add(output[:, :, 2], red_adj)
    output[:, :, 1] = cv2.add(output[:, :, 1], green_adj)
    output[:, :, 0] = cv2.add(output[:, :, 0], blue_adj)

    return output

image_path = "image.png"
image = cv2.imread(image_path)

if image is None:
    print("Error: image not found")
    exit()

image = cv2.resize(image, (1200, 800))

print("\nControls:")
print(" r - Red Tint")
print(" g - Green Tint")
print(" b - Blue Tint")
print(" o - Remove Tint")
print(" i - Increase Red")
print(" k - Decrease Red")
print(" w - Increase Green")
print(" a - Decrease Green")
print(" l - Increase Blue")
print(" d - Decrease Blue")
print(" s - Save Image")
print(" q - Quit\n")

while True:
    filtered = apply_adjustments(image)
    cv2.imshow("Filtered Image", filtered)

    key = cv2.waitKey(0)

    if key == ord('o'):
        tint_mode = "none"
    elif key == ord('r'):
        tint_mode = "red"
    elif key == ord('g'):
        tint_mode = "green"
    elif key == ord('b'):
        tint_mode = "blue"
    elif key == ord('i'):
        red_adj += 10
    elif key == ord('k'):
        red_adj -= 10
    elif key == ord("w"):
        green_adj += 10
    elif key == ord("a"):
        green_adj -= 10
    elif key == ord('l'):
        blue_adj += 10
    elif key == ord('d'):
        blue_adj -= 10
    elif key == ord('s'):
        filename = input("Enter filename: ")
        filename = "".join(c for c in filename if c.isalnum() or c in ['_', '-'])
        if filename == "":
            filename = "output"
        if not os.path.exists("images"):
            os.makedirs("images")
        cv2.imwrite(f"images/{filename}.png", filtered)
        print(f"Saved as images/{filename}.png")
    elif key == ord('q'):
        break

cv2.destroyAllWindows()
