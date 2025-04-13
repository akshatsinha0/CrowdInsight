<template>
  <div class="home-view">
    <section class="hero-section gradient-background">
      <div class="container">
        <div class="hero-content flex">
          <div class="hero-text">
            <h1 class="animate-slide-up">
              Advanced Crowd
              <span class="text-gradient">Analysis</span>
              Platform
            </h1>
            <p class="hero-description animate-slide-up">
              Upload crowd images and gain deep insights through our
              state-of-the-art machine learning model.
            </p>
            <div class="hero-cta animate-slide-up">
              <a href="#upload-section" class="btn btn-accent">
                Analyze Crowd Image
                <span class="icon">→</span>
              </a>
            </div>
          </div>
          <div class="hero-visualization">
            <div class="crowd-viz" ref="crowdViz"></div>
          </div>
        </div>
      </div>

      <div class="hero-particles" ref="particles"></div>
    </section>

    <section id="upload-section" class="upload-section">
      <div class="container">
        <div class="section-header">
          <h2>Image <span class="text-gradient">Analysis</span></h2>
          <p class="section-description">
            Upload a crowd image to analyze density, count, and behavioral patterns
          </p>
        </div>

        <div class="upload-area">
          <ImageUploader @image-selected="onImageSelected" @upload-complete="onUploadComplete" />
        </div>

        <div v-if="analysisData" class="analysis-results">
          <AnalysisDisplay :analysis-data="analysisData" />
        </div>
      </div>
    </section>

    <section class="features-section glass">
      <div class="container">
        <div class="section-header">
          <h2>Core <span class="text-gradient">Features</span></h2>
          <p class="section-description">
            Discover the advanced capabilities of our crowd analysis platform
          </p>
        </div>

        <div class="features-grid grid">
          <div class="feature-card card stagger-children">
            <div class="feature-icon">
              <i class="fas fa-chart-line"></i>
            </div>
            <h3>Density Estimation</h3>
            <p>Advanced crowd density mapping with high-precision heatmap visualization</p>
          </div>

          <div class="feature-card card stagger-children">
            <div class="feature-icon">
              <i class="fas fa-users"></i>
            </div>
            <h3>Accurate Counting</h3>
            <p>State-of-the-art deep learning for precise person counting in complex scenarios</p>
          </div>

          <div class="feature-card card stagger-children">
            <div class="feature-icon">
              <i class="fas fa-brain"></i>
            </div>
            <h3>Behavior Analysis</h3>
            <p>Intelligent crowd behavior classification and movement pattern recognition</p>
          </div>

          <div class="feature-card card stagger-children">
            <div class="feature-icon">
              <i class="fas fa-tachometer-alt"></i>
            </div>
            <h3>Real-time Processing</h3>
            <p>High-performance computing with optimized inference for rapid results</p>
          </div>
        </div>
      </div>
    </section>

    <section class="temporal-section">
      <div class="container">
        <div class="section-header">
          <h2>Temporal <span class="text-gradient">Analysis</span></h2>
          <p class="section-description">
            Understand crowd dynamics across time and space
          </p>
        </div>

        <div class="temporal-controls">
          <button @click="isPlaying = !isPlaying" class="btn" :class="isPlaying ? 'btn-secondary' : 'btn-primary'">
            {{ isPlaying ? 'Pause' : 'Play' }}
          </button>

          <div class="timeline-slider">
            <input type="range" min="0" max="100" v-model="timelineValue" :disabled="isPlaying">
            <div class="timeline-value">T+{{ timelineValue }}s</div>
          </div>
        </div>

        <div class="temporal-visualization">
          <TimeWarpViz :time-data="mockTimeData" :playing="isPlaying" />
        </div>
      </div>
    </section>

    <section class="neural-section">
      <div class="container">
        <div class="section-header">
          <h2>Neuromorphic <span class="text-gradient">Intelligence</span></h2>
          <p class="section-description">
            Our algorithm mimics neural processes for intuitive crowd understanding
          </p>
        </div>

        <div class="neural-grid">
          <div class="neural-visualization">
            <NeuralNetwork />
          </div>

          <div class="neural-explanation glass">
            <h3>Crowd Neural Networks</h3>
            <p>
              CrowdInsight's algorithm creates a neuromorphic map of crowd dynamics,
              treating each person as a node in an interconnected system. This approach
              enables us to:
            </p>

            <ul class="neural-features">
              <li>
                <div class="feature-icon">🧠</div>
                <div class="feature-text">
                  <h4>Process Spatial Relationships</h4>
                  <p>Analyze relative positioning and movement vectors between individuals</p>
                </div>
              </li>

              <li>
                <div class="feature-icon">🔄</div>
                <div class="feature-text">
                  <h4>Identify Behavioral Patterns</h4>
                  <p>Detect emergent behavior and group formation dynamics</p>
                </div>
              </li>

              <li>
                <div class="feature-icon">🔍</div>
                <div class="feature-text">
                  <h4>Predict Flow Trajectories</h4>
                  <p>Forecast potential movement patterns and congestion points</p>
                </div>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </section>

    <section class="zero-ui-section">
      <div class="container">
        <div class="section-header">
          <h2>Zero-UI <span class="text-gradient">Paradigm</span></h2>
          <p class="section-description">
            Experience the future of interaction—beyond traditional interfaces
          </p>
        </div>

        <ZeroUIHeatmap>
          <div class="zero-ui-demo">
            <div class="zero-ui-instructions">
              <h3>Ambient Intelligence</h3>
              <p>
                Move your mouse to create a heat map of attention. Areas you focus on more
                will be highlighted, simulating a gaze-tracking interface.
              </p>
              <div class="keyboard-shortcuts">
                <div class="shortcut">
                  <kbd>V</kbd>
                  <span>Activate voice commands</span>
                </div>
                <div class="shortcut">
                  <kbd>Space</kbd>
                  <span>Analyze current focus area</span>
                </div>
                <div class="shortcut">
                  <kbd>Esc</kbd>
                  <span>Reset interface state</span>
                </div>
              </div>
            </div>

            <div class="zero-ui-interaction">
              <div v-for="(area, index) in interactionAreas" :key="index" class="interaction-area" :style="{
                left: `${area.x}%`,
                top: `${area.y}%`,
                width: `${area.size}px`,
                height: `${area.size}px`
              }" @mouseenter="highlightArea(index)" @mouseleave="unhighlightArea(index)">
                <div class="area-content">{{ area.label }}</div>
              </div>
            </div>
          </div>
        </ZeroUIHeatmap>
      </div>
    </section>

    <section class="tech-section">
      <div class="container">
        <div class="section-header">
          <h2>Technology <span class="text-gradient">Stack</span></h2>
          <p class="section-description">Powered by cutting-edge technologies</p>
        </div>

        <div class="tech-showcase">
          <div class="terminal-window">
            <div class="terminal-header">
              <div class="terminal-buttons">
                <span class="terminal-button"></span>
                <span class="terminal-button"></span>
                <span class="terminal-button"></span>
              </div>
              <div class="terminal-title">crowd-insight-terminal</div>
            </div>
            <div class="terminal-content">
              <div class="terminal-line">
                <span class="prompt">$ </span>
                <span class="command animate-typing">python -m crowdinsight.analyze --model=CSRNet --cuda</span>
              </div>
              <div class="terminal-line">
                <span class="response">[INFO] Loading CSRNet model with CUDA acceleration</span>
              </div>
              <div class="terminal-line">
                <span class="response">[INFO] Model loaded successfully (weights: csrnet_v2.pth)</span>
              </div>
              <div class="terminal-line">
                <span class="response">[INFO] Processing image: crowd_sample.jpg</span>
              </div>
              <div class="terminal-line">
                <span class="response">[INFO] Generating density map...</span>
              </div>
              <div class="terminal-line">
                <span class="response">[SUCCESS] Analysis complete!</span>
              </div>
              <div class="terminal-line">
                <span class="response">Total count: 1,247 people</span>
              </div>
              <div class="terminal-line">
                <span class="response">Density pattern: Clustered (7 hotspots identified)</span>
              </div>
              <div class="terminal-line">
                <span class="response">Confidence score: 96.7%</span>
              </div>
              <div class="terminal-line">
                <span class="prompt">$ </span>
                <span class="cursor">_</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, computed } from 'vue';
