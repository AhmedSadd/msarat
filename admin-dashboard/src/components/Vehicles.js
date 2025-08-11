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

function Vehicles() {
  const [vehicles, setVehicles] = useState([]);
  const [drivers, setDrivers] = useState([]);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const [form, setForm] = useState({ id: null, vehicle_type: '', capacity: '', license_plate: '', driver: '' });

  const fetchVehiclesAndDrivers = useCallback(async () => {
    try {
      const [vehiclesRes, driversRes] = await Promise.all([
        apiClient.get('/api/vehicles/'),
        apiClient.get('/api/drivers/')
      ]);
      setVehicles(vehiclesRes.data);
      setDrivers(driversRes.data);
    } catch (err) {
      setError('Failed to fetch data.');
      if (err.response && (err.response.status === 401 || err.response.status === 403)) {
          navigate('/login');
      }
    }
  }, [navigate]);

  useEffect(() => {
    fetchVehiclesAndDrivers();
  }, [fetchVehiclesAndDrivers]);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setForm({ ...form, [name]: value });
  };

  const resetForm = () => {
    setForm({ id: null, vehicle_type: '', capacity: '', license_plate: '', driver: '' });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const { id, ...data } = form;
    // Ensure driver is an integer if it's not an empty string
    const payload = { ...data, driver: data.driver ? parseInt(data.driver) : null };

    try {
      if (id) {
        await apiClient.put(`/api/vehicles/${id}/`, payload);
      } else {
        await apiClient.post('/api/vehicles/', payload);
      }
      resetForm();
      fetchVehiclesAndDrivers();
    } catch (err) {
      setError('Failed to save vehicle.');
    }
  };

  const handleEdit = (vehicle) => {
    setForm({
      id: vehicle.id,
      vehicle_type: vehicle.vehicle_type,
      capacity: vehicle.capacity,
      license_plate: vehicle.license_plate,
      driver: vehicle.driver || ''
    });
  };

  const handleDelete = async (id) => {
    try {
      await apiClient.delete(`/api/vehicles/${id}/`);
      fetchVehiclesAndDrivers();
    } catch (err) {
      setError('Failed to delete vehicle.');
    }
  };

  return (
    <div>
      <h2>Vehicle Management</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}

      <hr />
      <h3>{form.id ? 'Edit Vehicle' : 'Add New Vehicle'}</h3>
      <form onSubmit={handleSubmit}>
        <input name="vehicle_type" value={form.vehicle_type} onChange={handleInputChange} placeholder="Vehicle Type (e.g., Van)" required />
        <input type="number" name="capacity" value={form.capacity} onChange={handleInputChange} placeholder="Capacity" required />
        <input name="license_plate" value={form.license_plate} onChange={handleInputChange} placeholder="License Plate" required />
        <select name="driver" value={form.driver} onChange={handleInputChange}>
          <option value="">Assign a Driver (Optional)</option>
          {drivers.map(d => (
            <option key={d.id} value={d.id}>{d.username}</option>
          ))}
        </select>
        <button type="submit">{form.id ? 'Update' : 'Create'}</button>
        {form.id && <button type="button" onClick={resetForm}>Cancel Edit</button>}
      </form>
      <hr />

      <table>
        <thead>
          <tr>
            <th>License Plate</th>
            <th>Type</th>
            <th>Capacity</th>
            <th>Assigned Driver</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {vehicles.map(v => (
            <tr key={v.id}>
              <td>{v.license_plate}</td>
              <td>{v.vehicle_type}</td>
              <td>{v.capacity}</td>
              <td>{v.driver_username || 'N/A'}</td>
              <td>
                <button onClick={() => handleEdit(v)}>Edit</button>
                <button onClick={() => handleDelete(v.id)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Vehicles;
