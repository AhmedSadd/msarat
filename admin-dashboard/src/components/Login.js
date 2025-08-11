import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

// It's a good practice to have a central place for your API configuration
const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:8000', // Assuming the backend runs on port 8000
});

function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');

    try {
      const response = await apiClient.post('/api/auth/login/', {
        username,
        password,
      });

      const token = response.data.token;
      localStorage.setItem('authToken', token);

      // You might want to also store user info
      // localStorage.setItem('userInfo', JSON.stringify(response.data.user));

      // Redirect to the dashboard
      navigate('/');
    } catch (err) {
      setError('Failed to login. Please check your credentials.');
      console.error(err);
    }
  };

  return (
    <div>
      <h2>Login</h2>
      <form onSubmit={handleLogin}>
        <div>
          <label>Username:</label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Password:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit">Login</button>
      </form>
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  );
}

export default Login;
