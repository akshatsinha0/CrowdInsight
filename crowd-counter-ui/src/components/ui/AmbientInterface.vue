<template>
    <div 
      class="ambient-interface" 
      ref="ambientRoot"
      :class="{ 
        'voice-active': voiceActive, 
        'motion-detected': motionDetected 
      }"
    >
      <div class="ambient-overlay">
        <div class="ambient-indicator" v-if="interfaceState !== 'hidden'">
          <div class="indicator-pulse"></div>
          <div class="indicator-status">
            {{ statusText }}
          </div>
        </div>
      </div>
      <div class="ambient-content">
        <slot></slot>
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref, watch, onMounted, onBeforeUnmount } from 'vue';
  
  // Interface state
  const interfaceState = ref<'hidden' | 'listening' | 'processing' | 'ready'>('hidden');
  const voiceActive = ref(false);
  const motionDetected = ref(false);
  const ambientRoot = ref<HTMLElement | null>(null);
  
  // Status text based on state
  const statusText = ref('');
  
  // Update status text when state changes
  watch(interfaceState, (state) => {
    switch (state) {
      case 'hidden':
        statusText.value = '';
        break;
      case 'listening':
        statusText.value = 'Listening...';
        break;
      case 'processing':
        statusText.value = 'Processing...';
        break;
      case 'ready':
        statusText.value = 'Command recognized';
        break;
    }
  });
  
  // Motion detection using device sensors
  let gyroMonitoring = false;
  
  const initMotionDetection = () => {
    // Check for device orientation support
    if ('DeviceOrientationEvent' in window) {
      window.addEventListener('deviceorientation', handleOrientation);
      gyroMonitoring = true;
    }
    
    // Also track significant mouse movements as a fallback
    document.addEventListener('mousemove', handleMouseActivity);
  };
  
  const handleOrientation = (event: DeviceOrientationEvent) => {
    if (!event.beta || !event.gamma) return;
    
    // Calculate magnitude of movement
    const magnitude = Math.sqrt(
      Math.pow(event.beta, 2) + 
      Math.pow(event.gamma, 2)
    );
    
    // Detect significant movement
    if (magnitude > 15) {
      motionDetected.value = true;
      
      // Reset after a delay
      setTimeout(() => {
        motionDetected.value = false;
      }, 2000);
    }
  };
  
  const handleMouseActivity = (event: MouseEvent) => {
    // Only use mouse as fallback if gyro isn't supported
    if (gyroMonitoring) return;
    
    // Detect rapid mouse movements
    if (event.movementX > 20 || event.movementY > 20) {
      motionDetected.value = true;
      
      // Reset after a delay
      setTimeout(() => {
        motionDetected.value = false;
      }, 1000);
    }
  };
  
  // Simulate voice recognition
  const initVoiceRecognition = () => {
    // In a real implementation, this would use Web Speech API
    // Here we'll simulate periodic activation
    
    let listenTimeout: number | null = null;
    
    // Listen for keyboard commands as a stand-in for voice
    document.addEventListener('keydown', (event) => {
      if (event.key === 'v') {
        // Simulate voice activation
        interfaceState.value = 'listening';
        voiceActive.value = true;
        
        // Simulate processing after 2 seconds
        if (listenTimeout) clearTimeout(listenTimeout);
        
        listenTimeout = setTimeout(() => {
          interfaceState.value = 'processing';
          
          // Then ready state after 1 more second
          setTimeout(() => {
            interfaceState.value = 'ready';
            
            // Then hide after 3 seconds
            setTimeout(() => {
              interfaceState.value = 'hidden';
              voiceActive.value = false;
            }, 3000);
          }, 1000);
        }, 2000);
      }
    });
  };
  
  // Initialize on mount
  onMounted(() => {
    initMotionDetection();
    initVoiceRecognition();
  });
  
  // Clean up on unmount
  onBeforeUnmount(() => {
    if (gyroMonitoring) {
      window.removeEventListener('deviceorientation', handleOrientation);
    }
    document.removeEventListener('mousemove', handleMouseActivity);
  });
  </script>
  
  <style>
  .ambient-interface {
    position: relative;
    width: 100%;
    height: 100%;
    transition: transform 0.5s cubic-bezier(0.65, 0, 0.35, 1);
  }
  
  .ambient-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 1000;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .ambient-indicator {
    position: relative;
    width: 60px;
    height: 60px;
    display: flex;
    align-items: center;
    justify-content: center;
    pointer-events: none;
  }
  
  .indicator-pulse {
    width: 100%;
    height: 100%;
    border-radius: 50%;
    background: radial-gradient(
      circle,
      rgba(112, 72, 232, 0.7) 0%,
      rgba(0, 255, 255, 0.3) 60%,
      transparent 100%
    );
    animation: pulse 2s infinite;
  }
  
  .indicator-status {
    position: absolute;
    top: 120%;
    white-space: nowrap;
    background: rgba(0, 0, 0, 0.7);
    color: white;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 14px;
  }
  
  .ambient-content {
    position: relative;
    z-index: 1;
  }
  
  /* Voice active state */
  .voice-active .ambient-content {
    filter: brightness(0.8) saturate(1.2);
  }
  
  /* Motion detected state */
  .motion-detected .ambient-content {
    transform: scale(0.98);
    transition: transform 0.3s ease;
  }
  
  @keyframes pulse {
    0% {
      transform: scale(0.8);
      opacity: 0.7;
    }
    50% {
      transform: scale(1.1);
      opacity: 0.5;
    }
    100% {
      transform: scale(0.8);
      opacity: 0.7;
    }
  }
  </style>
  