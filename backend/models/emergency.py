from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class EmergencyRequest(BaseModel):
    """Solicitud de emergencia del hospital"""
    patient_phone: str
    symptoms: str
    hospital: str
    hospital_email: str
    timestamp: Optional[str] = None

class EmergencyResponse(BaseModel):
    """Respuesta del sistema de alerta"""
    success: bool
    alert_id: str
    message: str
    policy_status: str
    insurance_company: str
    risk_level: str
    notifications_sent: int
    timestamp: str

class PolicyData(BaseModel):
    """Datos de póliza de Notion"""
    patient_phone: str
    patient_name: str
    insurance_company: str
    plan_type: str
    policy_number: str
    pre_existing_conditions: List[str]
    status: str
    
class AgentAnalysis(BaseModel):
    """Análisis del agente IA"""
    risk_level: str  # LOW, MEDIUM, HIGH, CRITICAL
    recommendation: str
    pre_existing_alert: bool
    requires_intervention: bool