import cv2
import numpy as np

def apply_color_filter(image, filter_type):
    filtered_image  = image.copy()

    if filter_type == "original":
        return filtered_image
    
    elif filter_type == "red_tint":
        filtered_image[:,:,0] = 0
        filtered_image[:,:,1] = 0
    
    elif filter_type == "blue_tint":
        filtered_image[:,:,1] = 0
        filtered_image[:,:,2] = 0
    
    elif filter_type == "green_tint":
        filtered_image[:,:,0] = 0
        filtered_image[:,:,2] = 0
        
    elif filter_type == "red_increase":
        filtered_image[:,:,2] = cv2.add(filtered_image[:,:,2], 50)
    
    elif filter_type == "blue_decrease":
        filtered_image[:,:,0] = cv2.subtract(filtered_image[:,:,0], 50)
        
    return filtered_image

image_path  = "image.png"
image = cv2.imread(image_path)

if image is None:
    print("Error: Image not found")
    exit()

image = cv2.resize(image, (1200, 800))
filter_type = "original"
print("Press the following keys to apply color filters:")
print("o: Original")
print("r: Red Tint")
print("b: Blue Tint")
print("g: Green Tint")
print("i: Increase Red")
print("d: Decrease Blue")   
print("q: Quit")
while True:
    filtered_image = apply_color_filter(image, filter_type)
    cv2.imshow("Filtered Image", filtered_image)
    key = cv2.waitKey(0) & 0xFF
    if key == ord("o"):
        filter_type = "original"
    elif key == ord("r"):
        filter_type = "red_tint"
    elif key == ord("b"):
        filter_type = "blue_tint"
    elif key == ord("g"):
        filter_type = "green_tint"
    elif key == ord("i"):
        filter_type = "red_increase"
    elif key == ord("d"):
        filter_type = "blue_decrease"
    elif key == ord("q"):
        print("Exitting....")
        break
    else:
        print("Invalid key! Please use o, r, b, g, i, d, or q key")
    
cv2.destroyAllWindows()
