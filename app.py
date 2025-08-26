# app.py
import os
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import tempfile

# Import your converter functions
from converters.pdf_to_word import convert_pdf_to_word
from converters.image_converter import convert_jpg_to_png, convert_png_to_jpg
# ... import other converter functions as you create API endpoints for them

app = Flask(__name__)
CORS(app) # This allows your Blogger site to communicate with this API

# --- API Endpoint for PDF to Word ---
@app.route('/convert/pdf-to-word', methods=['POST'])
def handle_pdf_to_word():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and file.filename.lower().endswith('.pdf'):
        try:
            # Create temporary files to handle the conversion
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
                file.save(temp_pdf.name)
                temp_pdf_path = temp_pdf.name
            
            temp_word_path = tempfile.mktemp(suffix=".docx")

            # Call your conversion function
            success = convert_pdf_to_word(temp_pdf_path, temp_word_path)

            if success:
                return send_file(
                    temp_word_path,
                    as_attachment=True,
                    download_name=os.path.basename(file.filename).replace('.pdf', '.docx')
                )
            else:
                return jsonify({"error": "Conversion failed on the server."}), 500

        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            # Clean up temporary files
            if os.path.exists(temp_pdf_path):
                os.remove(temp_pdf_path)
            if os.path.exists(temp_word_path):
                os.remove(temp_word_path)
    else:
        return jsonify({"error": "Invalid file type. Please upload a PDF."}), 400


# --- API Endpoint for JPG to PNG ---
@app.route('/convert/jpg-to-png', methods=['POST'])
def handle_jpg_to_png():
    # This follows the same pattern as the function above
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file and file.filename.lower().endswith('.jpg') or file.filename.lower().endswith('.jpeg'):
        # Use temporary files, call your converter, and send the result
        # ... (Implementation is similar to the pdf-to-word handler)
        # You can build this out for each of your tools
        pass # Placeholder
    else:
        return jsonify({"error": "Invalid file type. Please upload a JPG."}), 400


if __name__ == '__main__':
    app.run(debug=True)
