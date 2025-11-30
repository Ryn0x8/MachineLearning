import cv2
import numpy as np
import matplotlib.pyplot as plt

def display_image(title, image):
    plt.figure(figsize=(8,8))
    if len(image.shape) == 2:
        plt.imshow(image, cmap="gray")
    else:
        plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    plt.axis("off")
    plt.title(title)
    plt.show()

def interactive_edge_detection(path):
    image = cv2.imread(path)
    if image is None:
        print("Error: Image is not found")
        return
    
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    display_image("Original Gray Image", gray_image)


    print("Select an option:")
    print("1. Sobel Edge Detection")
    print("2. Canny Edge Detection")
    print("3. Laplacian Edge Detection")
    print("4. Gaussian Smoothing")
    print("5. Median Filtering")
    print("6. Exit")

    while True:
        choice = int(input("Enter your choice (1-6): "))

        if choice == 1:
            sobelx = cv2.Sobel(gray_image, cv2.CV_64F, 1,0, ksize=3)
            sobely = cv2.Sobel(gray_image, cv2.CV_64F, 0,1, ksize=3)
            combined_sobel = cv2.bitwise_or(sobelx.astype(np.uint8), sobely.astype(np.uint8))
            display_image("Sobel edge detection", combined_sobel)

        elif choice == 2:
            print("Adjust threshold for the canny (default: 100 and 200)")
            lower_thres = int(input("Enter the lower threshold: "))
            upper_thres = int(input("Enter the upper threshold: "))
            edges = cv2.Canny(gray_image, lower_thres, upper_thres)
            display_image("Canny edge detection", edges)

        elif choice == 3:
            laplacian = cv2.Laplacian(gray_image, cv2.CV_64F)
            display_image("Laplacian Edge Detection", np.abs(laplacian).astype(np.uint8))

        elif choice == 4:
            print("Adjust the kernel size for the Gussian Blur (Odd Default: 5)")
            kernel_size = int(input("Enter the kernel size (Must be odd): "))
            blurred = cv2.GaussianBlur(gray_image, (kernel_size, kernel_size), 0)
            display_image("Gussian Smoothed Image", blurred)

        elif choice == 5:
            print("Adjust the kernel size for the Median Filtering (Odd Default: 5)")
            kernel_size = int(input("Enter the kernel size (Must be odd): "))
            median_filtered = cv2.medianBlur(gray_image, kernel_size)
            display_image("Median Filtered Image", median_filtered)
        
        elif choice == 6:
            print("Exiting.....")
            break

        else:
            print("Invalid choice. Please make a choice between 1 to 6")


interactive_edge_detection("image.png")
        


