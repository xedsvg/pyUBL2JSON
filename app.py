import json
from flask import Flask, request, jsonify
import xmltodict
import os
import logging
from werkzeug.utils import secure_filename
from waitress import serve
from src.config import Config
from src.routes import api
from src.utils import setup_logging
from src.rate_limiter import limiter

def create_app():
    app = Flask(__name__)
    
    # Configure app
    app.config.from_object(Config)
    
    # Initialize extensions
    Config.init_app()
    limiter.init_app(app)
    
    # Register blueprints
    app.register_blueprint(api)
    
    return app

if __name__ == '__main__':
    setup_logging()
    app = create_app()
    serve(app, host=Config.HOST, port=Config.PORT)
