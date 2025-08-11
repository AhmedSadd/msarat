import React, { useEffect, useState, useCallback } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:8000',
});

apiClient.interceptors.request.use(config => {
  const token = localStorage.getItem('authToken');
  if (token) {
    config.headers.Authorization = `Token ${token}`;
  }
  return config;
});

function Dashboard() {
  const [workplaces, setWorkplaces] = useState([]);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  // State for the form
  const [form, setForm] = useState({ id: null, name: '', address: '', latitude: 0, longitude: 0 });

  const fetchWorkplaces = useCallback(async () => {
    try {
      const response = await apiClient.get('/api/workplaces/');
      setWorkplaces(response.data);
    } catch (err) {
      setError('Failed to fetch workplaces.');
      if (err.response && (err.response.status === 401 || err.response.status === 403)) {
          navigate('/login');
      }
    }
  }, [navigate]);

  useEffect(() => {
    fetchWorkplaces();
  }, [fetchWorkplaces]);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setForm({ ...form, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const { id, ...data } = form;
    try {
      if (id) {
        // Update
        await apiClient.put(`/api/workplaces/${id}/`, data);
      } else {
        // Create
        await apiClient.post('/api/workplaces/', data);
      }
      setForm({ id: null, name: '', address: '', latitude: 0, longitude: 0 }); // Reset form
      fetchWorkplaces(); // Refresh list
    } catch (err) {
      setError('Failed to save workplace. You may not have admin rights.');
    }
  };

  const handleEdit = (wp) => {
    setForm(wp);
  };

  const handleDelete = async (id) => {
    try {
      await apiClient.delete(`/api/workplaces/${id}/`);
      fetchWorkplaces(); // Refresh list
    } catch (err) {
      setError('Failed to delete workplace.');
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('authToken');
    navigate('/login');
  };

  return (
    <div>
      <h2>Workplace Management</h2>
      <button onClick={handleLogout}>Logout</button>
      {error && <p style={{ color: 'red' }}>{error}</p>}

      <hr />
      <h3>{form.id ? 'Edit Workplace' : 'Add New Workplace'}</h3>
      <form onSubmit={handleSubmit}>
        <input name="name" value={form.name} onChange={handleInputChange} placeholder="Name" required />
        <input name="address" value={form.address} onChange={handleInputChange} placeholder="Address" required />
        <input type="number" name="latitude" value={form.latitude} onChange={handleInputChange} placeholder="Latitude" required />
        <input type="number" name="longitude" value={form.longitude} onChange={handleInputChange} placeholder="Longitude" required />
        <button type="submit">{form.id ? 'Update' : 'Create'}</button>
        {form.id && <button onClick={() => setForm({ id: null, name: '', address: '', latitude: 0, longitude: 0 })}>Cancel Edit</button>}
      </form>
      <hr />

      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Address</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {workplaces.map(wp => (
            <tr key={wp.id}>
              <td>{wp.name}</td>
              <td>{wp.address}</td>
              <td>
                <button onClick={() => handleEdit(wp)}>Edit</button>
                <button onClick={() => handleDelete(wp.id)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Dashboard;
