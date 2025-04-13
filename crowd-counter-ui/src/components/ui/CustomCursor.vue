<template>
    <div>
      <div ref="cursorDot" class="custom-cursor-dot"></div>
      <div ref="cursor" class="custom-cursor"></div>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref, onMounted, onUnmounted } from 'vue';
  
  const cursor = ref<HTMLElement | null>(null);
  const cursorDot = ref<HTMLElement | null>(null);
  let mouseX = 0;
  let mouseY = 0;
  let dotX = 0;
  let dotY = 0;
  let cursorX = 0;
  let cursorY = 0;
  
  // Track hover states for different elements
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
          target.closest('.card') ||
          target.closest('.interactive')) {
        cursor.value.style.width = '48px';
        cursor.value.style.height = '48px';
        cursor.value.style.borderColor = 'var(--color-pink-500)';
      } else {
        cursor.value.style.width = '24px';
        cursor.value.style.height = '24px';
        cursor.value.style.borderColor = 'var(--color-cyan-500)';
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
    
    if (cursorDot.value) {
      cursorDot.value.style.transform = `translate3d(${dotX}px, ${dotY}px, 0)`;
    }
    
    if (cursor.value) {
      cursor.value.style.transform = `translate3d(${cursorX}px, ${cursorY}px, 0)`;
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
  