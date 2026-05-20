import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts';
import './Dashboard.css';

function Dashboard({ alerts }) {
  const riskLevels = { CRITICAL: 0, HIGH: 0, MEDIUM: 0, LOW: 0 };

  alerts.forEach(alert => {
    const alertData = alert._source || alert;
    const riskLevel = alertData.risk_level || 'LOW';
    if (riskLevels.hasOwnProperty(riskLevel)) {
      riskLevels[riskLevel]++;
    }
  });

  const chartData = [
    { name: 'CRITICAL', value: riskLevels.CRITICAL },
    { name: 'HIGH', value: riskLevels.HIGH },
    { name: 'MEDIUM', value: riskLevels.MEDIUM },
    { name: 'LOW', value: riskLevels.LOW }
  ].filter(item => item.value > 0 || alerts.length === 0);

  const COLORS = { CRITICAL: '#ef4444', HIGH: '#f97316', MEDIUM: '#eab308', LOW: '#10b981' };

  return (
    <div className="dashboard-container">
      <h2>📊 Análisis de Riesgos</h2>
      
      {alerts.length > 0 ? (
        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie data={chartData} cx="50%" cy="50%" outerRadius={80} fill="#8884d8" dataKey="value">
              {chartData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[entry.name]} />
              ))}
            </Pie>
            <Tooltip />
            <Legend />
          </PieChart>
        </ResponsiveContainer>
      ) : (
        <p className="empty-state">📈 Sin datos aún</p>
      )}
    </div>
  );
}

export default Dashboard;