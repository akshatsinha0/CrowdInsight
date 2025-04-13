// Create this new file for adaptive UI functionality
import { reactive } from 'vue';

// Adaptive UI state
export const adaptiveState = reactive({
  contentDensity: 'normal', // 'sparse', 'normal', 'dense'
  userExpertise: 'beginner', // 'beginner', 'intermediate', 'expert'
  preferredVisualization: '2d', // '2d', '3d', 'heatmap'
  colorBlindMode: false,
  isLargeDisplay: false,
  touchMode: false,
});

// Layout containers being observed
const observedElements = new Set<Element>();

// Interface to store element dimension history
interface ElementHistory {
  element: Element;
  dimensionHistory: { width: number; height: number; time: number }[];
}

// Keep track of element dimension history
const elementHistories = new Map<string, ElementHistory>();

// Resize observer
const resizeObserver = new ResizeObserver((entries) => {
  // Process resize information
  for (const entry of entries) {
    const elementId = entry.target.id || Math.random().toString(36).substring(2, 9);
    
    // Create history if it doesn't exist
    if (!elementHistories.has(elementId)) {
      elementHistories.set(elementId, {
        element: entry.target,
        dimensionHistory: [],
      });
    }
    
    // Add to history
    const history = elementHistories.get(elementId)!;
    history.dimensionHistory.push({
      width: entry.contentRect.width,
      height: entry.contentRect.height,
      time: Date.now(),
    });
    
    // Keep only last 10 entries
    if (history.dimensionHistory.length > 10) {
      history.dimensionHistory.shift();
    }
    
    // Detect if content is becoming too dense
    analyzeContentDensity(entry.target);
  }
});

// Intersection observer for visibility
const visibilityObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      // Element is visible, apply appropriate animations or optimizations
      entry.target.classList.add('in-viewport');
    } else {
      entry.target.classList.remove('in-viewport');
    }
  });
}, { threshold: 0.1 }); // 10% visibility threshold

// Analyze content density based on child elements
function analyzeContentDensity(element: Element) {
  const childCount = element.children.length;
  const area = element.clientWidth * element.clientHeight;
  
  // Calculate density score (children per 1000px²)
  const densityScore = (childCount * 1000) / area;
  
  // Update adaptive state based on density
  if (densityScore > 1) {
    adaptiveState.contentDensity = 'dense';
  } else if (densityScore < 0.2) {
    adaptiveState.contentDensity = 'sparse';
  } else {
    adaptiveState.contentDensity = 'normal';
  }
  
  // Apply appropriate CSS class
  element.classList.remove('content-dense', 'content-sparse', 'content-normal');
  element.classList.add(`content-${adaptiveState.contentDensity}`);
}

// Start observing an element for adaptive UI
export function observeElement(element: Element): void {
  if (!observedElements.has(element)) {
    resizeObserver.observe(element);
    visibilityObserver.observe(element);
    observedElements.add(element);
  }
}

// Stop observing an element
export function unobserveElement(element: Element): void {
  if (observedElements.has(element)) {
    resizeObserver.unobserve(element);
    visibilityObserver.unobserve(element);
    observedElements.delete(element);
  }
}

// Detect device capabilities
export function detectDeviceCapabilities(): void {
  // Check display size
  adaptiveState.isLargeDisplay = window.innerWidth >= 1440;
  
  // Check for touch support
  adaptiveState.touchMode = 'ontouchstart' in window || 
    navigator.maxTouchPoints > 0;
  
  // Listen for orientation changes
  window.addEventListener('resize', () => {
    adaptiveState.isLargeDisplay = window.innerWidth >= 1440;
  });
}

// Initialize adaptive UI service
export function initAdaptiveUI(): void {
  detectDeviceCapabilities();
  
  // Analyze user behavior over time to determine expertise level
  let interactionCount = 0;
  document.addEventListener('click', () => {
    interactionCount++;
    if (interactionCount > 50) {
      adaptiveState.userExpertise = 'intermediate';
    }
    if (interactionCount > 150) {
      adaptiveState.userExpertise = 'expert';
    }
  });
}
