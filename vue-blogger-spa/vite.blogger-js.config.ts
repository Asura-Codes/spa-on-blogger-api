import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// Special Vite config for Blogger JavaScript output
export default defineConfig({
  plugins: [
    vue(),
  ],
  base: './', // Use relative base path
  build: {
    outDir: 'dist-blogger',
    assetsDir: '',
    rollupOptions: {
      input: 'src/main.ts',
      output: {
        entryFileNames: 'index.[hash].js',
        format: 'iife',
        // Make sure to include all CSS in the JS file
        inlineDynamicImports: true
      },
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
