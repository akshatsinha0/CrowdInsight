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
