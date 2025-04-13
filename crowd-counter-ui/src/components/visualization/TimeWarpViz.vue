<template>
    <div class="time-warp-container" ref="container"></div>
  </template>
  
  <script setup lang="ts">
  import { ref, onMounted, onBeforeUnmount, watch } from 'vue';
  import {
    Scene,
    PerspectiveCamera,
    WebGLRenderer,
    TorusKnotGeometry,
    ShaderMaterial,
    Mesh,
    Vector2,
    Color,
    Clock
  } from 'three';
  import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';
  
  const props = defineProps<{
    timeData: number[][];
    playing: boolean;
  }>();
  
  const container = ref<HTMLElement | null>(null);
  let scene: Scene | null = null;
  let camera: PerspectiveCamera | null = null;
  let renderer: WebGLRenderer | null = null;
  let controls: OrbitControls | null = null;
  let timeWarp: Mesh | null = null;
  let clock: Clock | null = null;
  let animationId: number | null = null;
  
  // Shaders
  const vertexShader = `
  varying vec3 vPos;
  varying vec2 vUv;
  uniform float time;
  
  void main() {
    vPos = position;
    vUv = uv;
    
    // Time-based vertex displacement
    vec3 pos = position;
    float displacement = sin(position.x * 10.0 + time) * 0.1;
    displacement += sin(position.y * 10.0 + time) * 0.1;
    pos += normal * displacement;
    
    gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
  }
  `;
  
  const fragmentShader = `
  varying vec3 vPos;
  varying vec2 vUv;
  uniform float time;
  uniform vec2 resolution;
  uniform vec3 colorA;
  uniform vec3 colorB;
  
  void main() {
    // Dynamic color mixing based on position and time
    vec3 pos = vPos * 0.1;
    float pattern = sin(pos.x * 10.0 + time) * sin(pos.y * 10.0 + time) * sin(pos.z * 10.0 + time);
    
    // Holographic effect
    float edge = abs(sin(vUv.y * 100.0 + time * 2.0)) * 0.1;
    pattern += edge;
    
    // Color interpolation
    vec3 color = mix(colorA, colorB, pattern);
    
    gl_FragColor = vec4(color, 0.8);
  }
  `;
  
  const initScene = () => {
    if (!container.value) return;
    
    // Setup
    scene = new Scene();
    camera = new PerspectiveCamera(
      75,
      container.value.clientWidth / container.value.clientHeight,
      0.1,
      1000
    );
    renderer = new WebGLRenderer({ alpha: true, antialias: true });
    renderer.setSize(container.value.clientWidth, container.value.clientHeight);
    container.value.appendChild(renderer.domElement);
    
    // Add orbit controls
    controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    
    // Position camera
    camera.position.z = 30;
    
    // Create time warp geometry
    const geometry = new TorusKnotGeometry(10, 3, 256, 32);
    
    // Create shader material
    const material = new ShaderMaterial({
      uniforms: {
        time: { value: 0 },
        resolution: { value: new Vector2(
          container.value.clientWidth,
          container.value.clientHeight
        )},
        colorA: { value: new Color(0x7048E8) },
        colorB: { value: new Color(0x00FFFF) }
      },
      vertexShader,
      fragmentShader,
      transparent: true
    });
    
    // Create mesh
    timeWarp = new Mesh(geometry, material);
    scene.add(timeWarp);
    
    // Setup clock
    clock = new Clock();
    
    // Start animation
    animate();
    
    // Handle window resize
    const handleResize = () => {
      if (!container.value || !camera || !renderer) return;
      
      camera.aspect = container.value.clientWidth / container.value.clientHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(container.value.clientWidth, container.value.clientHeight);
      
      if (material.uniforms.resolution) {
        material.uniforms.resolution.value.set(
          container.value.clientWidth,
          container.value.clientHeight
        );
      }
    };
    
    window.addEventListener('resize', handleResize);
    
    // Return cleanup function
    return () => {
      window.removeEventListener('resize', handleResize);
    };
  };
  
  const animate = () => {
    if (!scene || !camera || !renderer || !clock || !timeWarp || !controls) return;
    
    animationId = requestAnimationFrame(animate);
    
    // Update controls
    controls.update();
    
    // Update time uniform
    if (props.playing && timeWarp.material instanceof ShaderMaterial) {
      timeWarp.material.uniforms.time.value = clock.getElapsedTime();
    }
    
    // Render
    renderer.render(scene, camera);
  };
  
  // Update time warp with new data
  watch(() => props.timeData, (newData) => {
    if (!timeWarp || !scene) return;
    
    // Could update geometry or colors based on new data
    if (timeWarp.material instanceof ShaderMaterial) {
      const maxValue = Math.max(...newData.flat());
      const intensity = maxValue / 100; // Scale based on data
      
      timeWarp.material.uniforms.colorA.value = new Color(
        intensity > 0.7 ? 0xff5500 : 0x7048E8
      );
    }
  });
  
  // Initialize and cleanup
  onMounted(() => {
    const cleanup = initScene();
    
    onBeforeUnmount(() => {
      if (animationId !== null) {
        cancelAnimationFrame(animationId);
      }
      
      if (renderer) {
        renderer.dispose();
      }
      
      if (container.value) {
        container.value.innerHTML = '';
      }
      
      if (cleanup) cleanup();
    });
  });
  </script>
  
  <style>
  .time-warp-container {
    width: 100%;
    height: 400px;
    position: relative;
    overflow: hidden;
    border-radius: var(--radius-lg);
  }
  </style>
  