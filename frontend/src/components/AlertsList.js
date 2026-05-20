import React from 'react';
import './AlertsList.css';

function AlertsList({ alerts }) {
  const recentAlerts = alerts.slice(-10).reverse();

  return (
    <section className="alerts-list-container">
      <h2>⚠️ Alertas Recientes</h2>
      
      {recentAlerts.length > 0 ? (
        <div className="alerts-list">
          {recentAlerts.map((alert, idx) => {
            const alertData = alert._source || alert;
            const severity = alertData.risk_level || 'LOW';

            return (
              <div key={idx} className={`alert-item alert-${severity.toLowerCase()}`}>
                <div className="alert-header">
                  <strong>{alertData.alert_type || 'alert'}</strong>
                  <span className={`badge badge-${severity.toLowerCase()}`}>{severity}</span>
                </div>
                <p className="alert-phone">📱 {alertData.phone}</p>
                <p className="alert-message">{alertData.message}</p>
                <small>{new Date(alertData.timestamp).toLocaleTimeString()}</small>
              </div>
            );
          })}
        </div>
      ) : (
        <p className="empty-state">📭 Sin alertas</p>
      )}
    </section>
  );
}

export default AlertsList;