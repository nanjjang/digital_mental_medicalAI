import { sveltekit } from '@sveltejs/kit/vite';

const config = {
  plugins: [sveltekit()],
  server: {
    proxy: {
      '/api': 'http://localhost:8000'
    }
  }
};

export default config;