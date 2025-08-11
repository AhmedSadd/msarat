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

function Drivers() {
  const [drivers, setDrivers] = useState([]);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const [form, setForm] = useState({
    id: null,
    username: '',
    email: '',
    password: '',
    first_name: '',
    last_name: ''
  });

  const fetchDrivers = useCallback(async () => {
    try {
      const response = await apiClient.get('/api/drivers/');
      setDrivers(response.data);
    } catch (err) {
      setError('Failed to fetch drivers.');
      if (err.response && (err.response.status === 401 || err.response.status === 403)) {
          navigate('/login');
      }
    }
  }, [navigate]);

  useEffect(() => {
    fetchDrivers();
  }, [fetchDrivers]);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setForm({ ...form, [name]: value });
  };

  const resetForm = () => {
    setForm({ id: null, username: '', email: '', password: '', first_name: '', last_name: '' });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    // For drivers, we only handle creation for now. Update is more complex.
    const { id, ...data } = form;

    // Password is required for new users
    if (!id && !data.password) {
        setError("Password is required for new drivers.");
        return;
    }

    try {
      if (id) {
        // Update logic would go here, but it's more complex as we might not want to update the password every time.
        // For now, we'll skip implementing update.
        setError("Update functionality is not implemented yet.");
      } else {
        // Create
        await apiClient.post('/api/drivers/', data);
      }
      resetForm();
      fetchDrivers();
    } catch (err) {
      setError('Failed to save driver.');
    }
  };

  const handleEdit = (driver) => {
    setForm({
        id: driver.id,
        username: driver.username,
        email: driver.email,
        first_name: driver.first_name,
        last_name: driver.last_name,
        password: '' // Don't pre-fill password
    });
  };

  return (
    <div>
      <h2>Driver Management</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}

      <hr />
      <h3>{form.id ? 'Edit Driver' : 'Add New Driver'}</h3>
      <form onSubmit={handleSubmit}>
        <input name="username" value={form.username} onChange={handleInputChange} placeholder="Username" required />
        <input name="email" value={form.email} onChange={handleInputChange} placeholder="Email" type="email" required />
        <input name="first_name" value={form.first_name} onChange={handleInputChange} placeholder="First Name" />
        <input name="last_name" value={form.last_name} onChange={handleInputChange} placeholder="Last Name" />
        <input name="password" value={form.password} onChange={handleInputChange} placeholder="Password" type="password" required={!form.id} />
        <button type="submit">{form.id ? 'Update (Not Implemented)' : 'Create'}</button>
        {form.id && <button type="button" onClick={resetForm}>Cancel Edit</button>}
      </form>
      <hr />

      <table>
        <thead>
          <tr>
            <th>Username</th>
            <th>Email</th>
            <th>Name</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {drivers.map(d => (
            <tr key={d.id}>
              <td>{d.username}</td>
              <td>{d.email}</td>
              <td>{d.first_name} {d.last_name}</td>
              <td>
                <button onClick={() => handleEdit(d)}>Edit</button>
                {/* Delete would be here */}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Drivers;
