<template>
    <div class="image-uploader" :class="{ 'drag-over': isDragOver }">
      <div 
        class="upload-area"
        @dragover.prevent="handleDragOver"
        @dragleave.prevent="handleDragLeave" 
        @drop.prevent="handleDrop"
        @click="triggerFileInput"
      >
        <input 
          type="file"
          ref="fileInput"
          class="visually-hidden"
          accept="image/*"
          @change="handleFileSelect"
        >
        
        <div v-if="!selectedImage && !isLoading" class="upload-placeholder">
          <div class="upload-icon">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
              <polyline points="17 8 12 3 7 8"></polyline>
              <line x1="12" y1="3" x2="12" y2="15"></line>
            </svg>
          </div>
          <h3>Upload Crowd Image</h3>
          <p>Drag and drop an image here or click to select</p>
          <p class="supported-formats">Supported formats: JPG, PNG, WEBP</p>
        </div>
        
        <div v-if="isLoading" class="upload-loading">
          <div class="loader"></div>
          <p>Analyzing crowd density...</p>
        </div>
        
        <div v-if="selectedImage && !isLoading" class="upload-preview">
          <img :src="previewUrl" alt="Selected image" class="preview-image">
          <div class="preview-controls">
            <button @click.stop="clearImage" class="btn btn-secondary">
              Clear
            </button>
            <button @click.stop="analyzeImage" class="btn btn-accent">
              Analyze
            </button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref, defineEmits } from 'vue';
  
  const emit = defineEmits(['image-selected', 'upload-complete']);
  
  const fileInput = ref<HTMLInputElement | null>(null);
  const selectedImage = ref<File | null>(null);
  const previewUrl = ref<string>('');
  const isDragOver = ref(false);
  const isLoading = ref(false);
  
  const triggerFileInput = () => {
    if (fileInput.value) {
      fileInput.value.click();
    }
  };
  
  const handleFileSelect = (event: Event) => {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
      processFile(input.files[0]);
    }
  };
  
  const handleDragOver = (event: DragEvent) => {
    isDragOver.value = true;
  };
  
  const handleDragLeave = (event: DragEvent) => {
    isDragOver.value = false;
  };
  
  const handleDrop = (event: DragEvent) => {
    isDragOver.value = false;
    if (event.dataTransfer?.files.length) {
      processFile(event.dataTransfer.files[0]);
    }
  };
  
  const processFile = (file: File) => {
    // Check if file is an image
    if (!file.type.match('image.*')) {
      alert('Please select an image file');
      return;
    }
    
    selectedImage.value = file;
    previewUrl.value = URL.createObjectURL(file);
    emit('image-selected', file);
  };
  
  const clearImage = (event: Event) => {
    event.stopPropagation();
    selectedImage.value = null;
    previewUrl.value = '';
    if (fileInput.value) {
      fileInput.value.value = '';
    }
  };
  
  const analyzeImage = async (event: Event) => {
    event.stopPropagation();
    if (!selectedImage.value) return;
    
    isLoading.value = true;
    
    try {
      // Create form data for API request
      const formData = new FormData();
      formData.append('image', selectedImage.value);
      
      // Here you would typically make an API call to your backend
      // For demonstration, let's simulate an API call
      setTimeout(() => {
        // Mock response
        const mockResponse = {
          count: 1247,
          density_map: 'base64_encoded_image_data',
          hotspots: [
            { center: [120, 150], intensity: 0.8, area: 450 },
            { center: [380, 210], intensity: 0.6, area: 320 },
            { center: [560, 180], intensity: 0.7, area: 380 }
          ],
          distribution: {
            pattern: 'Clustered',
            center_of_mass: [350, 200],
            uniformity: 0.65
          },
          crowd_type: 'Dense Gathering',
          risk_level: { level: 'Moderate', score: 0.58 }
        };
        
        isLoading.value = false;
        emit('upload-complete', mockResponse);
      }, 2000);
      
    } catch (error) {
      console.error('Error analyzing image:', error);
      isLoading.value = false;
      alert('An error occurred while analyzing the image. Please try again.');
    }
  };
  </script>
  
  <style scoped>
  .image-uploader {
    width: 100%;
  }
  
  .upload-area {
    border: 2px dashed rgba(255, 255, 255, 0.2);
    border-radius: var(--radius-lg);
    padding: var(--space-6);
    text-align: center;
    cursor: pointer;
    transition: all var(--transition-normal);
    background-color: rgba(30, 41, 59, 0.4);
  }
  
  .upload-area:hover, .drag-over .upload-area {
    border-color: var(--color-cyan-500);
    background-color: rgba(30, 41, 59, 0.6);
  }
  
  .upload-icon {
    width: 64px;
    height: 64px;
    margin: 0 auto var(--space-4);
    color: var(--color-cyan-500);
  }
  
  .upload-icon svg {
    width: 100%;
    height: 100%;
  }
  
  .supported-formats {
    font-size: var(--font-size-xs);
    color: var(--color-gray-200);
    margin-top: var(--space-3);
  }
  
  .upload-preview {
    position: relative;
  }
  
  .preview-image {
    max-width: 100%;
    max-height: 400px;
    border-radius: var(--radius-md);
    object-fit: contain;
  }
  
  .preview-controls {
    margin-top: var(--space-4);
    display: flex;
    justify-content: center;
    gap: var(--space-4);
  }
  
  .upload-loading {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: var(--space-6);
  }
  
  .loader {
    border: 3px solid rgba(255, 255, 255, 0.1);
    border-radius: 50%;
    border-top: 3px solid var(--color-cyan-500);
    width: 40px;
    height: 40px;
    animation: spin 1s linear infinite;
    margin-bottom: var(--space-4);
  }
  
  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
  </style>
  