import ImageUploader from '@/components/ImageUploader.vue';
import AnalysisDisplay from '@/components/AnalysisDisplay.vue';
import * as THREE from 'three';
import { Scene, WebGLRenderer } from 'three';
import type { PerspectiveCamera } from 'three';
import { Object3D } from 'three';
import { createScene, createCamera } from '@/services/three-service';
import TimeWarpViz from '@/components/visualization/TimeWarpViz.vue';
import NeuralNetwork from '@/components/ui/NeuralNetwork.vue';
import ZeroUIHeatmap from '@/components/ui/ZeroUIHeatmap.vue';
// import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';

const interactionAreas = ref([
  { x: 20, y: 30, size: 100, label: 'Hotspot A', highlighted: false },
  { x: 60, y: 40, size: 120, label: 'Hotspot B', highlighted: false },
  { x: 40, y: 70, size: 80, label: 'Hotspot C', highlighted: false },
  { x: 80, y: 20, size: 90, label: 'Hotspot D', highlighted: false }
]);

// Area interaction
const highlightArea = (index: number) => {
  interactionAreas.value[index].highlighted = true;
};

const unhighlightArea = (index: number) => {
  interactionAreas.value[index].highlighted = false;
};


// Add temporal control variables
const isPlaying = ref(false);
const timelineValue = ref(0);

