// main.ts
import './assets/styles/global.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

// Font Awesome setup - Import from correct packages
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
// Import solid icons from solid package
import { faChartLine, faUsers, faBrain, faTachometerAlt } from '@fortawesome/free-solid-svg-icons'
// Import brand icons from brands package
import { faGithub, faLinkedin, faTwitter } from '@fortawesome/free-brands-svg-icons'
import { initAdaptiveUI } from '@/services/AdaptiveUIService';
import { getGazeManager } from '@/services/GazeManager';

// Add icons to library
library.add(
  // Solid icons
  faChartLine, 
  faUsers, 
  faBrain, 
  faTachometerAlt, 
  // Brand icons
  faGithub, 
  faLinkedin, 
  faTwitter
)

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.component('FontAwesomeIcon', FontAwesomeIcon)

app.mount('#app')
initAdaptiveUI();

const gazeManager = getGazeManager();
gazeManager.initialize();
