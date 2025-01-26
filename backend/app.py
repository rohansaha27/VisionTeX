from flask import Flask, request, jsonify, send_file
from latex_openai import generate_latex_from_image
import os
from flask_cors import CORS
import base64

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/process-image', methods=['POST'])
def process_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    # Save the uploaded file
    image_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(image_path)

    # Generate LaTeX and PDF
    output_pdf_path = os.path.join(OUTPUT_FOLDER, f"{os.path.splitext(file.filename)[0]}.pdf")
    latex_code = generate_latex_from_image(image_path, output_pdf_path)

    # Read the PDF file and encode it in base64
    with open(output_pdf_path, "rb") as pdf_file:
        encoded_pdf = base64.b64encode(pdf_file.read()).decode('utf-8')

    # Return the LaTeX code and PDF as base64
    return jsonify({
        'latexCode': latex_code,
        'pdfBase64': encoded_pdf
    })

# @app.route('/get-pdf/<filename>', methods=['GET'])
# def get_pdf(filename):
#     file_path = os.path.join(OUTPUT_FOLDER, filename)
#     if not os.path.exists(file_path):
#         return jsonify({'error': 'File not found'}), 404
#     return send_file(file_path)

if __name__ == '__main__':
    app.run(debug=True)
