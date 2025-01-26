import os
import logging
import xmltodict
from werkzeug.utils import secure_filename

class XMLProcessor:
    @staticmethod
    def validate_xml_header(file_path):
        with open(file_path, 'r', encoding='utf-8') as xml_file:
            first_line = xml_file.readline().strip()
            return first_line.startswith('<?xml')

    @staticmethod
    def process_xml_file(file_path):
        with open(file_path, 'r', encoding='utf-8') as xml_file:
            xml_content = xml_file.read()
            # Simple XML to dict conversion without business logic
            data = xmltodict.parse(xml_content, process_namespaces=False)
            return data

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
