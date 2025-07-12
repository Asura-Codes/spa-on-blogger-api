import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { viteSingleFile } from 'vite-plugin-singlefile'

// Special Vite config for Blogger
// This creates a single HTML file with all assets inlined
export default defineConfig({
  plugins: [
    vue(),
    viteSingleFile(), // Plugin to inline all assets
  ],
  base: './', // Use relative base path
  build: {
    outDir: 'dist-blogger', // Output to a separate directory
    // The following settings help with inlining and optimization
    assetsInlineLimit: 100000000, // Inline all assets
    cssCodeSplit: false, // Don't split CSS
    rollupOptions: {
      // Make sure no external dependencies are left out
      external: [],
    },
  },
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
})
