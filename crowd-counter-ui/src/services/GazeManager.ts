// Create this new service for gaze tracking and ambient interactions
export class GazeManager {
    private gazeX: number = 0;
    private gazeY: number = 0;
    private focusStart: number = 0;
    private focusElement: Element | null = null;
    private tracking: boolean = false;
    private webcam: MediaStream | null = null;
    private initialized: boolean = false;
    
    // Event listeners
    private listeners: {
      [eventName: string]: ((event: CustomEvent) => void)[]
    } = {
      'gazemove': [],
      'gazefocus': [],
      'gazeblur': []
    };
    
    constructor() {
      // Initialize mouse tracking as a fallback
      document.addEventListener('mousemove', this.handleMouseMove.bind(this));
    }
    
    // Start real gaze tracking if supported
    async initialize(): Promise<boolean> {
      if (this.initialized) return true;
      
      try {
        // Check for webcam access
        this.webcam = await navigator.mediaDevices.getUserMedia({ 
          video: { 
            width: { ideal: 640 },
            height: { ideal: 480 },
            facingMode: 'user'
          } 
        });
        
        // In a real implementation, we would use face-api.js, WebGazer, or a custom model
        // to track eye movements. For this implementation, we'll use mouse as proxy.
        
        this.tracking = true;
        this.initialized = true;
        
        console.log('Gaze tracking initialized (simulated with mouse)');
        return true;
      } catch (error) {
        console.error('Failed to initialize gaze tracking:', error);
        return false;
      }
    }
    
    // Handle mouse movement (proxy for gaze)
    private handleMouseMove(e: MouseEvent): void {
      if (!this.tracking) return;
      
      this.gazeX = e.clientX;
      this.gazeY = e.clientY;
      
      // Dispatch gazemove event
      this.dispatchGazeEvent('gazemove', {
        x: this.gazeX,
        y: this.gazeY,
        timestamp: Date.now()
      });
      
      // Check for elements beneath the gaze
      this.checkElementFocus();
    }
    
    // Check if we're focusing on an element
    private checkElementFocus(): void {
      const element = document.elementFromPoint(this.gazeX, this.gazeY);
      
      if (element !== this.focusElement) {
        if (this.focusElement) {
          // Dispatch gazeblur event on previous element
          this.dispatchGazeEvent('gazeblur', {
            element: this.focusElement,
            duration: Date.now() - this.focusStart,
            x: this.gazeX,
            y: this.gazeY
          });
        }
        
        this.focusElement = element;
        this.focusStart = Date.now();
        
        if (element) {
          // Dispatch gazefocus event on new element
          this.dispatchGazeEvent('gazefocus', {
            element,
            x: this.gazeX,
            y: this.gazeY
          });
        }
      } else if (element && Date.now() - this.focusStart > 1000) {
        // Dispatch continuous focus updates for long gazes
        this.dispatchGazeEvent('gazefocus', {
          element,
          x: this.gazeX,
          y: this.gazeY,
          focusDuration: Date.now() - this.focusStart
        });
      }
    }
    
    // Dispatch custom gaze events
    private dispatchGazeEvent(eventName: string, detail: any): void {
      // Call all registered listeners
      this.listeners[eventName]?.forEach(listener => {
        listener(new CustomEvent(eventName, { detail }));
      });
      
      // Also dispatch on document for global listeners
      document.dispatchEvent(new CustomEvent(eventName, { detail }));
    }
    
    // Add event listener
    addEventListener(eventName: string, callback: (event: CustomEvent) => void): void {
      if (!this.listeners[eventName]) {
        this.listeners[eventName] = [];
      }
      this.listeners[eventName].push(callback);
    }
    
    // Remove event listener
    removeEventListener(eventName: string, callback: (event: CustomEvent) => void): void {
      if (this.listeners[eventName]) {
        this.listeners[eventName] = this.listeners[eventName].filter(
          listener => listener !== callback
        );
      }
    }
    
    // Disable tracking
    stop(): void {
      this.tracking = false;
      
      if (this.webcam) {
        this.webcam.getTracks().forEach(track => track.stop());
        this.webcam = null;
      }
    }
    
    // Get current gaze position
    getGazePosition(): { x: number, y: number } {
      return { x: this.gazeX, y: this.gazeY };
    }
  }
  
  // Singleton instance
  let gazeManagerInstance: GazeManager | null = null;
  
  // Get gaze manager instance
  export function getGazeManager(): GazeManager {
    if (!gazeManagerInstance) {
      gazeManagerInstance = new GazeManager();
    }
    return gazeManagerInstance;
  }
  