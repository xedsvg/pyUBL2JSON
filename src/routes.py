import os
import json
import logging
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from .invoice_parser import InvoiceParser
from .utils import XMLProcessor
from .config import Config
from .rate_limiter import limiter

api = Blueprint('api', __name__)

@api.route('/')
@limiter.exempt
def home():
    return "UBL 2.1 to JSON Converter API"

@api.route('/convert', methods=['POST'])
@limiter.limit("100 per day")
def convert_invoice():
    if 'file' not in request.files:
        logging.warning("No file uploaded")
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    if file.filename == '':
        logging.warning("No selected file")
        return jsonify({"error": "No selected file"}), 400
    
    filename = secure_filename(file.filename)
    file_path = os.path.join(Config.UPLOAD_FOLDER, filename)
    
    try:
        file.save(file_path)
        if not XMLProcessor.validate_xml_header(file_path):
            return jsonify({"error": "Invalid XML file header"}), 400
        
        json_data = XMLProcessor.process_xml_file(file_path)
        return jsonify({"success": True, "data": json_data})
    except Exception as e:
        logging.error(f"Error processing file: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

@api.route('/convert-and-parse', methods=['POST'])
@limiter.limit("100 per day")
def convert_and_parse_invoice():
    if 'file' not in request.files:
        logging.warning("No file uploaded")
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    if file.filename == '':
        logging.warning("No selected file")
        return jsonify({"error": "No selected file"}), 400
    
    filename = secure_filename(file.filename)
    file_path = os.path.join(Config.UPLOAD_FOLDER, filename)
    
    try:
        file.save(file_path)
        if not XMLProcessor.validate_xml_header(file_path):
            return jsonify({"error": "Invalid XML file header"}), 400
        
        json_data = XMLProcessor.process_xml_file(file_path)
        parsed_invoice = InvoiceParser.parse_invoice(json.dumps(json_data))
        return jsonify({"success": True, "invoice": parsed_invoice})
    except Exception as e:
        logging.error(f"Error processing file: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
