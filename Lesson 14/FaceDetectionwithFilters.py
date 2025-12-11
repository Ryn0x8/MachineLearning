import cv2
import numpy as np

def apply_filter(image, ftype):
    img = image.copy()
    if ftype == "red_tint":
        img[:, :, 0] = 0  
        img[:, :, 1] = 0  

    elif ftype == "green_tint":
        img[:, :, 0] = 0  
        img[:, :, 2] = 0 
    elif ftype == "blue_tint":
        img[:, :, 1] = 0  
        img[:, :, 2] = 0 

    elif ftype == "sobel":
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        sx = cv2.Sobel(gray, cv2.CV_64F, 1,0, ksize=3)
        sy = cv2.Sobel(gray, cv2.CV_64F, 0,1, ksize=3)
        sob = cv2.bitwise_or(sx.astype(np.uint8), sy.astype(np.uint8))
        img = cv2.cvtColor(sob, cv2.COLOR_GRAY2BGR)

    elif ftype == "canny":
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        canny = cv2.Canny(gray, 100, 200)
        img = cv2.cvtColor(canny, cv2.COLOR_GRAY2BGR)

    elif ftype == "cartoon":
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 5)
        edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                      cv2.THRESH_BINARY, 9, 9)
        color = cv2.bilateralFilter(img, 9, 300,300)
        img = cv2.bitwise_and(color, color, mask = edges)

    return img

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return
    
    ftype = "original"
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            return
        out = apply_filter(frame, ftype)
        cv2.imshow("Filtered Video", out)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('r'):
            ftype = "red_tint"
        elif key == ord('g'):
            ftype = "green_tint"
        elif key == ord('b'): 
            ftype = "blue_tint"
        elif key == ord('s'):
            ftype = "sobel"
        elif key == ord('c'):
            ftype = "canny"
        elif key == ord('t'):
            ftype = "cartoon"
        elif key == ord('o'):
            ftype = "original"

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()