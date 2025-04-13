<template>
    <div class="zero-ui-heatmap" ref="heatmapContainer">
      <canvas ref="heatmapCanvas" class="heatmap-canvas"></canvas>
      <div class="content-layer">
        <slot></slot>
      </div>
      <div 
        v-if="enableFocusIndicator" 
        class="focus-indicator"
        :style="{
          transform: `translate(${focusX}px, ${focusY}px)`,
          opacity: focusActive ? 1 : 0
        }"
      ></div>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref, onMounted, onBeforeUnmount } from 'vue';
  import { getGazeManager } from '@/services/GazeManager';
  
  // Props
  const props = defineProps({
    fadeTime: {
      type: Number,
      default: 2000
    },
    heatmapIntensity: {
      type: Number,
      default: 0.5
    },
    enableFocusIndicator: {
      type: Boolean,
      default: true
    }
  });
  
  // Refs
  const heatmapContainer = ref<HTMLElement | null>(null);
  const heatmapCanvas = ref<HTMLCanvasElement | null>(null);
  const focusX = ref(0);
  const focusY = ref(0);
  const focusActive = ref(false);
  
  // Heatmap data
  let heatmapData: { x: number; y: number; value: number; timestamp: number }[] = [];
  let ctx: CanvasRenderingContext2D | null = null;
  let animationId: number | null = null;
  let gazeManager: ReturnType<typeof getGazeManager> | null = null;
  
  // Initialize canvas and heatmap
  const initializeHeatmap = () => {
    if (!heatmapCanvas.value || !heatmapContainer.value) return;
    
    // Set canvas size to match container
    const containerRect = heatmapContainer.value.getBoundingClientRect();
    heatmapCanvas.value.width = containerRect.width;
    heatmapCanvas.value.height = containerRect.height;
    
    // Get context
    ctx = heatmapCanvas.value.getContext('2d');
    if (!ctx) return;
    
    // Initialize gaze tracking
    gazeManager = getGazeManager();
    gazeManager.initialize();
    
    // Listen for gaze movements
    gazeManager.addEventListener('gazemove', handleGazeMove);
    gazeManager.addEventListener('gazefocus', handleGazeFocus);
    gazeManager.addEventListener('gazeblur', handleGazeBlur);
    
    // Start render loop
    renderHeatmap();
  };
  
  // Handle gaze movement
  const handleGazeMove = (event: CustomEvent) => {
    if (!heatmapContainer.value) return;
    
    const containerRect = heatmapContainer.value.getBoundingClientRect();
    const relativeX = event.detail.x - containerRect.left;
    const relativeY = event.detail.y - containerRect.top;
    
    // Update focus indicator
    focusX.value = relativeX;
    focusY.value = relativeY;
    
    // Only add points within the container
    if (
      relativeX >= 0 && relativeX <= containerRect.width &&
      relativeY >= 0 && relativeY <= containerRect.height
    ) {
      // Add point to heatmap
      heatmapData.push({
        x: relativeX,
        y: relativeY,
        value: props.heatmapIntensity,
        timestamp: Date.now()
      });
    }
  };
  
  // Handle gaze focus
  const handleGazeFocus = (event: CustomEvent) => {
    focusActive.value = true;
  };
  
  // Handle gaze blur
  const handleGazeBlur = (event: CustomEvent) => {
    focusActive.value = false;
  };
  
  // Render heatmap
  const renderHeatmap = () => {
    if (!ctx || !heatmapCanvas.value) return;
    
    // Clear canvas
    ctx.clearRect(0, 0, heatmapCanvas.value.width, heatmapCanvas.value.height);
    
    // Remove old points
    const now = Date.now();
    heatmapData = heatmapData.filter(point => now - point.timestamp < props.fadeTime);
    
    // Draw heat points
    for (const point of heatmapData) {
      const age = (now - point.timestamp) / props.fadeTime;
      const opacity = 1 - age;
      
      const gradient = ctx.createRadialGradient(
        point.x, point.y, 0,
        point.x, point.y, 50
      );
      
      gradient.addColorStop(0, `rgba(0, 255, 255, ${opacity * 0.8})`);
      gradient.addColorStop(0.5, `rgba(112, 72, 232, ${opacity * 0.4})`);
      gradient.addColorStop(1, `rgba(0, 0, 0, 0)`);
      
      ctx.fillStyle = gradient;
      ctx.beginPath();
      ctx.arc(point.x, point.y, 50, 0, Math.PI * 2);
      ctx.fill();
    }
    
    // Continue animation
    animationId = requestAnimationFrame(renderHeatmap);
  };
  
  // Handle resize
  const handleResize = () => {
    if (!heatmapCanvas.value || !heatmapContainer.value) return;
    
    const containerRect = heatmapContainer.value.getBoundingClientRect();
    heatmapCanvas.value.width = containerRect.width;
    heatmapCanvas.value.height = containerRect.height;
  };
  
  // Initialize on mount
  onMounted(() => {
    initializeHeatmap();
    window.addEventListener('resize', handleResize);
  });
  
  // Clean up on unmount
  onBeforeUnmount(() => {
    if (animationId !== null) {
      cancelAnimationFrame(animationId);
    }
    
    if (gazeManager) {
      gazeManager.removeEventListener('gazemove', handleGazeMove);
      gazeManager.removeEventListener('gazefocus', handleGazeFocus);
      gazeManager.removeEventListener('gazeblur', handleGazeBlur);
    }
    
    window.removeEventListener('resize', handleResize);
  });
  </script>
  
  <style>
  .zero-ui-heatmap {
    position: relative;
    width: 100%;
    height: 100%;
    overflow: hidden;
  }
  
  .heatmap-canvas {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 1;
  }
  
  .content-layer {
    position: relative;
    z-index: 2;
    width: 100%;
    height: 100%;
  }
  
  .focus-indicator {
    position: absolute;
    width: 60px;
    height: 60px;
    border-radius: 50%;
    background: radial-gradient(
      circle,
      rgba(0, 255, 255, 0.2) 0%,
      rgba(0, 255, 255, 0.1) 40%,
      transparent 70%
    );
    transform: translate(-50%, -50%);
    pointer-events: none;
    z-index: 3;
    transition: opacity 0.3s ease;
  }
  </style>
  