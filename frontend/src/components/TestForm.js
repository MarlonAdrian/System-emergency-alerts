import React, { useState } from 'react';
import { sendEmergency } from '../utils/api';
import './TestForm.css';

function TestForm({ onAlert }) {
  const [phone, setPhone] = useState('+593999999999');
  const [symptoms, setSymptoms] = useState('');
  const [preExisting, setPreExisting] = useState('');
  const [hospital, setHospital] = useState('Hospital Metropolitano');
  const [email, setEmail] = useState('emergencias@test.ec');
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState(null);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!symptoms.trim()) {
      setError('Por favor describe los síntomas');
      return;
    }

    setLoading(true);
    setError(null);
    setResponse(null);

    try {
      const result = await sendEmergency({
        patient_phone: phone,
        symptoms: symptoms,
        pre_existing: preExisting,
        hospital: hospital,
        hospital_email: email
      });

      setResponse(result);
      setSymptoms('');
      setPreExisting('');
      onAlert();
    } catch (err) {
      setError(err.message || 'Error enviando emergencia');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="test-form-container">
      <h2>📋 Simular Emergencia</h2>
      
      <form onSubmit={handleSubmit} className="test-form">
        <div className="form-group">
          <label>📱 Teléfono del Paciente</label>
          <input
            type="text"
            value={phone}
            onChange={(e) => setPhone(e.target.value)}
            placeholder="+593999999999"
            className="form-input"
          />
        </div>

        <div className="form-group">
          <label>🏥 Hospital</label>
          <input
            type="text"
            value={hospital}
            onChange={(e) => setHospital(e.target.value)}
            placeholder="Hospital Metropolitano"
            className="form-input"
          />
        </div>

        <div className="form-group">
          <label>📧 Email Hospital</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="emergencias@hospital.ec"
            className="form-input"
          />
        </div>

        <div className="form-group">
          <label>🩺 Síntomas</label>
          <textarea
            value={symptoms}
            onChange={(e) => setSymptoms(e.target.value)}
            placeholder="Describe los síntomas del paciente... (ej: infarto, dolor pecho, dificultad respiratoria)"
            className="form-textarea"
            rows="3"
          />
        </div>

        <div className="form-group">
          <label>💊 Pre-existencias (opcional)</label>
          <textarea
            value={preExisting}
            onChange={(e) => setPreExisting(e.target.value)}
            placeholder="Ej: cardiopatía, diabetes, cáncer, asma... (separadas por comas)"
            className="form-textarea"
            rows="2"
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          className="btn-submit"
        >
          {loading ? '⏳ Enviando...' : '🚨 Enviar Alerta'}
        </button>
      </form>

      {response && (
        <div className={`response response-${response.risk_level.toLowerCase()}`}>
          <h3>✅ Alerta Procesada</h3>
          <p><strong>Estado:</strong> {response.policy_status}</p>
          <p><strong>Aseguradora:</strong> {response.insurance_company}</p>
          <p><strong>Nivel de Riesgo:</strong> <span className={`risk-badge ${response.risk_level.toLowerCase()}`}>{response.risk_level}</span></p>
          <p><strong>Recomendación:</strong> {response.recommendation}</p>
          <p><strong>Notificaciones:</strong> {response.notifications_sent} enviadas</p>
          <small>ID: {response.alert_id}</small>
        </div>
      )}

      {error && (
        <div className="response response-error">
          <h3>❌ Error</h3>
          <p>{error}</p>
        </div>
      )}
    </div>
  );
}

export default TestForm;