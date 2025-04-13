# CrowdInsight ![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg) ![Vue 3](https://img.shields.io/badge/Vue-3-42b883) ![Python 3.11](https://img.shields.io/badge/Python-3.11-3776ab) ![Model v1.2](https://img.shields.io/badge/Model-v1.2-ff69b4)

**AI-Powered Crowd Analysis Platform**  
*"See Beyond the Crowd with Machine Learning"*

[![Live Demo](https://img.shields.io/badge/Demo-Live-green)](https://crowdinsight.ai) | [![Paper Citation](https://img.shields.io/badge/Citation-Research_Paper-orange)](https://arxiv.org/abs/XXXX.XXXXX)

![CrowdInsight Interface](docs/screenshots/interface-showcase.gif)

## 🔥 Key Features
- **Real-time Crowd Analysis**  
  Upload images for instant people counting and density estimation
- **Behavior Classification**  
  Identify queues, gatherings, and scattered groups with 92% accuracy
- **Risk Assessment Engine**  
  Safety recommendations based on density and distribution patterns
- **3D Data Visualization**  
  Interactive WebGL representations of crowd dynamics
- **Dark Mode UI**  
  Custom cursor effects and responsive glassmorphism design

## 🛠 Tech Stack
### ML Backend
![Python](https://img.shields.io/badge/-Python-3776ab?logo=python) ![Flask](https://img.shields.io/badge/-Flask-000000?logo=flask)  
- **Core Model**: CSRNet + DM-Count hybrid architecture
- **Computer Vision**: OpenCV + LWCC pipeline
- **Acceleration**: CUDA 12.1 with TorchVision

### Frontend
![Vue 3](https://img.shields.io/badge/-Vue_3-42b883?logo=vuedotjs) ![TypeScript](https://img.shields.io/badge/-TypeScript-3178c6?logo=typescript)  
- **Visualization**: Three.js + D3.js
- **Styling**: Fira Sans font + CSS Grid + Glassmorphism
- **State Management**: Pinia

## 🚀 Getting Started

### Prerequisites
- NVIDIA GPU (Recommended) or CPU-only mode
- Docker 24.0+ / Node 18+ / Python 3.11

### Installation
Clone repository
git clone https://github.com/yourusername/crowd-insight.git
cd crowd-insight

Option 1: Docker Setup
docker-compose up --build

Option 2: Local Development
cd server && pip install -r requirements.txt
cd ../client && npm install
npm run dev

## 📊 Dataset Preparation
1. Download [ShanghaiTech Dataset Part A](https://www.dropbox.com/s/xxxxxx/dataset.zip?dl=0)
2. Structure files:
/datasets
/ShanghaiTech
/part_A
/train_data
/test_data

## 🧠 Model Training
python train.py --dataset ShanghaiTech --batch_size 16 --epochs 100


**Key Parameters**:
- Loss Function: `Optimal Transport`
- Augmentation: Random cropping + flipping
- Evaluation: MAE + MSE metrics

## 🌐 API Documentation
curl -X POST -F "image=@crowd.jpg" http://localhost:5000/api/analyze


**Sample Response**:
{
"count": 1247,
"hotspots": [...],
"risk_level": "Moderate",
"density_map": "base64_data"
}



## 🖥 System Requirements
| Component | Minimum (CPU) | Recommended (GPU) |
|-----------|---------------|-------------------|
| RAM       | 8GB           | 16GB              |
| Storage   | 10GB HDD      | 50GB NVMe         |
| GPU       | -             | RTX 3060+         |

## 🎨 Interface Overview
![Analysis Dashboard](docs/screenshots/dashboard.png)  
*Interactive density map with risk assessment overlay*

## 🤝 Contribution
1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

## 📜 License
MIT License - See [LICENSE](LICENSE) for details  
*Please cite our work if using in research:*
@misc{crowdinsight2024,
title={CrowdInsight: Hybrid ML Architecture for Crowd Analysis},
author={Your Name},
year={2024},
publisher={GitHub},
journal={GitHub repository},
howpublished={\url{https://github.com/yourusername/crowd-insight}}
}


## 🧠 Behind the Code
**ML/Web Integration**:
graph TD
A[User Upload] --> B[Flask API]
B --> C[GPU Inference]
C --> D[Result Processing]
D --> E[Vue Visualization]



## ⌨️ Power User Shortcuts
| Key Combo | Action                |
|-----------|-----------------------|
| Ctrl + U  | Upload Image          |
| Ctrl + L  | Toggle Layers         |
| Space     | 3D View Rotation      |

---

**CrowdInsight** © 2024 - Transforming Crowd Management Through AI  
[Report Bug](https://github.com/yourusername/crowd-insight/issues) | [Request Feature](https://github.com/yourusername/crowd-insight/issues)
