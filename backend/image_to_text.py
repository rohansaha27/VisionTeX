import cv2
import pytesseract
import numpy as np

# Function to convert an image to text using Tesseract
def convert_image_to_text(image_path):
    try:
        # Step 1: Read the image using OpenCV
        image = cv2.imread(image_path)

        # Step 2: Preprocess the image for better OCR accuracy
        # Convert the image to grayscale (helps in reducing complexity)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply GaussianBlur to remove noise and smooth the image
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Apply adaptive thresholding for better contrast
        thresholded = cv2.adaptiveThreshold(blurred, 255, 
                                            cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                            cv2.THRESH_BINARY, 
                                            11, 2)

        # Optional: Perform dilation and erosion to close gaps in text
        kernel = np.ones((1, 1), np.uint8)
        dilated = cv2.dilate(thresholded, kernel, iterations=1)

        # Step 3: Extract text using Tesseract
        custom_config = r'--oem 3 --psm 6'  # OCR Engine Mode 3 and Page Segmentation Mode 6
        text = pytesseract.image_to_string(dilated, config=custom_config)

        return text
    except Exception as e:
        print(f"Error: {e}")
        return None

# Example usage
image_path = 'sample.jpeg'  # Replace with your image path
text = convert_image_to_text(image_path)

if text:
    print("Extracted Text:", text)
else:
    print("No text extracted")
