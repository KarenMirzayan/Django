import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000/api/items/';

const getAuthHeaders = () => ({
  Authorization: `Bearer ${localStorage.getItem('token')}`
});

export const getItems = async () => {
  const response = await axios.get(API_URL, {
    headers: getAuthHeaders()
  });
  return response.data;
};

export const createItem = async (item) => {
  const response = await axios.post(API_URL, item, {
    headers: getAuthHeaders()
  });
  return response.data;
};