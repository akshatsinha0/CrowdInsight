<template>
  <div class="analysis-display">
    <div class="analysis-header">
      <h3>Crowd Analysis Results</h3>
    </div>

    <div class="analysis-content">
      <div class="analysis-grid">
        <HolographicCard class="analysis-visualization">
          <div class="visualization-container">
            <div class="visualization-tabs">
              <button 
                class="viz-tab" 
                :class="{ 'active': activeTab === 'density' }" 
                @click="activeTab = 'density'"
              >
                Density Map
              </button>
              <button 
                class="viz-tab" 
                :class="{ 'active': activeTab === 'hotspot' }" 
                @click="activeTab = 'hotspot'"
              >
                Hotspot Analysis
              </button>
              <button 
                class="viz-tab" 
                :class="{ 'active': activeTab === '3d' }" 
                @click="activeTab = '3d'"
              >
                3D Visualization
              </button>
            </div>

            <div class="visualization-content">
              <div v-show="activeTab === 'density'" class="viz-density">
                <div ref="densityMapContainer" class="density-map-container"></div>
              </div>

              <div v-show="activeTab === 'hotspot'" class="viz-hotspot">
                <div ref="hotspotContainer" class="hotspot-container"></div>
              </div>

              <div v-show="activeTab === '3d'" class="viz-3d">
                <div ref="viz3dContainer" class="viz-3d-container"></div>
              </div>
            </div>
          </div>
        </HolographicCard>

        <HolographicCard class="analysis-metrics">
          <div class="metrics-container">
            <div class="metrics-header">
              <h4>Crowd Metrics</h4>
            </div>

            <div class="metrics-grid">
              <div class="metric-item">
                <div class="metric-label">Total Count</div>
                <div class="metric-value text-gradient">
                  {{ analysisData.count }}
                </div>
              </div>

              <div class="metric-item">
                <div class="metric-label">Crowd Type</div>
                <div class="metric-value">
                  {{ analysisData.crowd_type }}
                </div>
              </div>

              <div class="metric-item">
                <div class="metric-label">Distribution</div>
                <div class="metric-value">
                  {{ analysisData.distribution.pattern }}
                </div>
              </div>

              <div class="metric-item">
                <div class="metric-label">Risk Level</div>
                <div class="metric-value" :class="`risk-${analysisData.risk_level.level.toLowerCase()}`">
                  {{ analysisData.risk_level.level }}
                </div>
              </div>
            </div>

            <div class="metrics-chart">
              <canvas ref="metricsChart"></canvas>
            </div>
          </div>
        </HolographicCard>
      </div>

      <HolographicCard class="analysis-details">
        <div class="details-container">
          <div class="details-header">
            <h4>Detailed Analysis</h4>
          </div>

          <div class="details-content">
            <div class="details-section">
              <h5>Hotspot Analysis</h5>
              <p>
                {{ analysisData.hotspots.length }} distinct hotspots detected.
                Primary concentration intensity: 
                <span class="text-gradient">
                  {{ Math.round(analysisData.hotspots[0].intensity * 100) }}%
                </span>
              </p>
            </div>

            <div class="details-section">
              <h5>Behavior Patterns</h5>
              <p>
                {{ analysisData.distribution.pattern }} distribution with
                <span class="text-gradient">
                  {{ Math.round(analysisData.distribution.uniformity * 100) }}%
                </span>
                uniformity index
              </p>
            </div>

            <div class="details-section">
              <h5>Safety Assessment</h5>
              <p>
                Risk level: 
                <span :class="`risk-${analysisData.risk_level.level.toLowerCase()}`">
                  {{ analysisData.risk_level.level }}
                </span>
                (Score: {{ Math.round(analysisData.risk_level.score * 100) }}/100)
              </p>
              <p>{{ getRiskRecommendation(analysisData.risk_level.level) }}</p>
            </div>
          </div>
        </div>
      </HolographicCard>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, defineProps, onBeforeUnmount } from 'vue';
import type { PropType } from 'vue';
import * as d3 from 'd3';
import Chart from 'chart.js/auto';
import * as THREE from 'three';
import { Scene, WebGLRenderer, PerspectiveCamera } from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';

