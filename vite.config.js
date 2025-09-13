import { defineConfig } from 'vite';
import { resolve } from 'path';
import { createHtmlPlugin } from 'vite-plugin-html';

export default defineConfig({
  root: 'src',
  plugins: [
    createHtmlPlugin({
      minify: true,
      pages: [
        {
          entry: 'scripts/main.js',
          filename: 'index.html',
          template: 'pages/index.html',
          injectOptions: {
            data: {
              title: 'Square Transport - AI Delivery Robots',
              description: 'Revolutionary autonomous delivery robots powered by vision-only AI navigation'
            }
          }
        },
        {
          entry: 'scripts/main.js',
          filename: 'overview.html',
          template: 'pages/overview.html',
          injectOptions: {
            data: {
              title: 'Product Overview - Square Transport',
              description: 'Detailed overview of Square Transport\'s autonomous delivery robots'
            }
          }
        },
        {
          entry: 'scripts/main.js',
          filename: 'about.html',
          template: 'pages/about.html',
          injectOptions: {
            data: {
              title: 'About Us - Square Transport',
              description: 'Meet the passionate team behind Square Transport\'s delivery revolution'
            }
          }
        }
      ]
    })
  ],
  publicDir: '../public',
  build: {
    outDir: '../dist',
    emptyOutDir: true, // Enable automatic cleanup of output directory
    rollupOptions: {
      input: {
        main: resolve(__dirname, 'src/pages/index.html'),
        overview: resolve(__dirname, 'src/pages/overview.html'),
        about: resolve(__dirname, 'src/pages/about.html')
      }
    }
  },
  server: {
    port: 3000,
    open: true
  }
});
