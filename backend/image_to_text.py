import cv2
import pytesseract
import numpy as np
import matplotlib.pyplot as plt

# Load image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def remove_noise(image):
    return cv2.medianBlur(image, 5)

def adaptive_threshold(image):
    return cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

def dilate(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.dilate(image, kernel, iterations=1)

def erode(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.erode(image, kernel, iterations=1)

def opening(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

def deskew(image):
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated

def preprocess_image(image_path):
    img = cv2.imread(image_path)
    
    gray = get_grayscale(img)
    noise_removed = remove_noise(gray)
    thresholded = adaptive_threshold(noise_removed)
    dilated = dilate(thresholded)
    eroded = erode(dilated)
    opened = opening(eroded)
    
    # Resize for better recognition if necessary
    height, width = opened.shape[:2]
    new_width = 1000
    new_height = int((new_width / width) * height)
    opened_resized = cv2.resize(opened, (new_width, new_height))
    
    return opened_resized

def extract_text(image_path):
    preprocessed_image = preprocess_image(image_path)
    
    # Display the preprocessed image to check
    show_image(preprocessed_image)
    
    # Extract text using Tesseract
    custom_config = r'--oem 3 --psm 6'  # OCR Engine Mode 3 and Page Segmentation Mode 6
    text = pytesseract.image_to_string(preprocessed_image, config=custom_config)
    return text

def show_image(image):
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.show()

