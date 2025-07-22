<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import { ref, onMounted, onUnmounted, watch, computed } from 'vue'
import { useRoute } from 'vue-router'
import LoadingIndicator from './components/LoadingIndicator.vue'
import { usePageStore } from './stores'
import { storeToRefs } from 'pinia'
import { useBloggerData } from './composables/useBloggerData'

const isHeaderScrolled = ref(false)
const isPageLoading = ref(false)
const route = useRoute()

// Pages dropdown functionality
const pagesDropdown = ref<HTMLElement | null>(null)
const isPagesDropdownOpen = ref(false)
const pageStore = usePageStore()
const { pages, isLoading: isLoadingPages, error: pagesError } = storeToRefs(pageStore)

// Get Blogger data if available
const { bloggerData, isInBloggerEnvironment } = useBloggerData()
const siteTitle = computed(() => {
  return isInBloggerEnvironment.value && bloggerData.value.blog.title
    ? bloggerData.value.blog.title
    : 'Vue Blogger SPA'
})

const pagesList = computed(() => pages.value)

const togglePagesDropdown = () => {
  isPagesDropdownOpen.value = !isPagesDropdownOpen.value
}

const closePagesDropdown = () => {
  isPagesDropdownOpen.value = false
}

const handleClickOutside = (event: MouseEvent) => {
  if (pagesDropdown.value && !pagesDropdown.value.contains(event.target as Node)) {
    closePagesDropdown()
  }
}

// Scroll handling
const handleScroll = () => {
  isHeaderScrolled.value = window.scrollY > 10
}

// Show loading indicator on route change
watch(() => route.path, () => {
  isPageLoading.value = true
  closePagesDropdown() // Close dropdown on route change

  // Simulate loading completion (in a real app, this would be based on actual data loading)
  setTimeout(() => {
    isPageLoading.value = false
  }, 800)
})

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
  document.addEventListener('click', handleClickOutside)

  // Load pages data when component is mounted
  pageStore.fetchPages()
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
  document.removeEventListener('click', handleClickOutside)
})

// Function to log blogger data for debugging
const logBloggerData = () => {
  console.log('Blogger Data:', JSON.stringify(bloggerData.value, null, 2))
}
</script>

<template>
  <div class="app">
    <LoadingIndicator :is-loading="isPageLoading" />
    <a href="#main-content" class="skip-to-content">Skip to content</a>
    <header :class="{ 'scrolled': isHeaderScrolled }">
      <div class="header-content">
        <h1 class="site-title">{{ siteTitle }}</h1>
        <nav aria-label="Main navigation">
          <RouterLink to="/">Home</RouterLink>
          <RouterLink to="/about">About</RouterLink>
          <div class="dropdown" ref="pagesDropdown">
            <button
              class="dropdown-toggle"
              @click="togglePagesDropdown"
              @keydown.enter="togglePagesDropdown"
              @keydown.space="togglePagesDropdown"
              aria-haspopup="true"
              :aria-expanded="isPagesDropdownOpen"
            >
              Pages <span class="dropdown-arrow">▾</span>
            </button>
            <ul class="dropdown-menu" v-if="isPagesDropdownOpen" role="menu">
              <li v-if="isLoadingPages" class="dropdown-loading">Loading...</li>
              <li v-else-if="pagesError" class="dropdown-error">Error loading pages</li>
              <li v-else-if="pagesList.length === 0" class="dropdown-empty">No pages available</li>
              <li v-else v-for="page in pagesList" :key="page.id" role="menuitem">
                <RouterLink :to="page.url || `/page/${page.id}`" @click="closePagesDropdown">
                  {{ page.title }}
                </RouterLink>
              </li>
            </ul>
          </div>
        </nav>
      </div>
    </header>

    <main id="main-content">
      <div v-if="isInBloggerEnvironment" class="blogger-context-info">
        <div class="container">
          <p>Running in Blogger: {{ bloggerData.blog.title }}</p>
        </div>
      </div>
      <div class="container">
        <RouterView v-slot="{ Component }">
          <transition name="page" mode="out-in">
            <component :is="Component" />
          </transition>
        </RouterView>
      </div>
    </main>

    <footer>
      <div class="container">
        <p>&copy; {{ new Date().getFullYear() }} {{ siteTitle }}. <button @click="logBloggerData" class="debug-button">Embedded in <span class="debug-text">Blogger</span></button></p>
      </div>
    </footer>
  </div>
</template>

