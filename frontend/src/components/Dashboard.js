import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts';
import './Dashboard.css';

function Dashboard({ alerts }) {
  // Contar alertas por risk_level
  const riskLevels = {
    CRITICAL: 0,
    HIGH: 0,
    MEDIUM: 0,
    LOW: 0
  };

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

  const COLORS = {
    CRITICAL: '#ef4444',
    HIGH: '#f97316',
    MEDIUM: '#eab308',
    LOW: '#10b981'
  };

  return (
    <div className="dashboard-container">
      <h2>📊 Análisis de Riesgos</h2>
      
      {alerts.length > 0 ? (
        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie
              data={chartData}
              cx="50%"
              cy="50%"
              labelLine={false}
              label={({ name, value }) => `${name}: ${value}`}
              outerRadius={80}
              fill="#8884d8"
              dataKey="value"
            >
              {chartData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[entry.name]} />
              ))}
            </Pie>
            <Tooltip />
            <Legend />
          </PieChart>
        </ResponsiveContainer>
      ) : (
        <div className="empty-state">
          <p>📈 Sin datos aún. Envía una emergencia para ver el análisis.</p>
        </div>
      )}

      <div className="risk-legend">
        <div className="legend-item critical">
          <span className="dot"></span>
          <span>CRITICAL - Intervención inmediata</span>
        </div>
        <div className="legend-item high">
          <span className="dot"></span>
          <span>HIGH - Riesgo alto</span>
        </div>
        <div className="legend-item medium">
          <span className="dot"></span>
          <span>MEDIUM - Riesgo medio</span>
        </div>
        <div className="legend-item low">
          <span className="dot"></span>
          <span>LOW - Riesgo bajo</span>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;