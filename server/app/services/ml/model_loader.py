import os
import torch
import torch.nn as nn
from torchvision import models
from flask import current_app 

class CSRNet(nn.Module):
    def __init__(self):
        super(CSRNet, self).__init__()
        # Frontend (VGG16)
        frontend = list(models.vgg16(pretrained=True).features.children())
        self.frontend = nn.Sequential(*frontend[:23])
        
        # Backend (Dilated Convolutions)
        self.backend = nn.Sequential(
            nn.Conv2d(512, 512, kernel_size=3, padding=2, dilation=2), nn.ReLU(),
            nn.Conv2d(512, 512, kernel_size=3, padding=2, dilation=2), nn.ReLU(),
            nn.Conv2d(512, 512, kernel_size=3, padding=2, dilation=2), nn.ReLU(),
            nn.Conv2d(512, 256, kernel_size=3, padding=2, dilation=2), nn.ReLU(),
            nn.Conv2d(256, 128, kernel_size=3, padding=2, dilation=2), nn.ReLU(),
            nn.Conv2d(128, 64, kernel_size=3, padding=2, dilation=2), nn.ReLU()
        )
        
        # Output Layer
        self.output = nn.Sequential(
            nn.Conv2d(64, 1, kernel_size=1)
        )
        
    def forward(self, x):
        x = self.frontend(x)
        x = self.backend(x)
        x = self.output(x)
        return x

class ModelService:
    """Singleton service for loading and managing ML model"""
    _instance = None
    
    def __init__(self, model_path, device="cpu"):
        self.model_path = model_path
        self.device = device
        self.model = None
        self.load_model()
        
    @classmethod
    def get_instance(cls):
        """Get singleton instance of model service"""
        if cls._instance is None:
            from flask import current_app
            config = current_app.config
            cls._instance = cls(config["MODEL_PATH"], config["MODEL_DEVICE"])
        return cls._instance
        
    def load_model(self):
        """Load CSRNet model from disk"""
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Model file not found: {self.model_path}")
            
        model = CSRNet()
        
        # Load weights
        if torch.cuda.is_available() and self.device == "cuda":
            model.load_state_dict(torch.load(self.model_path))
            model = model.cuda()
        else:
            model.load_state_dict(torch.load(self.model_path, map_location=torch.device('cpu')))
            
        model.eval()
        self.model = model
        
    def is_loaded(self):
        """Check if model is loaded"""
        return self.model is not None
