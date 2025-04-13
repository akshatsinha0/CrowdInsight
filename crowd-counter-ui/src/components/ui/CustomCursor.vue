<template>
  <div>
    <div ref="cursorDot" class="custom-cursor-dot"></div>
    <div ref="cursor" class="custom-cursor"></div>
    <div ref="cursorRing" class="custom-cursor-ring"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';

const cursor = ref<HTMLElement | null>(null);
const cursorDot = ref<HTMLElement | null>(null);
const cursorRing = ref<HTMLElement | null>(null);
let mouseX = 0;
let mouseY = 0;
let dotX = 0;
let dotY = 0;
let cursorX = 0;
let cursorY = 0;
let ringX = 0;
let ringY = 0;

// Updated mouse move handler with quantum effects
const onMouseMove = (e: MouseEvent) => {
  mouseX = e.clientX;
  mouseY = e.clientY;

  // Check what element we're hovering
  const target = e.target as HTMLElement;
  
  if (cursor.value) {
    // Change cursor style based on element type
    if (target.tagName === 'BUTTON' || 
        target.tagName === 'A' || 
        target.closest('.btn') ||
        target.closest('.holographic-card') ||
        target.closest('.interactive')) {
      cursor.value.style.width = '48px';
      cursor.value.style.height = '48px';
      cursor.value.style.borderColor = 'var(--color-pink-500)';
      cursor.value.style.mixBlendMode = 'difference';
      
      // Add quantum shifting hue effect
      cursor.value.style.setProperty('--hue-primary', '280deg');
      cursor.value.style.setProperty('--hue-secondary', '160deg');
    } else {
      cursor.value.style.width = '24px';
      cursor.value.style.height = '24px';
      cursor.value.style.borderColor = 'var(--color-cyan-500)';
      cursor.value.style.mixBlendMode = 'difference';
      
      // Reset quantum hue
      cursor.value.style.setProperty('--hue-primary', '250deg');
      cursor.value.style.setProperty('--hue-secondary', '190deg');
    }
  }
  
  if (cursorRing.value) {
    // Expand ring on interactive elements
    if (target.tagName === 'BUTTON' || 
        target.tagName === 'A' || 
        target.closest('.btn') ||
        target.closest('.holographic-card') ||
        target.closest('.interactive')) {
      cursorRing.value.style.transform = 'translate(-50%, -50%) scale(1.5)';
      cursorRing.value.style.opacity = '0.6';
    } else {
      cursorRing.value.style.transform = 'translate(-50%, -50%) scale(1)';
      cursorRing.value.style.opacity = '0.3';
    }
  }
};

const updateCursor = () => {
  // Update dot position - follows mouse exactly
  dotX = mouseX;
  dotY = mouseY;
  
  // Update cursor with slight delay for smooth effect
  cursorX += (mouseX - cursorX) * 0.1;
  cursorY += (mouseY - cursorY) * 0.1;
  
  // Update ring with even more delay for trailing effect
  ringX += (mouseX - ringX) * 0.05;
  ringY += (mouseY - ringY) * 0.05;
  
  if (cursorDot.value) {
    cursorDot.value.style.transform = `translate3d(${dotX}px, ${dotY}px, 0)`;
  }
  
  if (cursor.value) {
    cursor.value.style.transform = `translate3d(${cursorX}px, ${cursorY}px, 0)`;
  }
  
  if (cursorRing.value) {
    cursorRing.value.style.left = `${ringX}px`;
    cursorRing.value.style.top = `${ringY}px`;
  }
  
  requestAnimationFrame(updateCursor);
};

onMounted(() => {
  window.addEventListener('mousemove', onMouseMove);
  updateCursor();
});

onUnmounted(() => {
  window.removeEventListener('mousemove', onMouseMove);
});
</script>

<style>
.custom-cursor-dot {
  width: 6px;
  height: 6px;
  background-color: var(--color-cyan-500);
  border-radius: 50%;
  position: fixed;
  transform: translate(-50%, -50%);
  pointer-events: none;
  z-index: 9999;
  transition: transform 0.1s;
}

.custom-cursor {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  border: 2px solid var(--color-cyan-500);
  position: fixed;
  transform: translate(-50%, -50%);
  pointer-events: none;
  transition: width 0.3s, height 0.3s, border-color 0.3s;
  z-index: 9999;
  mix-blend-mode: difference;
}

.custom-cursor-ring {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: radial-gradient(
    circle,
    rgba(var(--hue-primary), 0.3) 0%,
    rgba(var(--hue-secondary), 0) 70%
  );
  position: fixed;
  pointer-events: none;
  z-index: 9998;
  opacity: 0.3;
  transform: translate(-50%, -50%) scale(1);
  transition: transform 0.3s ease, opacity 0.3s ease;
}
</style>