<style>
/* Global Styles */
:root {
  /* Color System */
  --primary-color: #3498db;
  --primary-dark: #2980b9;
  --primary-light: #5dade2;
  --accent-color: #f39c12;
  --success-color: #2ecc71;
  --warning-color: #f39c12;
  --error-color: #e74c3c;
  --text-color: #333;
  --text-secondary: #666;
  --text-muted: #999;
  --bg-color: #f9f9f9;
  --bg-card: #ffffff;
  --border-color: #e1e1e1;

  /* Layout */
  --header-height: 60px;
  --footer-height: 60px;

  /* Typography */
  --font-family: 'Helvetica Neue', Arial, sans-serif;
  --font-size-xs: 0.75rem;    /* 12px */
  --font-size-sm: 0.875rem;   /* 14px */
  --font-size-md: 1rem;       /* 16px */
  --font-size-lg: 1.25rem;    /* 20px */
  --font-size-xl: 1.5rem;     /* 24px */
  --font-size-xxl: 2rem;      /* 32px */
  --line-height-tight: 1.2;
  --line-height-normal: 1.6;
  --font-weight-normal: 400;
  --font-weight-medium: 500;
  --font-weight-bold: 700;

  /* Spacing */
  --spacing-xs: 0.25rem;      /* 4px */
  --spacing-sm: 0.5rem;       /* 8px */
  --spacing-md: 1rem;         /* 16px */
  --spacing-lg: 1.5rem;       /* 24px */
  --spacing-xl: 2rem;         /* 32px */
  --spacing-xxl: 3rem;        /* 48px */

  /* UI Elements */
  --border-radius-sm: 2px;
  --border-radius: 4px;
  --border-radius-lg: 8px;
  --border-radius-pill: 9999px;
  --box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  --box-shadow-md: 0 4px 8px rgba(0, 0, 0, 0.1);
  --box-shadow-lg: 0 8px 16px rgba(0, 0, 0, 0.1);

  /* Animation */
  --transition-speed: 0.2s;
  --transition-timing: ease;
}

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: var(--font-family);
  line-height: var(--line-height-normal);
  color: var(--text-color);
  background: var(--bg-color);
  font-size: var(--font-size-md);
  overflow-x: hidden;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  transition: all var(--transition-speed) var(--transition-timing);
  background-color: var(--bg-color);
  position: relative;
  overflow-x: hidden;
}

header {
  background-color: var(--bg-card);
  border-bottom: 1px solid var(--border-color);
  padding: var(--spacing-md) 0;
  box-shadow: var(--box-shadow);
  position: sticky;
  top: 0;
  z-index: 100;
  transition: box-shadow var(--transition-speed) var(--transition-timing);
}

header.scrolled {
  box-shadow: var(--box-shadow-md);
}

.container {
  width: 100%;
  max-width: 1000px;
  margin: 0 auto;
  padding: 0 var(--spacing-md);
}

@media (max-width: 768px) {
  .container {
    padding: 0 var(--spacing-sm);
  }
}

.header-content {
  max-width: 1000px;
  margin: 0 auto;
  padding: 0 var(--spacing-md);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

@media (max-width: 480px) {
  .header-content {
    flex-direction: column;
    gap: var(--spacing-sm);
    text-align: center;
  }
}

.site-title {
  color: var(--primary-color);
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-bold);
  margin: 0;
  letter-spacing: -0.5px;
  transition: transform var(--transition-speed) var(--transition-timing);
}

.site-title:hover {
  transform: translateY(-1px);
}

nav {
  display: flex;
  gap: var(--spacing-lg);
}

@media (max-width: 480px) {
  nav {
    gap: var(--spacing-md);
    flex-direction: column;
    align-items: center;
  }
}

nav a {
  text-decoration: none;
  color: var(--text-color);
  font-weight: var(--font-weight-medium);
  transition: color var(--transition-speed) var(--transition-timing),
              transform var(--transition-speed) var(--transition-timing);
  padding: var(--spacing-xs) var(--spacing-sm);
  border-radius: var(--border-radius);
  position: relative;
  font-size: var(--font-size-md);
}

nav a:hover {
  color: var(--primary-color);
  transform: translateY(-2px);
}

nav a.router-link-active {
  color: var(--primary-color);
}

nav a.router-link-active::after {
  content: '';
  position: absolute;
  bottom: -3px;
  left: 0;
  width: 100%;
  height: 2px;
  background-color: var(--primary-color);
  transform: scaleX(0.8);
  transition: transform var(--transition-speed) var(--transition-timing);
}

nav a.router-link-active:hover::after {
  transform: scaleX(1);
}

/* Dropdown styles */
.dropdown {
  position: relative;
  display: inline-block;
}

