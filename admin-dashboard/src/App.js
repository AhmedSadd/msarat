import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Login from './components/Login';
import Dashboard from './components/Dashboard';
import Drivers from './components/Drivers';
import Vehicles from './components/Vehicles';
import './App.css';

function App() {
  // A simple layout component to wrap protected pages
  const AdminLayout = ({ children }) => (
    <div>
      <nav>
        <Link to="/">Dashboard (Workplaces)</Link> |{' '}
        <Link to="/drivers">Drivers</Link> |{' '}
        <Link to="/vehicles">Vehicles</Link>
      </nav>
      <hr />
      {children}
    </div>
  );

  return (
    <Router>
      <div className="App">
        <h1>Waslni Admin</h1>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/" element={<AdminLayout><Dashboard /></AdminLayout>} />
          <Route path="/drivers" element={<AdminLayout><Drivers /></AdminLayout>} />
          <Route path="/vehicles" element={<AdminLayout><Vehicles /></AdminLayout>} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
