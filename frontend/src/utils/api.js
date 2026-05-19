import axios from 'axios';

// URL del backend (cambiar según donde esté deployed)
const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json'
  }
});

export const sendEmergency = async (emergency) => {
  try {
    const response = await api.post('/webhook/emergency', emergency);
    return response.data;
  } catch (error) {
    console.error('Error sending emergency:', error);
    throw error;
  }
};

export const getStats = async () => {
  try {
    const response = await api.get('/stats');
    return response.data;
  } catch (error) {
    console.error('Error getting stats:', error);
    return {
      total_emergencies: 0,
      insured_count: 0,
      uninsured_count: 0,
      high_risk_count: 0
    };
  }
};

export const getAlerts = async () => {
  try {
    const response = await api.get('/alerts/recent');
    return Array.isArray(response.data) ? response.data : [];
  } catch (error) {
    console.error('Error getting alerts:', error);
    return [];
  }
};