// Define props with proper typing
const props = defineProps({
  analysisData: {
    type: Object as PropType<any>,
    required: true
  }
});

// Visualization tabs
const activeTab = ref('density');

// Refs for visualization containers
const densityMapContainer = ref<HTMLElement | null>(null);
const hotspotContainer = ref<HTMLElement | null>(null);
const viz3dContainer = ref<HTMLElement | null>(null);
const metricsChart = ref<HTMLCanvasElement | null>(null);

let scene: THREE.Scene | null = null;
let camera: THREE.PerspectiveCamera | null = null;
let renderer: THREE.WebGLRenderer | null = null;
let controls: OrbitControls | null = null;
let animationId: number | null = null;

// Chart instance
let chartInstance: Chart | null = null;

// Risk level recommendations
const getRiskRecommendation = (level: string) => {
  switch (level.toLowerCase()) {
    case 'low':
      return 'Normal monitoring procedures recommended.';
    case 'moderate':
      return 'Consider implementing crowd flow optimization and increased monitoring.';
    case 'high':
      return 'Immediate intervention recommended to reduce density in hotspot areas.';
    case 'critical':
      return 'Urgent action required. Consider emergency protocols to prevent potential hazards.';
    default:
      return '';
  }
};

// Render density map visualization
const renderDensityMap = () => {
  if (!densityMapContainer.value || !props.analysisData) return;

  const container = densityMapContainer.value;
  container.innerHTML = '';

  const width = container.clientWidth;
  const height = container.clientHeight;

  // Create SVG
  const svg = d3.select(container)
    .append('svg')
    .attr('width', width)
    .attr('height', height);

  // Create a sample density grid (this would come from your ML model)
  // For this example, we'll generate a sample
  const gridSize = 30;
  const cellWidth = width / gridSize;
  const cellHeight = height / gridSize;

  // Generate sample data
  const densityData: number[][] = [];
  for (let i = 0; i < gridSize; i++) {
    densityData[i] = [];
    for (let j = 0; j < gridSize; j++) {
      // Create a pattern resembling crowd density
      const centerX = gridSize / 2;
      const centerY = gridSize / 2;
      const distance = Math.sqrt(Math.pow(i - centerX, 2) + Math.pow(j - centerY, 2));
      const base = Math.max(0, 1 - (distance / (gridSize / 2)));

      // Add hotspots
      let value = base;
      props.analysisData.hotspots.forEach((hotspot: any) => {
        const hx = Math.floor((hotspot.center[0] / 600) * gridSize);
        const hy = Math.floor((hotspot.center[1] / 600) * gridSize);
        const hdist = Math.sqrt(Math.pow(i - hx, 2) + Math.pow(j - hy, 2));
        if (hdist < gridSize / 6) {
          value += (hotspot.intensity * (1 - hdist / (gridSize / 6)));
        }
      });

      densityData[i][j] = Math.min(1, value);
    }
  }

  // Color scale
  const colorScale = d3.scaleSequential(d3.interpolateInferno)
    .domain([0, 1]);

  // Draw cells
  for (let i = 0; i < gridSize; i++) {
    for (let j = 0; j < gridSize; j++) {
      svg.append('rect')
        .attr('x', j * cellWidth)
        .attr('y', i * cellHeight)
        .attr('width', cellWidth)
        .attr('height', cellHeight)
        .attr('fill', colorScale(densityData[i][j]))
        .attr('opacity', 0.8);
    }
  }

  // Add legend
  const legendWidth = 20;
  const legendHeight = height - 40;

  // Create gradient for legend
  const defs = svg.append('defs');
  const gradient = defs.append('linearGradient')
    .attr('id', 'density-gradient')
    .attr('x1', '0%')
    .attr('y1', '0%')
    .attr('x2', '0%')
    .attr('y2', '100%');

  gradient.append('stop')
    .attr('offset', '0%')
    .attr('stop-color', colorScale(1));

  gradient.append('stop')
    .attr('offset', '100%')
    .attr('stop-color', colorScale(0));

  // Draw legend rectangle
  svg.append('rect')
    .attr('x', width - legendWidth - 20)
    .attr('y', 20)
    .attr('width', legendWidth)
    .attr('height', legendHeight)
    .style('fill', 'url(#density-gradient)');

  // Add legend ticks
  const legendScale = d3.scaleLinear()
    .domain([1, 0])
    .range([20, 20 + legendHeight]);

  const legendAxis = d3.axisRight(legendScale)
    .ticks(5)
    .tickFormat(d => `${d}`);

  svg.append('g')
    .attr('class', 'legend-axis')
    .attr('transform', `translate(${width - 20}, 0)`)
    .call(legendAxis)
    .selectAll('text')
    .style('fill', 'white')
    .style('font-size', '12px');

  // Add title
  svg.append('text')
    .attr('x', width / 2)
    .attr('y', 15)
    .attr('text-anchor', 'middle')
    .style('fill', 'white')
    .style('font-size', '14px')
    .text('Crowd Density Heatmap');
};