.dropdown-toggle {
  background: none;
  border: none;
  color: var(--text-color);
  font-weight: var(--font-weight-medium);
  font-size: var(--font-size-md);
  padding: var(--spacing-xs) var(--spacing-sm);
  cursor: pointer;
  border-radius: var(--border-radius);
  transition: color var(--transition-speed) var(--transition-timing),
              transform var(--transition-speed) var(--transition-timing);
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
}

.dropdown-toggle:hover {
  color: var(--primary-color);
  transform: translateY(-2px);
}

.dropdown-arrow {
  font-size: 0.8em;
  transition: transform var(--transition-speed) var(--transition-timing);
}

.dropdown-toggle:hover .dropdown-arrow {
  transform: translateY(2px);
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  left: 0;
  z-index: 1000;
  min-width: 180px;
  padding: var(--spacing-xs) 0;
  margin: var(--spacing-xs) 0 0;
  background-color: var(--bg-card);
  border-radius: var(--border-radius);
  box-shadow: var(--box-shadow-md);
  list-style: none;
}

.dropdown-menu li {
  padding: 0;
}

.dropdown-menu a {
  padding: var(--spacing-sm) var(--spacing-md);
  display: block;
  text-decoration: none;
  color: var(--text-color);
  transition: background-color var(--transition-speed) var(--transition-timing),
              color var(--transition-speed) var(--transition-timing);
  font-size: var(--font-size-sm);
}

.dropdown-menu a:hover {
  background-color: rgba(0, 0, 0, 0.03);
  color: var(--primary-color);
  transform: translateX(3px);
}

.dropdown-loading,
.dropdown-error,
.dropdown-empty {
  padding: var(--spacing-sm) var(--spacing-md);
  color: var(--text-muted);
  font-size: var(--font-size-sm);
}

.dropdown-error {
  color: var(--error-color);
}

main {
  flex: 1;
  padding: var(--spacing-xl) 0;
  min-height: 50vh;
  background-color: var(--bg-color);
  position: relative;
}

main::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 6px;
  background: linear-gradient(to right, var(--primary-color), var(--accent-color));
  opacity: 0.1;
}

@media (max-width: 768px) {
  main {
    padding: var(--spacing-lg) 0;
  }
}

footer {
  background-color: var(--bg-card);
  border-top: 1px solid var(--border-color);
  padding: var(--spacing-lg) 0;
  text-align: center;
  color: var(--text-secondary);
  font-size: var(--font-size-sm);
  position: relative;
}

footer::before {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(to right, var(--primary-color), var(--accent-color));
  opacity: 0.05;
}

footer p {
  margin: 0;
}

/* Accessibility Focus Styles */
:focus {
  outline: 2px solid var(--primary-color);
  outline-offset: 2px;
  transition: outline-offset var(--transition-speed) var(--transition-timing);
}

:focus:not(:focus-visible) {
  outline: none;
}

:focus-visible {
  outline: 2px solid var(--primary-color);
  outline-offset: 2px;
}

/* Skip to content for keyboard users */
.skip-to-content {
  position: absolute;
  left: -9999px;
  z-index: 999;
  padding: var(--spacing-sm) var(--spacing-md);
  background: var(--primary-color);
  color: white;
  text-decoration: none;
  border-radius: 0 0 var(--border-radius) var(--border-radius);
  font-weight: var(--font-weight-medium);
  box-shadow: var(--box-shadow-md);
  transition: transform var(--transition-speed) var(--transition-timing);
}

/* Page transitions */
.page-enter-active,
.page-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.page-enter-from {
  opacity: 0;
  transform: translateY(10px);
}

.page-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* Loader animation for progress indication */
@keyframes pulse {
  0% { opacity: 0.6; }
  50% { opacity: 1; }
  100% { opacity: 0.6; }
}

.loading-indicator {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(to right, var(--primary-color), var(--accent-color));
  z-index: 9999;
  animation: pulse 1.5s infinite;
  transform-origin: left;
}

/* Blogger context info */
.blogger-context-info {
  background-color: rgba(0, 0, 0, 0.05);
  padding: 8px 0;
  font-size: 0.8rem;
  color: var(--text-muted);
  margin-bottom: 1rem;
}

/* Debug button style */
.debug-button {
  background: none;
  border: none;
  color: var(--text-secondary);
  font-size: var(--font-size-sm);
  cursor: pointer;
  padding: 0;
  font-family: var(--font-family);
  transition: color var(--transition-speed) var(--transition-timing);
  display: inline-flex;
  align-items: center;
}

.debug-button:hover {
  color: var(--primary-color);
}

.debug-text {
  text-decoration: underline;
  text-decoration-style: dotted;
}
</style>
