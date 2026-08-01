import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const api = axios.create({
  baseURL: `${API_BASE_URL}/api/v1`,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Campaign API endpoints
export const campaignApi = {
  list: () => api.get('/campaigns/'),
  create: (data: any) => api.post('/campaigns/', data),
  get: (id: string) => api.get(`/campaigns/${id}`),
};

// Troubleshooter API endpoints
export const troubleshootApi = {
  diagnose: (data: any) => api.post('/troubleshoot/', data),
  library: () => api.get('/troubleshoot/library'),
};

// Creative API endpoints
export const creativeApi = {
  generate: (data: any) => api.post('/creative/generate', data),
};

// Analytics API endpoints
export const analyticsApi = {
  dashboard: () => api.get('/analytics/dashboard'),
  gaql: (query: string) => api.post('/analytics/gaql', { query }),
};

// CodeGen API endpoints
export const codegenApi = {
  generate: (data: any) => api.post('/codegen/', data),
};

// Agents API endpoints
export const agentsApi = {
  run: (data: any) => api.post('/agents/run', data),
};
