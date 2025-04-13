import cv2
import numpy as np
import torch
from typing import Tuple

def preprocess_image(image_path: str) -> torch.Tensor:
    """
    Preprocess image for model input
    
    Args:
        image_path: Path to image file
        
    Returns:
        Preprocessed image tensor
    """
    # Read and normalize image
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Could not read image: {image_path}")
        
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Preserve aspect ratio while resizing
    h, w = image.shape[:2]
    scale = min(1024/w, 768/h)
    new_w, new_h = int(w*scale), int(h*scale)
    image = cv2.resize(image, (new_w, new_h))
    
    # Convert to tensor and normalize
    tensor = torch.tensor(image).float() / 255.0
    tensor = tensor.permute(2, 0, 1).unsqueeze(0)  # [B, C, H, W]
    
    # Normalize with ImageNet mean/std
    mean = torch.tensor([0.485, 0.456, 0.406]).view(1, 3, 1, 1)
    std = torch.tensor([0.229, 0.224, 0.225]).view(1, 3, 1, 1)
    tensor = (tensor - mean) / std
    
    return tensor

def predict_count(model: torch.nn.Module, image_path: str) -> Tuple[float, np.ndarray]:
    """
    Predict crowd count from image
    
    Args:
        model: CSRNet model
        image_path: Path to image file
        
    Returns:
        Tuple of (count, density_map)
    """
    # Preprocess image
    tensor = preprocess_image(image_path)
    
    # Move to GPU if available
    if next(model.parameters()).is_cuda:
        tensor = tensor.cuda()
    
    # Generate prediction
    with torch.no_grad():
        density_map = model(tensor).squeeze().cpu().numpy()
    
    # Scale factor for count (since density map is downsampled)
    scale_factor = 2000  # Typically between 1000-3000 based on training setup
    count = float(np.sum(density_map)) * scale_factor
    
    return count, density_map
