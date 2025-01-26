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

    try:
        # Save LaTeX code to a .tex file
        with open("temp.tex", "w") as f:
            f.write(complete_latex_code)

        # Run pdflatex to generate the PDF
        subprocess.run(["pdflatex", "-interaction=nonstopmode", "temp.tex"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Move the generated PDF to the desired location
        os.replace("temp.pdf", output_pdf_path)

    except subprocess.CalledProcessError as e:
        # If there is a LaTeX error, handle it gracefully
        error_message = """
        \\documentclass{article}
        \\usepackage{amsmath}
        \\begin{document}
        There was a syntax error in the LaTeX code. Please try submitting your file again.
        \\end{document}
        """
        with open("temp.tex", "w") as f:
            f.write(error_message)
        try:
            # Generate an error message PDF
            subprocess.run(["pdflatex", "-interaction=nonstopmode", "temp.tex"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            os.replace("temp.pdf", output_pdf_path)
        except subprocess.CalledProcessError:
            # If the error PDF generation fails, log the issue (optional)
            print("Failed to generate error message PDF.")
            return False

    except Exception as general_error:
        # Log unexpected exceptions
        print(f"An unexpected error occurred: {general_error}")
        return False

    finally:
        # Clean up temporary files
        for temp_file in ["temp.tex", "temp.log", "temp.aux"]:
            if os.path.exists(temp_file):
                os.remove(temp_file)

    return True



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