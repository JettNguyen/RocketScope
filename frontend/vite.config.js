import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  // Use base path only for production builds (GitHub Pages, etc.)
  base: process.env.NODE_ENV === 'production' ? '/RocketScope/' : '/',
  build: {
    outDir: 'dist'
  }
})