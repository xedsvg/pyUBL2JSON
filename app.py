from flask import Flask, request, jsonify
import xmltodict
import os
import logging
from werkzeug.utils import secure_filename
from waitress import serve

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return "UBL 2.1 to JSON Converter API" 

@app.route('/convert', methods=['POST'])
def convert_invoice():
    if 'file' not in request.files:
        logging.warning("No file uploaded")
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    if file.filename == '':
        logging.warning("No selected file")
        return jsonify({"error": "No selected file"}), 400
    
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as xml_file:
            first_line = xml_file.readline().strip()
            if not first_line.startswith('<?xml'):
                logging.warning("Invalid XML file header")
                return jsonify({"error": "Invalid XML file header"}), 400
            
            xml_file.seek(0)
            xml_content = xml_file.read()
            json_data = xmltodict.parse(xml_content)
            logging.info("File processed successfully")
            return jsonify({"success": True, "data": json_data})
    except xmltodict.expat.ExpatError:
        logging.error("Invalid XML format")
        return jsonify({"error": "Invalid XML format"}), 400
    except Exception as e:
        logging.error(f"Error processing file: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        os.remove(file_path)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    logging.info(f"Starting production server on port {port}...")
    serve(app, host='0.0.0.0', port=port)

