import os
from flask import Flask
from flask_cors import CORS

def create_app():
    """Create and configure Flask application using app factory pattern"""
    app = Flask(__name__)
    
    # Load configuration
    from config import get_config
    app.config.from_object(get_config())
    
    # Setup CORS
    CORS(app, resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}})
    
    # Ensure upload folder exists
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    
    # Initialize services
    from app.services.ml.model_loader import ModelService
    model_service = ModelService(app.config["MODEL_PATH"], app.config["MODEL_DEVICE"])
    
    # Register blueprints
    from app.routes.api import api_bp
    app.register_blueprint(api_bp, url_prefix="/api")
    
    # Health check endpoint
    @app.route("/health")
    def health_check():
        return {"status": "healthy", "model_loaded": model_service.is_loaded()}
    
    return app
