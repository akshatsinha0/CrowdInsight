import os
import uuid
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
import numpy as np
import base64
import cv2

from app.services.ml.model_loader import ModelService
from app.services.ml.inference import predict_count
from app.services.crowd_analysis import CrowdAnalyzer

api_bp = Blueprint("api", __name__)
crowd_analyzer = CrowdAnalyzer()

def allowed_file(filename):
    """Check if uploaded file has allowed extension"""
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@api_bp.route("/analyze", methods=["POST"])
def analyze_image():
    """Endpoint to analyze crowd in uploaded image"""
    # Check if image was uploaded
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400
        
    file = request.files["image"]
    
    # Check if file is empty
    if file.filename == "":
        return jsonify({"error": "Empty file"}), 400
        
    # Check if file type is allowed
    if not allowed_file(file.filename):
        return jsonify({"error": "File type not allowed. Use JPG, JPEG or PNG"}), 400
    
    # Generate unique filename and save
    filename = secure_filename(file.filename)
    unique_filename = f"{uuid.uuid4()}_{filename}"
    file_path = os.path.join(current_app.config["UPLOAD_FOLDER"], unique_filename)
    file.save(file_path)
    
    try:
        # Get ML model instance
        model_service = ModelService.get_instance()
        
        # Get crowd count and density map
        count, density_map = predict_count(model_service.model, file_path)
        
        # Analyze crowd behavior
        analysis_result = crowd_analyzer.analyze_crowd(density_map)
        
        # Generate visualization
        visualization = create_visualization(file_path, density_map)
        
        return jsonify({
            "success": True,
            "count": int(count),
            "analysis": analysis_result,
            "visualization": visualization
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        # Clean up temporary file
        if os.path.exists(file_path):
            os.remove(file_path)

def create_visualization(image_path, density_map):
    """Create heatmap overlay on original image"""
    # Read original image
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Resize density map to match image
    h, w = image.shape[:2]
    density_resized = cv2.resize(density_map, (w, h))
    
    # Normalize density map for visualization
    if density_resized.max() > 0:
        density_normalized = density_resized / density_resized.max()
    else:
        density_normalized = density_resized
    
    # Apply heatmap colormap
    density_heatmap = cv2.applyColorMap((density_normalized * 255).astype(np.uint8), cv2.COLORMAP_JET)
    
    # Blend original image with heatmap
    alpha = 0.6
    overlay = cv2.addWeighted(image, 1-alpha, density_heatmap, alpha, 0)
    
    # Encode as base64 for JSON response
    _, buffer = cv2.imencode(".jpg", overlay)
    jpg_as_text = base64.b64encode(buffer).decode()
    
    return jpg_as_text
