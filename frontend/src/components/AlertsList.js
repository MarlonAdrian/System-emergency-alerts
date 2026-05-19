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
            const alertType = alertData.alert_type || 'unknown';

            return (
              <div key={idx} className={`alert-item alert-${severity.toLowerCase()}`}>
                <div className="alert-header">
                  <div className="alert-title">
                    <strong>{alertType.replace(/_/g, ' ').toUpperCase()}</strong>
                    <span className={`badge badge-${severity.toLowerCase()}`}>
                      {severity}
                    </span>
                  </div>
                  <small className="alert-time">
                    {new Date(alertData.timestamp).toLocaleTimeString()}
                  </small>
                </div>

                <div className="alert-content">
                  <p className="alert-phone">📱 {alertData.phone}</p>
                  <p className="alert-message">{alertData.message}</p>
                  
                  {alertData.pre_existing_conditions && alertData.pre_existing_conditions.length > 0 && (
                    <p className="alert-pre-existing">
                      🏥 Pre-existencias: {alertData.pre_existing_conditions.join(', ')}
                    </p>
                  )}
                </div>

                <div className="alert-footer">
                  <span className="insurance-badge">
                    {alertData.is_insured ? `✅ ${alertData.insurance_company}` : '❌ Sin seguro'}
                  </span>
                </div>
              </div>
            );
          })}
        </div>
      ) : (
        <div className="empty-state">
          <p>📭 Sin alertas aún. Simula una emergencia para ver las alertas aquí.</p>
        </div>
      )}
    </section>
  );
}

export default AlertsList;