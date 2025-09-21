// Frontend configuration - ALL environment variables REQUIRED
const apiBaseUrl = import.meta.env.VITE_API_BASE_URL;

if (!apiBaseUrl) {
  throw new Error("VITE_API_BASE_URL environment variable is required");
}

const config = {
  API_BASE_URL: apiBaseUrl,
  API_ENDPOINTS: {
    AFFIRMATIONS: "/api/affirmations",
    DAILY_DATA: "/api/daily-data",
    TASKS: "/api/tasks",
  },
};

export default config;
