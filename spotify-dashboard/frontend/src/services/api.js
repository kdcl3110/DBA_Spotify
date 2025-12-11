import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
});

// Stats endpoints
export const getStats = async () => {
  const response = await api.get('/stats');
  return response.data;
};

// Playlists endpoints
export const getPlaylists = async (filters = {}) => {
  const response = await api.get('/playlists', { params: filters });
  return response.data;
};

export const getPlaylistById = async (id) => {
  const response = await api.get(`/playlists/${id}`);
  return response.data;
};

// Genres endpoints
export const getGenres = async () => {
  const response = await api.get('/genres');
  return response.data;
};

export const getSubgenres = async (genre = null) => {
  const params = genre ? { genre } : {};
  const response = await api.get('/subgenres', { params });
  return response.data;
};

// Tracks endpoints
export const getTracks = async (sortBy = 'popularity', limit = 20) => {
  const response = await api.get('/tracks', { params: { sortBy, limit } });
  return response.data;
};

// Audio features endpoints
export const getAudioFeatures = async (filters = {}) => {
  const response = await api.get('/audio-features', { params: filters });
  return response.data;
};

export default api;