// Generate mock time series data
const mockTimeData = computed(() => {
  // Create a 10x10 grid of time-based data
  const result = [];
  for (let i = 0; i < 10; i++) {
    const row = [];
    for (let j = 0; j < 10; j++) {
      // Base value plus time-dependent component
      const baseValue = (i + j) * 5;
      const timeComponent = Math.sin(timelineValue.value * 0.1 + i * 0.2) * 20;
      row.push(baseValue + timeComponent);
    }
    result.push(row);
  }
  return result;
});

// Visualization setup
const crowdViz = ref<HTMLElement | null>(null);
const particles = ref<HTMLElement | null>(null);
let scene: Scene | null = null;
let camera: PerspectiveCamera | null = null;
let renderer: WebGLRenderer | null = null;
let animationFrame: number | null = null;
// Analysis data state
const analysisData = ref(null);

// Event handlers
const onImageSelected = (image: File) => {
  console.log('Image selected:', image);
  // Here you would typically show a loading state
};

const onUploadComplete = (data: any) => {
  // Set analysis data from API response
  analysisData.value = data;
};

// Three.js visualization
const initThreeJsViz = () => {
  if (!crowdViz.value) return;

  // Initialize Three.js scene
  scene = new THREE.Scene();
  camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
  renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });

  renderer.setSize(crowdViz.value.clientWidth, crowdViz.value.clientHeight);
  crowdViz.value.appendChild(renderer.domElement);

  // Add floating objects
  const geometry = new THREE.SphereGeometry(1, 32, 32);
  const material = new THREE.MeshBasicMaterial({
    color: 0x7048E8,
    wireframe: true
  });

  // Create multiple objects
  for (let i = 0; i < 5; i++) {
    const mesh = new THREE.Mesh(geometry, material);
    mesh.position.set(
      Math.random() * 10 - 5,
      Math.random() * 10 - 5,
      Math.random() * 10 - 15
    );
    mesh.scale.set(
      Math.random() * 2 + 0.5,
      Math.random() * 2 + 0.5,
      Math.random() * 2 + 0.5
    );
    scene.add(mesh);
  }

  camera.position.z = 5;

  // Animation function
  const animate = () => {
    if (!scene || !camera || !renderer) return;

    animationFrame = requestAnimationFrame(animate);

    // Rotate all children
    scene.children.forEach((child: THREE.Object3D, i: number) => {
      child.rotation.x += 0.01 * (i % 2 ? 1 : -1);
      child.rotation.y += 0.01 * (i % 3 ? 1 : -1);
    });

    renderer.render(scene, camera);
  };

  animate();
};

