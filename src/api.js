import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:5000', // Replace with your Flask API base URL
});

export default api;
