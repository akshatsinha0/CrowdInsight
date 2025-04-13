import {
    Scene,
    PerspectiveCamera,
    WebGLRenderer,
    DirectionalLight,
    PlaneGeometry,
    Color
  } from 'three';
  
  // Export initialized instances
  export function createScene() {
    return new Scene();
  }
  
  export function createCamera(aspect: number) {
    return new PerspectiveCamera(75, aspect, 0.1, 1000);
  }
  
  // Additional factory functions...
  