// Render hotspot visualization
const renderHotspots = () => {
  if (!hotspotContainer.value || !props.analysisData) return;

  const container = hotspotContainer.value;
  container.innerHTML = '';

  const width = container.clientWidth;
  const height = container.clientHeight;

  // Create SVG
  const svg = d3.select(container)
    .append('svg')
    .attr('width', width)
    .attr('height', height);

  // Background
  svg.append('rect')
    .attr('width', width)
    .attr('height', height)
    .attr('fill', 'var(--color-deep-blue-800)')
    .attr('rx', 8);

  // Scale hotspot coordinates to container
  const scaleX = width / 600;
  const scaleY = height / 600;

  // Draw connection lines between hotspots
  for (let i = 0; i < props.analysisData.hotspots.length; i++) {
    for (let j = i + 1; j < props.analysisData.hotspots.length; j++) {
      const source = props.analysisData.hotspots[i];
      const target = props.analysisData.hotspots[j];

      svg.append('line')
        .attr('x1', source.center[0] * scaleX)
        .attr('y1', source.center[1] * scaleY)
        .attr('x2', target.center[0] * scaleX)
        .attr('y2', target.center[1] * scaleY)
        .attr('stroke', 'rgba(0, 255, 255, 0.3)')
        .attr('stroke-width', 1)
        .attr('stroke-dasharray', '3,3');
    }
  }

  // Draw hotspots
  svg.selectAll('circle.hotspot')
    .data(props.analysisData.hotspots)
    .enter()
    .append('circle')
    .attr('class', 'hotspot')
    .attr('cx', (d) => (d as { center: [number, number]; area: number }).center[0] * scaleX)
    .attr('cy', (d: unknown) => {
      if (typeof d === 'object' && d !== null && 'center' in d && Array.isArray((d as any).center)) {
        return (d as { center: [number, number]; area: number }).center[1] * scaleY;
      }
      return 0; // Default value if 'd' is not in the expected format
    })
    .attr('r', (d) => Math.sqrt((d as { area: number }).area) * 0.05 * scaleX)
    .attr('fill', d => {
      const color = d3.interpolateRdYlBu(1 - (d as { intensity: number }).intensity);
      return color;
    })
    .attr('opacity', 0.7)
    .attr('stroke', 'white')
    .attr('stroke-width', 1);

  // Add labels
  svg.selectAll('text.hotspot-label')
    .data(props.analysisData.hotspots as { center: [number, number]; area: number }[])
    .enter()
    .append('text')
    .attr('class', 'hotspot-label')
    .attr('x', (d: { center: [number, number]; area: number }) => d.center[0] * scaleX)
    .attr('y', (d: { center: [number, number]; area: number }) => (d.center[1] * scaleY) - (Math.sqrt(d.area) * 0.05 * scaleX) - 10)
    .attr('text-anchor', 'middle')
    .attr('fill', 'white')
    .attr('font-size', '12px')
    .text((d: { center: [number, number]; area: number }, i) => `Hotspot ${i + 1}`);

  // Center of mass
  svg.append('circle')
    .attr('cx', props.analysisData.distribution.center_of_mass[0] * scaleX)
    .attr('cy', props.analysisData.distribution.center_of_mass[1] * scaleY)
    .attr('r', 8)
    .attr('fill', 'var(--color-pink-500)')
    .attr('stroke', 'white')
    .attr('stroke-width', 1);

  svg.append('text')
    .attr('x', props.analysisData.distribution.center_of_mass[0] * scaleX)
    .attr('y', props.analysisData.distribution.center_of_mass[1] * scaleY - 15)
    .attr('text-anchor', 'middle')
    .attr('fill', 'white')
    .attr('font-size', '12px')
    .text('Center of Mass');

  // Add title
  svg.append('text')
    .attr('x', width / 2)
    .attr('y', 15)
    .attr('text-anchor', 'middle')
    .style('fill', 'white')
    .style('font-size', '14px')
    .text('Crowd Hotspot Analysis');
};

