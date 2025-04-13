import os
import cv2
import numpy as np
import scipy.io as sio

def create_density_map(image_path, gt_path, sigma=15):
    # Load image and annotations
    image = cv2.imread(image_path)
    mat = sio.loadmat(gt_path)
    points = mat["image_info"][0][0][0][0][0]
    
    # Create density map
    density_map = np.zeros(image.shape[:2], dtype=np.float32)
    h, w = density_map.shape
    
    for x, y in points:
        x = min(int(x), w-1)
        y = min(int(y), h-1)
        density_map[y, x] = 1
        
    # Apply Gaussian filter
    density_map = cv2.GaussianBlur(density_map, (sigma, sigma), 0)
    return density_map[..., np.newaxis]

def load_data(dataset_path, part='A'):
    train_images = []
    train_maps = []
    
    base_path = f"{dataset_path}/part_{part}/train_data/"
    for img_file in os.listdir(f"{base_path}/images"):
        img_path = f"{base_path}/images/{img_file}"
        gt_path = f"{base_path}/ground-truth/GT_{img_file.replace('.jpg', '.mat')}"
        density_map = create_density_map(img_path, gt_path)
        
        train_images.append(img_path)
        train_maps.append(density_map)
        
    return train_images, train_maps
