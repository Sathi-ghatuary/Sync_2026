import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const titleApi = {
  // Verify a title
  verify: async (title) => {
    try {
      const response = await api.post('/verify', { title });
      return response.data;
    } catch (error) {
      throw error.response?.data || error.message;
    }
  },

  // Submit an application
  submitApplication: async (title, userEmail) => {
    try {
      const response = await api.post('/application', {
        title,
        user_email: userEmail,
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || error.message;
    }
  },

  // Get user applications
  getUserApplications: async (userEmail) => {
    try {
      const response = await api.get(`/applications/${userEmail}`);
      return response.data;
    } catch (error) {
      throw error.response?.data || error.message;
    }
  },

  // Get database stats
  getStats: async () => {
    try {
      const response = await api.get('/database/stats');
      return response.data;
    } catch (error) {
      throw error.response?.data || error.message;
    }
  },

  // Health check
  healthCheck: async () => {
    try {
      const response = await api.get('/health');
      return response.data;
    } catch (error) {
      throw error.response?.data || error.message;
    }
  },

  // Upload CSV file
  uploadCSV: async (file) => {
    try {
      const formData = new FormData();
      formData.append('file', file);
      const response = await api.post('/database/ingest/csv', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || error.message;
    }
  },
};

export default api;
