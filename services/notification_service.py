import logging
from typing import Optional, Dict
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

logger = logging.getLogger(__name__)

class NotificationService:
    """Envía notificaciones a hospital + aseguradora"""
    
    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", 587))
        self.email = os.getenv("NOTIFICATION_EMAIL", "")
        self.password = os.getenv("NOTIFICATION_PASSWORD", "")
        
        self.mock_mode = not (self.email and self.password)
        
        if self.mock_mode:
            logger.warning("⚠️ Email credentials not configured. Using mock notifications.")
        else:
            logger.info("✅ Email notifications enabled")
    
    def send_alerts(self, alert: Dict, hospital_email: str, 
                   insurance_email: Optional[str] = None) -> int:
        """
        Envía notificaciones de emergencia
        
        Retorna: número de notificaciones enviadas
        """
        notifications_sent = 0
        
        # 1. Notificación a hospital
        if hospital_email:
            success = self._send_hospital_alert(alert, hospital_email)
            if success:
                notifications_sent += 1
                logger.info(f"📧 Notificación enviada a hospital: {hospital_email}")
        
        # 2. Notificación a aseguradora (si existe)
        if insurance_email and alert['is_insured']:
            success = self._send_insurance_alert(alert, insurance_email)
            if success:
                notifications_sent += 1
                logger.info(f"📧 Notificación enviada a aseguradora: {insurance_email}")
        
        # 3. Log de emergencia
        self._log_emergency(alert)
        
        return notifications_sent
    
    def _send_hospital_alert(self, alert: Dict, hospital_email: str) -> bool:
        """Envía alerta al hospital"""
        
        subject = f"🚨 ALERTA EMERGENCIA - {alert['patient_phone']}"
        
        body = f"""
ALERTA TEMPRANA - PACIENTE EN EMERGENCIA
{'='*50}

PACIENTE:
  Teléfono: {alert['patient_phone']}
  Síntomas: {alert['symptoms']}
  
ESTADO DE SEGURO:
  Asegurado: {'SÍ' if alert['is_insured'] else 'NO'}
  Compañía: {alert['insurance_company']}
  Estado: {alert['policy_status']}
  
ANÁLISIS DE RIESGO:
  Nivel de Riesgo: {alert['agent_risk_level']}
  Recomendación: {alert['agent_recommendation']}
  Pre-existencias: {', '.join(alert['pre_existing_conditions']) if alert['pre_existing_conditions'] else 'Ninguna'}
  
ACCIÓN REQUERIDA:
  - Procesar admisión
  - {'Contactar a aseguradora' if alert['is_insured'] else 'Solicitar garantía de pago'}
  - Monitoreo: {alert['agent_recommendation']}

Timestamp: {alert['timestamp']}
Alert ID: {alert['alert_id']}
"""
        
        return self._send_email(hospital_email, subject, body)
    
    def _send_insurance_alert(self, alert: Dict, insurance_email: str) -> bool:
        """Envía notificación a aseguradora"""
        
        subject = f"📬 NOTIFICACIÓN DE ADMISIÓN - {alert['patient_phone']}"
        
        body = f"""
NOTIFICACIÓN DE ADMISIÓN A EMERGENCIA
{'='*50}

INFORMACIÓN DEL ASEGURADO:
  Teléfono: {alert['patient_phone']}
  Compañía: {alert['insurance_company']}
  Plan: {alert['plan_type']}
  Sintomas: {alert['symptoms']}
  
INFORMACIÓN CLÍNICA:
  Nivel de Riesgo: {alert['agent_risk_level']}
  Pre-existencias: {', '.join(alert['pre_existing_conditions']) if alert['pre_existing_conditions'] else 'Ninguna'}
  
ACCIÓN REQUERIDA:
  - Asignar gestor de casos
  - Validar cobertura
  - {'INTERVENCIÓN INMEDIATA' if alert['agent_risk_level'] in ['CRITICAL', 'HIGH'] else 'Monitoreo'}

RECOMENDACIÓN DEL AGENTE:
  {alert['agent_recommendation']}

Timestamp: {alert['timestamp']}
Alert ID: {alert['alert_id']}
"""
        
        return self._send_email(insurance_email, subject, body)
    
    def _send_email(self, to_email: str, subject: str, body: str) -> bool:
        """Envía email (mock o real)"""
        
        if self.mock_mode:
            logger.info(f"📧 (MOCK) Email a {to_email}")
            logger.info(f"   Subject: {subject}")
            return True
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email
            msg['To'] = to_email
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'plain'))
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email, self.password)
                server.send_message(msg)
            
            logger.info(f"✅ Email enviado a {to_email}")
            return True
        
        except Exception as e:
            logger.error(f"❌ Error enviando email: {str(e)}")
            return False
    
    def _log_emergency(self, alert: Dict):
        """Registra emergencia en log"""
        logger.info(f"""
🚨 EMERGENCIA REGISTRADA:
   ID: {alert['alert_id']}
   Paciente: {alert['patient_phone']}
   Hospital: {alert['hospital']}
   Asegurado: {alert['is_insured']}
   Riesgo: {alert['agent_risk_level']}
   Timestamp: {alert['timestamp']}
""")