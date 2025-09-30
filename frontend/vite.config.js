import { defineConfig, loadEnv } from "vite";
import react from "@vitejs/plugin-react";

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), "");
  const apiBaseUrl = env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000";
  const tailscaleHost = env.TAILSCALE_HOST ?? "";

  return {
    plugins: [react()],
    server: {
      host: true,
      allowedHosts: [
        tailscaleHost
      ],
      proxy: {
        "/api": {
          target: apiBaseUrl,
          changeOrigin: true,
          secure: apiBaseUrl.startsWith("https"),
        },
      },
    },
  };
});
