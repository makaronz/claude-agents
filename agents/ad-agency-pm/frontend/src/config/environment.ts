interface AppConfig {
  API_URL: string;
  WS_URL: string;
  ENVIRONMENT: 'development' | 'staging' | 'production';
}

const config: AppConfig = {
  API_URL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  WS_URL: import.meta.env.VITE_WS_URL || 'ws://localhost:8000',
  ENVIRONMENT: (import.meta.env.MODE as AppConfig['ENVIRONMENT']) || 'development',
};

export default config;
