<template>
    <div 
      class="holographic-card" 
      :style="cardStyle" 
      @mousemove="handleMouseMove" 
      @mouseleave="handleMouseLeave"
      ref="cardElement"
    >
      <div class="holographic-overlay"></div>
      <div class="holographic-content">
        <slot></slot>
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref, reactive, onMounted } from 'vue';
  
  // Card element reference
  const cardElement = ref<HTMLElement | null>(null);
  
  // Reactive state for dynamic styling
  const cardStyle = reactive({
    '--rotate-x': '0deg',
    '--rotate-y': '0deg',
    '--glow-x': '50%',
    '--glow-y': '50%',
    '--glow-opacity': '0',
  });
  
  // Handle mouse movement
  const handleMouseMove = (e: MouseEvent) => {
    if (!cardElement.value) return;
    
    const rect = cardElement.value.getBoundingClientRect();
    const centerX = rect.left + rect.width / 2;
    const centerY = rect.top + rect.height / 2;
    
    const percentX = (e.clientX - centerX) / (rect.width / 2);
    const percentY = (e.clientY - centerY) / (rect.height / 2);
    
    // Update rotation based on mouse position (limited to 10deg)
    cardStyle['--rotate-x'] = `${-percentY * 10}deg`;
    cardStyle['--rotate-y'] = `${percentX * 10}deg`;
    
    // Update glow position
    cardStyle['--glow-x'] = `${(e.clientX - rect.left) / rect.width * 100}%`;
    cardStyle['--glow-y'] = `${(e.clientY - rect.top) / rect.height * 100}%`;
    cardStyle['--glow-opacity'] = '1';
  };
  
  const handleMouseLeave = () => {
    // Reset rotation on mouse leave with slight delay for smooth transition
    setTimeout(() => {
      cardStyle['--rotate-x'] = '0deg';
      cardStyle['--rotate-y'] = '0deg';
      cardStyle['--glow-opacity'] = '0';
    }, 100);
  };
  </script>
  
  <style>
  .holographic-card {
    position: relative;
    transform-style: preserve-3d;
    transform: perspective(1000px) rotateX(var(--rotate-x)) rotateY(var(--rotate-y));
    transition: transform 0.2s ease-out;
    border-radius: var(--radius-lg);
    background: rgba(30, 41, 59, 0.4);
    overflow: hidden;
    padding: var(--space-5);
    box-shadow: var(--depth-2);
  }
  
  .holographic-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: radial-gradient(
      circle at var(--glow-x) var(--glow-y),
      rgba(var(--color-primary), 0.15),
      transparent 60%
    );
    pointer-events: none;
    opacity: var(--glow-opacity);
    transition: opacity 0.3s ease;
    z-index: 1;
  }
  
  .holographic-content {
    position: relative;
    z-index: 2;
  }
  
  /* Quantum depth effect */
  .holographic-card {
    --hologram: linear-gradient(
      45deg, 
      hsl(var(--hue-primary) 100% 60% / 0.3),
      hsl(var(--hue-secondary) 100% 60% / 0.3)  
    );
    filter: drop-shadow(0 0 12px var(--hologram));
    transition: filter 0.4s cubic-bezier(0.68, -0.55, 0.27, 1.55);
  }
  
  .holographic-card:hover {
    filter: drop-shadow(0 0 20px var(--hologram));
  }
  </style>
  