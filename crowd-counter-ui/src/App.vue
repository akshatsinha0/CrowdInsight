<template>
  <div id="app" class="app">
    <CustomCursor />
    
    <header class="app-header glass">
      <div class="container flex justify-between items-center">
        <div class="logo">
          <h1 class="logo-text">Crowd<span class="text-gradient">Insight</span></h1>
        </div>
        <nav class="main-nav">
          <ul class="nav-list flex">
            <li><RouterLink to="/" class="nav-link">Root</RouterLink></li>
            <li><RouterLink to="/readme" class="nav-link">ReadMe</RouterLink></li>
            <li><RouterLink to="/repository" class="nav-link">Repository</RouterLink></li>
            <li><RouterLink to="/connect" class="nav-link">Connect()</RouterLink></li>
          </ul>
        </nav>
      </div>
    </header>
    
    <main>
      <RouterView v-slot="{ Component }">
        <Transition name="page" mode="out-in">
          <component :is="Component" />
        </Transition>
      </RouterView>
    </main>
    
    <footer class="app-footer glass">
      <div class="container">
        <div class="footer-grid grid">
          <div class="footer-section">
            <h4>CrowdInsight</h4>
            <p class="footer-description">Advanced crowd analysis platform powered by machine learning</p>
          </div>
          <div class="footer-section">
            <h4>Navigation</h4>
            <ul class="footer-nav">
              <li><RouterLink to="/" class="footer-link">Root</RouterLink></li>
              <li><RouterLink to="/readme" class="footer-link">ReadMe</RouterLink></li>
              <li><RouterLink to="/repository" class="footer-link">Repository</RouterLink></li>
              <li><RouterLink to="/connect" class="footer-link">Connect()</RouterLink></li>
            </ul>
          </div>
          <div class="footer-section">
            <h4>Connect()</h4>
            <ul class="social-links">
              <li><a href="#" class="social-link" aria-label="GitHub"><i class="fa-brands fa-github"></i></a></li>
              <li><a href="#" class="social-link" aria-label="LinkedIn"><i class="fa-brands fa-linkedin"></i></a></li>
              <li><a href="#" class="social-link" aria-label="Twitter"><i class="fa-brands fa-twitter"></i></a></li>
            </ul>
          </div>
        </div>
        <div class="footer-copyright">
          <p>&copy; {{ new Date().getFullYear() }} CrowdInsight. All rights reserved.</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';
import { RouterView, RouterLink } from 'vue-router';
import CustomCursor from '@/components/ui/CustomCursor.vue';
const isScrolled = ref(false);

const handleScroll = () => {
  isScrolled.value = window.scrollY > 50;
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll);
});

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll);
});
</script>

<style>
@import '@/assets/styles/global.css';
@import '@/assets/styles/quantum-variables.css';

.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-image: radial-gradient(
    circle at 80% 20%,
    color-mix(in srgb, var(--color-deep-blue-800) 70%, var(--color-purple-700)),
    var(--color-deep-blue-900)
  );
}

.app-header {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 100;
  padding: var(--space-3) 0;
  backdrop-filter: blur(8px);
  box-shadow: var(--depth-1);
  transition: all 0.4s cubic-bezier(0.68, -0.55, 0.27, 1.55);
}

.app-header.scrolled {
  padding: var(--space-2) 0;
  background: color-mix(in srgb, var(--color-deep-blue-900) 70%, transparent);
}

/* Update other styles with quantum design system */
.logo-text {
  font-size: var(--font-size-xl);
  font-weight: var(--heading-weight);
  letter-spacing: -0.05em;
  margin: 0;
}

.app-header {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 100;
  padding: var(--space-3) 0;
}

.logo-text {
  font-size: var(--font-size-xl);
  font-weight: var(--font-black);
  letter-spacing: -0.05em;
  margin: 0;
}

.main-nav {
  font-weight: var(--font-medium);
}

.nav-list {
  list-style: none;
  gap: var(--space-5);
}

.nav-link {
  color: var(--color-gray-100);
  text-decoration: none;
  position: relative;
  transition: color var(--transition-normal);
}

.nav-link::after {
  content: '';
  position: absolute;
  width: 0;
  height: 2px;
  bottom: -4px;
  left: 0;
  background-color: var(--color-cyan-500);
  transition: width var(--transition-normal);
}

.nav-link:hover, .nav-link.router-link-active {
  color: var(--color-cyan-500);
}

.nav-link:hover::after, .nav-link.router-link-active::after {
  width: 100%;
}

main {
  flex: 1;
  margin-top: 80px;
}

.app-footer {
  margin-top: auto;
  padding: var(--space-6) 0;
}

.footer-grid {
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: var(--space-6);
}

.footer-nav, .social-links {
  list-style: none;
  padding: 0;
}

.footer-nav li, .social-links li {
  margin-bottom: var(--space-2);
}

.footer-link, .social-link {
  color: var(--color-gray-200);
  text-decoration: none;
  transition: color var(--transition-normal);
}

.footer-link:hover, .social-link:hover {
  color: var(--color-cyan-500);
}

.social-links {
  display: flex;
  gap: var(--space-3);
}

.footer-copyright {
  margin-top: var(--space-6);
  padding-top: var(--space-4);
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  text-align: center;
  font-size: var(--font-size-sm);
  color: var(--color-gray-200);
}

/* Page transitions */
.page-enter-active,
.page-leave-active {
  transition: opacity 0.3s, transform 0.3s;
}

.page-enter-from,
.page-leave-to {
  opacity: 0;
  transform: translateY(10px);
}
</style>