// Render 3D visualization
const render3DView = () => {
  if (!viz3dContainer.value || !props.analysisData) return;

  const container = viz3dContainer.value;
  container.innerHTML = '';

  // Initialize Three.js
  scene = new THREE.Scene();
  camera = new THREE.PerspectiveCamera(75, container.clientWidth / container.clientHeight, 0.1, 1000);
  renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
  renderer.setSize(container.clientWidth, container.clientHeight);
  container.appendChild(renderer.domElement);

  // Setup OrbitControls
  controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  controls.dampingFactor = 0.05;

  // Add lights
  const ambientLight = new THREE.AmbientLight(0x404040);
  scene.add(ambientLight);

  const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
  directionalLight.position.set(0, 10, 10);
  scene.add(directionalLight);

  // Create base plane
  const planeGeometry = new THREE.PlaneGeometry(10, 10, 20, 20);
  const planeMaterial = new THREE.MeshBasicMaterial({
    color: 0x1E293B,
    wireframe: true,
    transparent: true,
    opacity: 0.5
  });
  const plane = new THREE.Mesh(planeGeometry, planeMaterial);
  plane.rotation.x = -Math.PI / 2;
  scene.add(plane);

  // Add hotspots as columns
  props.analysisData.hotspots.forEach((hotspot: any, index: number) => {
    const normalizedX = (hotspot.center[0] / 600) * 10 - 5;
    const normalizedZ = (hotspot.center[1] / 600) * 10 - 5;
    const height = hotspot.intensity * 5;

    const columnGeometry = new THREE.BoxGeometry(0.5, height, 0.5);
    const columnMaterial = new THREE.MeshStandardMaterial({
      color: new THREE.Color(`hsl(${index * 137.5 % 360}, 70%, 60%)`),
      transparent: true,
      opacity: 0.8
    });

    const column = new THREE.Mesh(columnGeometry, columnMaterial);
    column.position.set(normalizedX, height / 2, normalizedZ);
    scene.add(column);

    // Add hotspot label
    const labelDiv = document.createElement('div');
    labelDiv.className = 'hotspot-3d-label';
    labelDiv.textContent = `Hotspot ${index + 1}`;
    labelDiv.style.position = 'absolute';
    labelDiv.style.color = 'white';
    labelDiv.style.padding = '2px 5px';
    labelDiv.style.backgroundColor = 'rgba(0, 0, 0, 0.5)';
    labelDiv.style.borderRadius = '4px';
    labelDiv.style.fontSize = '10px';
    container.appendChild(labelDiv);

    // Position labels in update loop
  });

  // Position camera
  camera.position.set(5, 5, 5);
  camera.lookAt(0, 0, 0);

  // Animation loop
  const animate = () => {
    if (!scene || !camera || !renderer || !controls) return;

    animationId = requestAnimationFrame(animate);
    controls.update();
    renderer.render(scene, camera);
  };

  animate();
};

