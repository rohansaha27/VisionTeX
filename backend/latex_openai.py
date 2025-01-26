import requests
import subprocess
from image_to_text_google import detect_document_with_api_key
import os
from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),  # This is the default and can be omitted
)

# Function to send the extracted text to OpenAI API and get LaTeX formatted text
def generate_latex_from_text(text):
    prompt = f"""
    This text was converted from an image to text. Please convert it to LaTeX format. Infer the proof if required. Please be utmost mindful of syntax in LateX. Remember, only give latex text, nothing else.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # You can change this to any available model you want
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": text},
            ]
        )
        print(response.choices[0].message.content)
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: Unable to process the text. Details: {str(e)}"

# Function to convert LaTeX to PDF
def latex_to_pdf(latex_code, output_pdf_path):
    # Wrap the LaTeX code in a complete LaTeX document structure
    complete_latex_code = f"""
    \\documentclass{{article}}
    \\usepackage{{amsmath}}
    \\usepackage{{amssymb}}
    \\usepackage{{amsfonts}}
    \\usepackage{{amsthm}} 
    
    \\begin{{document}}
    {latex_code}
    \\end{{document}}
    """

    # Save LaTeX code to a .tex file
    print(complete_latex_code)
    with open("temp.tex", "w") as f:
        f.write(complete_latex_code)

    
    try:
        # Run pdflatex to generate the PDF
        subprocess.run(["pdflatex", "temp.tex"], check=True)

    except subprocess.CalledProcessError:
        # If there is an error, generate a simple error message PDF
        error_message = """
        \\documentclass{article}
        \\begin{document}
        There was an error processing the LaTeX code. Please check the syntax and try again.
        \\end{document}
        """
        with open("temp.tex", "w") as f:
            f.write(error_message)
        subprocess.run(["pdflatex", "temp.tex"], check=True)

    # Move the generated PDF to the desired location
    os.replace("temp.pdf", output_pdf_path)



# Main function to process the image
def generate_latex_from_image(image_path, output_pdf_path):
    # Step 1: Extract text from the image
    text = detect_document_with_api_key(image_path)
    # text = "1. Let x be a real number.2. Assume x is greater than 0.3. Then, x + 1 is greater than 1. 4. Subtract 1 from both sides: x > 0. 5. Therefore, x is positive. 6. Thus, we have shown that if x > 0, then x is positive."

    # Step 2: Send the extracted text to OpenAI to get LaTeX formatted text
    latex_code = generate_latex_from_text(text)

    # Step 3: Convert the LaTeX code to PDF
    latex_to_pdf(latex_code, output_pdf_path)

    print(f"PDF generated: {output_pdf_path}")
    return latex_code

# # Example usage
# image_path = "sample.jpg"
# output_pdf_path = "output3.pdf"
# generate_latex_from_image(image_path, output_pdf_path)