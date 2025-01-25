# UBL to JSON Converter API

A Flask-based REST API that converts Universal Business Language (UBL) XML documents (E-Invoice / E-Factura) to JSON format.

## Features

- RESTful API endpoint for XML to JSON conversion
- Docker support for easy deployment
- Secure file handling
- Automatic cleanup of processed files
- Production-ready with Waitress WSGI server
- Comprehensive error handling and logging

## Quick Start with Docker

```bash
# Build and run with Docker Compose
docker-compose up --build

# The API will be available at http://localhost:8080
```

## API Endpoints

### Convert UBL to JSON
- **URL**: `/convert`
- **Method**: `POST`
- **Content-Type**: `multipart/form-data`
- **Parameter**: `file` (XML file)

Example using curl:
```bash
curl -X POST -F "file=@path/to/your/ubl.xml" http://localhost:8080/convert
```

## Development Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

## Environment Variables

- `PORT`: Server port (default: 8080)
- `FLASK_ENV`: Flask environment setting

## Directory Structure

```
.
├── app.py              # Main application file
├── Dockerfile          # Docker configuration
├── docker-compose.yml  # Docker Compose configuration
├── requirements.txt    # Python dependencies
└── uploads/           # Temporary upload directory
```

## Error Handling

The API returns appropriate HTTP status codes:
- 200: Successful conversion
- 400: Invalid request or file format
- 500: Server error

## License

MIT License