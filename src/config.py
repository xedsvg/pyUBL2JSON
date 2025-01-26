import os

class Config:
    UPLOAD_FOLDER = 'uploads'
    PORT = int(os.environ.get('PORT', 8080))
    HOST = '0.0.0.0'
    
    # Rate limiting configuration
    RATELIMIT_DEFAULT = os.environ.get('RATELIMIT_DEFAULT', "100 per day")
    RATELIMIT_STORAGE_URL = os.environ.get('RATELIMIT_STORAGE_URL', "memory://")
    RATELIMIT_STRATEGY = "fixed-window"
    RATELIMIT_HEADERS_ENABLED = True
    
    @classmethod
    def init_app(cls):
        os.makedirs(cls.UPLOAD_FOLDER, exist_ok=True)
