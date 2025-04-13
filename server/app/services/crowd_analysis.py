import numpy as np
from scipy.ndimage import gaussian_filter, label, maximum_filter
import cv2

class CrowdAnalyzer:
    """Advanced crowd behavior analysis based on density maps"""
    
    def __init__(self):
        self.density_threshold = 0.25
        
    def analyze_crowd(self, density_map):
        """
        Analyzes density map to extract crowd insights
        Args:
            density_map: 2D numpy array with crowd density
        Returns:
            Dictionary with crowd metrics
        """
        # Normalize for analysis
        normalized_map = density_map / density_map.max() if density_map.max() > 0 else density_map
        
        # Identify hotspots (high density areas)
        hotspots = self._find_hotspots(normalized_map)
        
        # Calculate crowd distribution patterns
        distribution = self._analyze_distribution(normalized_map)
        
        # Determine crowd flow from density gradient
        flow = self._estimate_flow(normalized_map)
        
        # Classify crowd type
        crowd_type = self._classify_crowd_type(normalized_map, hotspots)
        
        return {
            "count": float(np.sum(density_map)),
            "hotspots": hotspots,
            "distribution": distribution,
            "flow_pattern": flow,
            "crowd_type": crowd_type,
            "risk_level": self._assess_risk(normalized_map, hotspots)
        }
    
    def _find_hotspots(self, density_map):
        """Identifies high-density regions"""
        threshold = self.density_threshold * density_map.max()
        binary = density_map > threshold
        
        # Label connected components
        labeled, num_features = label(binary)
        
        hotspots = []
        for i in range(1, num_features + 1):
            region = (labeled == i)
            if np.sum(region) > 10:  # Minimum size threshold
                y, x = np.where(region)
                center_y, center_x = int(np.mean(y)), int(np.mean(x))
                intensity = float(np.mean(density_map[region]))
                area = int(np.sum(region))
                
                hotspots.append({
                    "center": (center_x, center_y),
                    "intensity": intensity,
                    "area": area
                })
        
        return hotspots
    
    def _analyze_distribution(self, density_map):
        """Analyzes spatial distribution of crowd"""
        # Calculate statistical moments
        h, w = density_map.shape
        y_indices, x_indices = np.mgrid[0:h, 0:w]
        
        # Center of mass
        total = density_map.sum()
        if total == 0:
            return {"pattern": "No crowd detected"}
            
        cm_y = np.sum(y_indices * density_map) / total
        cm_x = np.sum(x_indices * density_map) / total
        
        # Calculate dispersion/spread
        dist_from_cm = np.sqrt((y_indices - cm_y)**2 + (x_indices - cm_x)**2)
        dispersion = np.sum(dist_from_cm * density_map) / total
        
        # Analyze uniformity (std dev relative to mean)
        uniformity = 1 - (np.std(density_map) / (np.mean(density_map) + 1e-5))
        
        if dispersion < 0.15 * max(h, w):
            pattern = "Clustered"
        elif uniformity > 0.7:
            pattern = "Uniform"
        else:
            pattern = "Dispersed"
            
        return {
            "center_of_mass": (float(cm_x), float(cm_y)),
            "dispersion": float(dispersion),
            "uniformity": float(uniformity),
            "pattern": pattern
        }
    
    def _estimate_flow(self, density_map):
        """Estimates crowd flow direction based on density gradient"""
        smoothed = gaussian_filter(density_map, sigma=3)
        
        # Calculate gradient (dy, dx)
        gy, gx = np.gradient(smoothed)
        
        # Compute magnitude and direction
        magnitude = np.sqrt(gx**2 + gy**2)
        direction = np.arctan2(gy, gx) * 180 / np.pi
        
        # Find dominant direction
        if magnitude.max() < 0.01:
            flow_type = "Static"
            dominant_angle = 0
        else:
            # Weight angles by gradient magnitude
            bins = np.linspace(-180, 180, 9)  # 8 direction bins
            hist, _ = np.histogram(direction, bins=bins, weights=magnitude)
            dominant_idx = np.argmax(hist)
            dominant_angle = (bins[dominant_idx] + bins[dominant_idx+1]) / 2
            
            # Classify flow pattern
            if magnitude.max() > 0.1:
                flow_type = "Directional"
            else:
                flow_type = "Turbulent" if np.std(direction[magnitude > 0.01]) > 45 else "Laminar"
        
        return {
            "type": flow_type,
            "direction_degrees": float(dominant_angle),
            "magnitude": float(magnitude.mean())
        }
    
    def _classify_crowd_type(self, density_map, hotspots):
        """Determines crowd behavior type based on density and distribution"""
        if not hotspots:
            return "Empty"
            
        max_density = density_map.max()
        avg_density = density_map.mean()
        num_hotspots = len(hotspots)
        
        # Calculate distances between hotspots
        centers = np.array([h["center"] for h in hotspots])
        if len(centers) > 1:
            from scipy.spatial.distance import pdist
            distances = pdist(centers)
            avg_distance = float(np.mean(distances))
        else:
            avg_distance = 0
            
        if max_density > 0.8:
            if num_hotspots == 1:
                return "Dense Gathering"
            elif avg_distance < 100:
                return "Multiple Gatherings"
            else:
                return "Distributed Groups"
        elif 0.3 < max_density <= 0.8:
            if avg_density < 0.2:
                return "Queue Formation"
            else:
                return "Uniform Crowd"
        else:
            return "Sparse Population"
    
    def _assess_risk(self, density_map, hotspots):
        """Evaluates safety risk based on crowd density and patterns"""
        if not hotspots:
            return {"level": "Low", "score": 0.0}
            
        # Get maximum density
        max_density = max([h["intensity"] for h in hotspots])
        
        # Calculate density gradient (rapid changes indicate potential issues)
        smoothed = gaussian_filter(density_map, sigma=2)
        gy, gx = np.gradient(smoothed)
        gradient_magnitude = np.sqrt(gx**2 + gy**2)
        max_gradient = gradient_magnitude.max()
        
        # Calculate risk factors
        density_factor = min(max_density * 10, 1.0)
        gradient_factor = min(max_gradient * 20, 1.0)
        hotspot_factor = min(len(hotspots) / 5, 1.0)
        
        # Combined risk score (0-1)
        risk_score = 0.5 * density_factor + 0.3 * gradient_factor + 0.2 * hotspot_factor
        
        # Risk level classification
        if risk_score < 0.3:
            level = "Low"
        elif risk_score < 0.6:
            level = "Moderate"
        elif risk_score < 0.8:
            level = "High"
        else:
            level = "Critical"
            
        return {"level": level, "score": float(risk_score)}