// Background particles
const initParticles = () => {
  if (!particles.value) return;

  const canvas = document.createElement('canvas');
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
  particles.value.appendChild(canvas);

  const ctx = canvas.getContext('2d');
  if (!ctx) return;

  const particlesArray: any[] = [];

  class Particle {
    x: number;
    y: number;
    size: number;
    speedX: number;
    speedY: number;
    color: string;

    constructor() {
      this.x = Math.random() * canvas.width;
      this.y = Math.random() * canvas.height;
      this.size = Math.random() * 3 + 1;
      this.speedX = Math.random() * 0.5 - 0.25;
      this.speedY = Math.random() * 0.5 - 0.25;
      this.color = '#00FFFF';
    }

    update() {
      this.x += this.speedX;
      this.y += this.speedY;

      if (this.x > canvas.width) this.x = 0;
      if (this.x < 0) this.x = canvas.width;
      if (this.y > canvas.height) this.y = 0;
      if (this.y < 0) this.y = canvas.height;
    }

    draw() {
      if (!ctx) return;
      ctx.fillStyle = this.color;
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
      ctx.fill();
    }
  }

  const createParticles = () => {
    for (let i = 0; i < 100; i++) {
      particlesArray.push(new Particle());
    }
  };

  const animateParticles = () => {
    if (!ctx) return;
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    for (let i = 0; i < particlesArray.length; i++) {
      particlesArray[i].update();
      particlesArray[i].draw();

      // Connect nearby particles
      for (let j = i; j < particlesArray.length; j++) {
        const dx = particlesArray[i].x - particlesArray[j].x;
        const dy = particlesArray[i].y - particlesArray[j].y;
        const distance = Math.sqrt(dx * dx + dy * dy);

        if (distance < 100) {
          ctx.beginPath();
          ctx.strokeStyle = `rgba(0, 255, 255, ${1 - distance / 100})`;
          ctx.lineWidth = 0.5;
          ctx.moveTo(particlesArray[i].x, particlesArray[i].y);
          ctx.lineTo(particlesArray[j].x, particlesArray[j].y);
          ctx.stroke();
        }
      }
    }

    requestAnimationFrame(animateParticles);
  };

  createParticles();
  animateParticles();
};

// Intersection Observer for scroll animations
const setupScrollAnimations = () => {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('in-view');
      }
    });
  }, { threshold: 0.1 });

  // Observe all cards and sections
  document.querySelectorAll('.card, .section-header').forEach(el => {
    observer.observe(el);
  });
};

onMounted(() => {
  initThreeJsViz();
  initParticles();
  setupScrollAnimations();
});

onBeforeUnmount(() => {
  if (animationFrame !== null) {
    cancelAnimationFrame(animationFrame);
  }

  // Clean up Three.js resources
  if (renderer) {
    renderer.dispose();
  }
});
</script>

<style scoped>
.hero-section {
  min-height: 85vh;
  display: flex;
  align-items: center;
  position: relative;
  overflow: hidden;
  padding: var(--space-8) 0;
}

.hero-content {
  position: relative;
  z-index: 2;
  flex-direction: column;
  gap: var(--space-6);
}

@media (min-width: 768px) {
  .hero-content {
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
  }

  .hero-text {
    width: 50%;
  }
}

.hero-description {
  font-size: var(--font-size-xl);
  font-weight: var(--font-light);
  margin-bottom: var(--space-6);
  max-width: 600px;
}

.hero-cta {
  display: flex;
  gap: var(--space-4);
}

.hero-visualization {
  flex: 1;
  min-height: 400px;
}

.crowd-viz {
  width: 100%;
  height: 400px;
}

.hero-particles {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
}

.upload-section {
  padding: var(--space-8) 0;
}

.section-header {
  text-align: center;
  margin-bottom: var(--space-7);
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.5s, transform 0.5s;
}

.section-header.in-view {
  opacity: 1;
  transform: translateY(0);
}

.section-description {
  font-size: var(--font-size-lg);
  font-weight: var(--font-light);
  max-width: 700px;
  margin: 0 auto;
}

.upload-area {
  max-width: 800px;
  margin: 0 auto;
}

.analysis-results {
  margin-top: var(--space-7);
}

.features-section {
  padding: var(--space-8) 0;
  margin: var(--space-8) 0;
}

.features-grid {
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: var(--space-5);
}

.feature-card {
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.5s, transform 0.5s;
}

.feature-card.in-view {
  opacity: 1;
  transform: translateY(0);
}

.feature-icon {
  font-size: 2.5rem;
  margin-bottom: var(--space-4);
  color: var(--color-cyan-500);
}

.tech-section {
  padding: var(--space-8) 0;
}

.tech-showcase {
  max-width: 900px;
  margin: 0 auto;
}

.terminal-window {
  background-color: var(--color-deep-blue-800);
  border-radius: var(--radius-lg);
  overflow: hidden;
  box-shadow: var(--shadow-lg);
  margin-top: var(--space-6);
}

.terminal-header {
  background-color: var(--color-deep-blue-900);
  padding: var(--space-3);
  display: flex;
  align-items: center;
}

.terminal-buttons {
  display: flex;
  gap: 8px;
}

