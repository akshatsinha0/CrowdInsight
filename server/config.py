import os
from pathlib import Path

class Config:
    """Base configuration"""
    # Flask settings
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-key-change-in-production")
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "temp_uploads")
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload
    
    # Project paths
    BASE_DIR = Path(__file__).resolve().parent
    MODEL_DIR = os.path.join(BASE_DIR.parent, "models")
    
    # ML model settings
    MODEL_PATH = os.path.join(MODEL_DIR, "csrnet_crowd_v1.pth")
    MODEL_DEVICE = "cuda" if os.environ.get("USE_GPU", "0") == "1" else "cpu"
    
    # Redis for task queue
    REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
    
    # CORS settings
    CORS_ORIGINS = [
        "http://localhost:5173",  # Vue dev server
        "http://localhost:8080"   # Optional alternate port
    ]

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False
    
class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = False
    TESTING = True
    
class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    
    # Override with stronger secret key
    SECRET_KEY = os.environ.get("SECRET_KEY")
    
    # Allow frontend domains (should be set in environment)
    CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "").split(",")

# Configuration dictionary
config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig
}

# Get current configuration
def get_config():
    env = os.environ.get("FLASK_ENV", "development")
    return config_by_name.get(env, DevelopmentConfig)
