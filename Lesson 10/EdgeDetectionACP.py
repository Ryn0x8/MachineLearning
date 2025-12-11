import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

def display_side_by_side(original, processed, title1="Original", title2="Processed"):
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.imshow(original, cmap="gray")
    plt.title(title1)
    plt.axis("off")
    
    plt.subplot(1, 2, 2)
    plt.imshow(processed, cmap="gray")
    plt.title(title2)
    plt.axis("off")
    
    plt.show()

def save_image(image):
    os.makedirs("output", exist_ok=True)
    filename = input("Enter filename to save (without extension): ") + ".png"
    save_path = os.path.join("output", filename)
    cv2.imwrite(save_path, image)
    print(f"Image saved as {save_path}")

def interactive_image_processing(path):
    image = cv2.imread(path)
    if image is None:
        print("Error: Image not found")
        return
    
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    display_side_by_side(gray_image, gray_image, "Original", "Original")
    
    while True:
        print("\nOptions:")
        print("1. Sobel Edge Detection")
        print("2. Canny Edge Detection")
        print("3. Laplacian Edge Detection")
        print("4. Gaussian Smoothing")
        print("5. Median Filtering")
        print("6. Save Processed Image")
        print("7. Exit")
        
        choice = input("Enter your choice (1-7): ")
        
        if choice == "1":
            sobelx = cv2.Sobel(gray_image, cv2.CV_64F, 1, 0, ksize=3)
            sobely = cv2.Sobel(gray_image, cv2.CV_64F, 0, 1, ksize=3)
            processed = cv2.bitwise_or(sobelx.astype(np.uint8), sobely.astype(np.uint8))
            display_side_by_side(gray_image, processed, "Original", "Sobel Edge Detection")
        
        elif choice == "2":
            lower = int(input("Enter lower threshold for Canny: "))
            upper = int(input("Enter upper threshold for Canny: "))
            processed = cv2.Canny(gray_image, lower, upper)
            display_side_by_side(gray_image, processed, "Original", "Canny Edge Detection")
        
        elif choice == "3":
            laplacian = cv2.Laplacian(gray_image, cv2.CV_64F)
            processed = np.abs(laplacian).astype(np.uint8)
            display_side_by_side(gray_image, processed, "Original", "Laplacian Edge Detection")
        
        elif choice == "4":
            k = int(input("Enter odd kernel size for Gaussian blur: "))
            processed = cv2.GaussianBlur(gray_image, (k, k), 0)
            display_side_by_side(gray_image, processed, "Original", "Gaussian Blur")
        
        elif choice == "5":
            k = int(input("Enter odd kernel size for Median filter: "))
            processed = cv2.medianBlur(gray_image, k)
            display_side_by_side(gray_image, processed, "Original", "Median Filter")
        
        elif choice == "6":
            if 'processed' in locals():
                save_image(processed)
            else:
                print("No processed image to save yet!")
        
        elif choice == "7":
            print("Exiting...")
            break
        else:
            print("Invalid choice, try again.")

interactive_image_processing("image.png")