// Initialize metrics chart
const initMetricsChart = () => {
  if (!metricsChart.value || !props.analysisData) return;

  if (chartInstance) {
    chartInstance.destroy();
  }

  // Get data from analysis
  const data = {
    labels: ['Density', 'Risk Score', 'Uniformity', 'Area Coverage'],
    datasets: [{
      label: 'Crowd Metrics',
      data: [
        props.analysisData.hotspots[0].intensity * 100,
        props.analysisData.risk_level.score * 100,
        props.analysisData.distribution.uniformity * 100,
        props.analysisData.hotspots.reduce((acc: number, h: any) => acc + h.area, 0) / 1000
      ],
      backgroundColor: 'rgba(112, 72, 232, 0.6)',
      borderColor: 'rgba(0, 255, 255, 1)',
      borderWidth: 2,
      borderRadius: 5,
    }]
  };

  chartInstance = new Chart(metricsChart.value, {
    type: 'bar',
    data,
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
          max: 100,
          ticks: {
            color: 'rgba(255, 255, 255, 0.7)'
          },
          grid: {
            color: 'rgba(255, 255, 255, 0.1)'
          }
        },
        x: {
          ticks: {
            color: 'rgba(255, 255, 255, 0.7)'
          },
          grid: {
            color: 'rgba(255, 255, 255, 0.1)'
          }
        }
      },
      plugins: {
        legend: {
          display: false
        }
      }
    }
  });
};

// Clean up function for 3D visualization
const cleanup3D = () => {
  if (animationId !== null) {
    cancelAnimationFrame(animationId);
  }

  if (renderer) {
    renderer.dispose();
  }

  if (viz3dContainer.value) {
    const labels = viz3dContainer.value.querySelectorAll('.hotspot-3d-label');
    labels.forEach(label => label.remove());
  }
};

// Initialize visualizations when component is mounted
onMounted(() => {
  renderDensityMap();
  renderHotspots();
  render3DView();
  initMetricsChart();
});

// Watch for tab changes to render the appropriate visualization
watch(activeTab, (newTab) => {
  if (newTab === 'density') {
    renderDensityMap();
  } else if (newTab === 'hotspot') {
    renderHotspots();
  } else if (newTab === '3d') {
    cleanup3D();
    render3DView();
  }
});

// Clean up on component unmount
onBeforeUnmount(() => {
  cleanup3D();
  if (chartInstance) {
    chartInstance.destroy();
  }
});
</script>

<style scoped>
.analysis-display {
  width: 100%;
}

.analysis-header {
  margin-bottom: var(--space-5);
  text-align: center;
}

.analysis-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--space-5);
  margin-bottom: var(--space-5);
}

@media (min-width: 768px) {
  .analysis-grid {
    grid-template-columns: 3fr 2fr;
  }
}

.visualization-tabs {
  display: flex;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  margin-bottom: var(--space-4);
}

.viz-tab {
  padding: var(--space-2) var(--space-4);
  background: none;
  border: none;
  color: var(--color-gray-200);
  cursor: pointer;
  font-size: var(--font-size-sm);
  position: relative;
  transition: color var(--transition-normal);
}

.viz-tab::after {
  content: '';
  position: absolute;
  bottom: -1px;
  left: 0;
  width: 0;
  height: 2px;
  background-color: var(--color-cyan-500);
  transition: width var(--transition-normal);
}

.viz-tab:hover,
.viz-tab.active {
  color: var(--color-gray-100);
}

.viz-tab.active::after {
  width: 100%;
}

.visualization-content {
  height: 400px;
  position: relative;
  overflow: hidden;
  border-radius: var(--radius-md);
}

.density-map-container,
.hotspot-container,
.viz-3d-container {
  width: 100%;
  height: 100%;
}

.metrics-header {
  margin-bottom: var(--space-4);
}

.metrics-content {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--space-3);
  margin-bottom: var(--space-4);
}

.metric-item {
  background-color: rgba(0, 0, 0, 0.2);
  border-radius: var(--radius-md);
  padding: var(--space-3);
}

.metric-label {
  font-size: var(--font-size-xs);
  color: var(--color-gray-200);
  margin-bottom: var(--space-1);
}

.metric-value {
  font-size: var(--font-size-lg);
  font-weight: var(--font-semibold);
}

.risk-low {
  color: #4ade80;
}

.risk-moderate {
  color: #fbbf24;
}

.risk-high {
  color: #fb923c;
}

.risk-critical {
  color: #ef4444;
}

.metrics-chart {
  height: 200px;
  margin-top: var(--space-4);
}

.details-header {
  margin-bottom: var(--space-4);
}

.details-content {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--space-4);
}

@media (min-width: 768px) {
  .details-content {
    grid-template-columns: repeat(3, 1fr);
  }
}

.details-section h5 {
  margin-bottom: var(--space-3);
  color: var(--color-cyan-500);
}
</style>