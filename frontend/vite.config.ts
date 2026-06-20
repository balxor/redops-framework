import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "node:path";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  server: {
    port: 5173,
    host: true,
    // On WSL when the project lives on the Windows drive (/mnt/c/...), the
    // native file watcher misses changes. Set VITE_USE_POLLING=true to fix HMR.
    watch: process.env.VITE_USE_POLLING === "true" ? { usePolling: true, interval: 300 } : undefined,
    // Proxy API calls to the backend during development so the browser talks
    // to the Vite origin and avoids CORS. Override the target via VITE_API_TARGET.
    proxy: {
      "/api": {
        target: process.env.VITE_API_TARGET ?? "http://localhost:8000",
        changeOrigin: true,
      },
    },
  },
});
