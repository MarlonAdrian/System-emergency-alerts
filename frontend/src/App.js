import React, { useState, useEffect } from 'react';
import './App.css';
import Dashboard from './components/Dashboard';
import TestForm from './components/TestForm';
import AlertsList from './components/AlertsList';
import Stats from './components/Stats';
import { getStats, getAlerts } from './utils/api';

function App() {
  const [stats, setStats] = useState({
    total_emergencies: 0,
    insured_count: 0,
    uninsured_count: 0,
    high_risk_count: 0
  });
  
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchStats();
    fetchAlerts();
    const interval = setInterval(() => {
      fetchStats();
      fetchAlerts();
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  const fetchStats = async () => {
    try {
      const data = await getStats();
      setStats(data);
    } catch (err) {
      console.error('Error fetching stats:', err);
    }
  };

  const fetchAlerts = async () => {
    try {
      const data = await getAlerts();
      setAlerts(data);
    } catch (err) {
      console.error('Error fetching alerts:', err);
    }
  };

  const handleNewAlert = () => {
    setTimeout(() => {
      fetchStats();
      fetchAlerts();
    }, 500);
  };

  return (
    <div className="app">
      <header className="header">
        <h1>🚨 Alerta Temprana</h1>
        <p>Sistema de notificación en emergencias hospitalarias</p>
      </header>

      <main className="main-container">
        <Stats stats={stats} alerts={alerts} />
        <div className="content-grid">
          <TestForm onAlert={handleNewAlert} />
          <Dashboard alerts={alerts} />
        </div>
        <AlertsList alerts={alerts} />
      </main>

      <footer className="footer">
        <p>🏥 Reto 4 hackIAthon 2026 - Sistema de Alerta Temprana de Emergencias</p>
      </footer>
    </div>
  );
}

export default App;