.terminal-button {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background-color: #ff5f56;
}

.terminal-button:nth-child(2) {
  background-color: #ffbd2e;
}

.terminal-button:nth-child(3) {
  background-color: #27c93f;
}

.terminal-title {
  margin-left: auto;
  margin-right: auto;
  font-size: var(--font-size-sm);
  color: var(--color-gray-200);
}

.terminal-content {
  padding: var(--space-5);
  font-family: 'Fira Code', monospace;
  font-size: var(--font-size-sm);
}

.terminal-line {
  margin-bottom: var(--space-2);
  line-height: 1.5;
}

.prompt {
  color: var(--color-cyan-500);
}

.command {
  color: var(--color-gray-100);
}

.response {
  color: var(--color-gray-200);
}

.cursor {
  display: inline-block;
  width: 10px;
  height: 1.2em;
  background-color: var(--color-gray-100);
  animation: blink 1s step-end infinite;
}

/* Component transitions */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.temporal-section {
  padding: var(--space-8) 0;
}

.temporal-controls {
  display: flex;
  align-items: center;
  gap: var(--space-4);
  margin-bottom: var(--space-5);
}

.timeline-slider {
  flex: 1;
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.timeline-slider input {
  flex: 1;
  -webkit-appearance: none;
  appearance: none;
  height: 4px;
  background: var(--color-deep-blue-700);
  border-radius: 2px;
  outline: none;
}

.timeline-slider input::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: var(--color-cyan-500);
  cursor: pointer;
  transition: transform 0.2s ease;
}

.timeline-slider input::-webkit-slider-thumb:hover {
  transform: scale(1.2);
}

.timeline-value {
  font-family: 'Fira Code', monospace;
  font-size: var(--font-size-sm);
  color: var(--color-cyan-500);
  min-width: 60px;
}

.temporal-visualization {
  width: 100%;
  height: 500px;
  margin-top: var(--space-4);
}

.neural-section {
  padding: var(--space-8) 0;
  background: radial-gradient(circle at 30% 50%,
      var(--color-deep-blue-800),
      var(--color-deep-blue-900));
}

.neural-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--space-6);
}

@media (min-width: 768px) {
  .neural-grid {
    grid-template-columns: 1fr 1fr;
  }
}

.neural-visualization {
  min-height: 400px;
}

.neural-explanation {
  padding: var(--space-5);
  border-radius: var(--radius-lg);
}

.neural-features {
  list-style: none;
  padding: 0;
  margin: var(--space-5) 0 0;
}

.neural-features li {
  display: flex;
  align-items: flex-start;
  margin-bottom: var(--space-4);
}

.feature-icon {
  font-size: 1.5rem;
  margin-right: var(--space-3);
  background: linear-gradient(45deg, var(--color-purple-700), var(--color-cyan-500));
  border-radius: var(--radius-full);
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.feature-text h4 {
  margin: 0 0 var(--space-1);
  font-size: var(--font-size-lg);
  color: var(--color-cyan-500);
}

.feature-text p {
  margin: 0;
  font-size: var(--font-size-sm);
  color: var(--color-gray-200);
}

.zero-ui-section {
  padding: var(--space-8) 0;
}

.zero-ui-demo {
  width: 100%;
  height: 500px;
  position: relative;
  display: flex;
  flex-direction: column;
}

.zero-ui-instructions {
  padding: var(--space-4);
  background: rgba(30, 41, 59, 0.7);
  border-radius: var(--radius-lg);
  margin-bottom: var(--space-4);
}

.keyboard-shortcuts {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-3);
  margin-top: var(--space-4);
}

.shortcut {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

kbd {
  background-color: var(--color-deep-blue-700);
  color: white;
  padding: 2px 6px;
  border-radius: var(--radius-sm);
  font-family: 'Fira Code', monospace;
  font-size: 0.8rem;
}

.zero-ui-interaction {
  flex: 1;
  position: relative;
  background: rgba(18, 26, 41, 0.5);
  border-radius: var(--radius-lg);
  overflow: hidden;
}

.interaction-area {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  cursor: pointer;
}

.interaction-area:hover {
  background: rgba(var(--color-primary), 0.2);
  border-color: rgba(var(--color-primary), 0.4);
  transform: scale(1.1);
}

.area-content {
  color: white;
  font-weight: var(--font-medium);
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.5);
}
</style>
