import requests
import subprocess
from image_to_text_google import detect_document_with_api_key
import os 
from dotenv import load_dotenv

# Define API keys

# Function to send the extracted text to Cohere API and get LaTeX formatted text
def generate_latex_from_text(text):
    url = "https://api.cohere.ai/generate"
    
    headers = {
        "Authorization": f"Bearer {os.getenv("COHERE_API_KEY")}",
        "Content-Type": "application/json"
    }

    prompt = f"""
    The following text may contain mathematical proofs, equations, and expressions. Convert it to LaTeX code:
    \n\n{text}\n\n
    """

    data = {
        "model": "medium",  # Choose the model you want to use (e.g., "xlarge")
        "prompt": prompt,
        "max_tokens": 128,
        "temperature": 0.7
    }

    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 200:
        return response.json()['text']
    else:
        return "Error: Unable to process the text"
    


# # Function to convert LaTeX to PDF
# def latex_to_pdf(latex_code, output_pdf_path):
#     # Save LaTeX code to a .tex file
#     print(latex_code)
#     with open("temp.tex", "w") as f:
#         f.write(latex_code)
    
#     # Run pdflatex to generate the PDF
#     subprocess.run(["pdflatex", "temp.tex"])
    
#     # Move the generated PDF to the desired location
#     subprocess.run(["mv", "temp.pdf", output_pdf_path])

# # Main function to process the image
# def generate_latex_from_image(image_path, output_pdf_path):
#     # Step 1: Extract text from the image
#     #text = detect_document_with_api_key(image_path)
#     text = "Bla bla bla x = 2"
    
#     # Step 2: Send the extracted text to Cohere to get LaTeX formatted text
#     latex_code = generate_latex_from_text(text)
    
#     # Step 3: Convert the LaTeX code to PDF
#     latex_to_pdf(latex_code, output_pdf_path)

#     print(f"PDF generated: {output_pdf_path}")

# # Example usage
# image_path = "sample.jpg"
# output_pdf_path = "output.pdf"
# generate_latex_from_image(image_path, output_pdf_path)
