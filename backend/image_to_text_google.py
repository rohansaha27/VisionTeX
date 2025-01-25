import requests
import json
import base64
from image_to_text import preprocess_image
from dotenv import load_dotenv
import os


def detect_document_with_api_key(image_path):
    url = f"https://vision.googleapis.com/v1/images:annotate?key={os.getenv("GOOGLE_API_KEY")}"

  

    with open(image_path, "rb") as image_file:
        content = image_file.read()

    # Base64 encode the image content
    encoded_image = base64.b64encode(content).decode("UTF-8")

    # Prepare the request payload
    request_payload = {
        "requests": [
            {
                "image": {
                    "content": encoded_image
                },
                "features": [
                    {
                        "type": "DOCUMENT_TEXT_DETECTION"
                    }
                ],
                "imageContext": {
                "languageHints": ["en"]  # Specify English as the primary language
            }
            }
        ]
    }

    response = requests.post(url, json=request_payload)

    if response.status_code == 200:
        result = response.json()
        # Extract the full text from the response
        full_text = result["responses"][0].get("fullTextAnnotation", {}).get("text", "")
        print("Extracted Text:")
        print(full_text)
        
        return full_text
    else:
        print(f"Error: {response.status_code}, {response.text}")

# Example usage
if __name__ == '__main__':
    image_path = 'sample.jpg'  # Replace with your image path
    detect_document_with_api_key(image_path)



# import requests
# import json
# import base64
# import cv2
# from image_to_text import preprocess_image  # Import your preprocessing function

# API_KEY = "AIzaSyCyagZBg8Us5ohOByHS7LPsSssTgMsZb7A"

# def detect_document_with_api_key(image_path):
#     url = f"https://vision.googleapis.com/v1/images:annotate?key={API_KEY}"

#     # Preprocess the image
#     preprocessed_image = preprocess_image(image_path)

#     # Convert the preprocessed image to binary format
#     _, encoded_image = cv2.imencode('.jpg', preprocessed_image)
#     image_bytes = encoded_image.tobytes()

#     # Base64 encode the preprocessed image
#     base64_image = base64.b64encode(image_bytes).decode('UTF-8')

#     # Prepare the request payload
#     request_payload = {
#         "requests": [
#             {
#                 "image": {
#                     "content": base64_image
#                 },
#                 "features": [
#                     {
#                         "type": "DOCUMENT_TEXT_DETECTION"
#                     }
#                 ],
#                 "imageContext": {
#                     "languageHints": ["en"]  # Specify English as the primary language
#                 }
#             }
#         ]
#     }

#     # Send the request to the Vision API
#     response = requests.post(url, json=request_payload)

#     if response.status_code == 200:
#         result = response.json()
#         # Extract the full text from the response
#         full_text = result["responses"][0].get("fullTextAnnotation", {}).get("text", "")
#         print("Extracted Text:")
#         print(full_text)
#     else:
#         print(f"Error: {response.status_code}, {response.text}")

# # Example usage
# image_path = 'sample.jpg'  # Replace with your image path
# detect_document_with_api_key(image_path)
