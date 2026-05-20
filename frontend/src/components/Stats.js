import React from 'react';
import './Stats.css';

function Stats({ stats, alerts }) {
  const statCards = [
    {
      label: '🚨 Emergencias',
      value: stats.total_emergencies || 0,
      color: '#ef4444'
    },
    {
      label: '⚠️ Alertas Activas',
      value: alerts.length,
      color: '#f97316'
    },
    {
      label: '✅ Asegurados',
      value: stats.insured_count || 0,
      color: '#10b981'
    },
    {
      label: '❌ Sin Seguro',
      value: stats.uninsured_count || 0,
      color: '#8b5cf6'
    }
  ];

  return (
    <section className="stats-section">
      {statCards.map((stat, idx) => (
        <div key={idx} className="stat-card" style={{ borderTopColor: stat.color }}>
          <h3>{stat.label}</h3>
          <p className="stat-value" style={{ color: stat.color }}>
            {stat.value}
          </p>
        </div>
      ))}
    </section>
  );
}

export default Stats;