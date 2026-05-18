from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
from datetime import datetime
import logging

from services.notion_service import NotionService
from services.notification_service import NotificationService
from agents.emergency_agent import EmergencyAgent
from models.emergency import EmergencyRequest, EmergencyResponse
import os
from dotenv import load_dotenv

# Cargar .env
load_dotenv()
# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Alerta Temprana - Emergencias", version="1.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Services
notion_service = NotionService()
notification_service = NotificationService()
emergency_agent = EmergencyAgent()

@app.on_event("startup")
async def startup():
    logger.info("✅ Sistema de Alerta Temprana iniciado")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "timestamp": datetime.now().isoformat()}

@app.post("/webhook/emergency", response_model=EmergencyResponse)
async def receive_emergency(emergency: EmergencyRequest):
    """
    Webhook que recibe notificación de emergencia del hospital
    
    Flujo:
    1. Recibe paciente que llegó a emergencia
    2. Valida póliza en Notion
    3. Agente revisa pre-existencias
    4. Notifica hospital + aseguradora
    5. Retorna confirmación
    """
    try:
        logger.info(f"🚨 EMERGENCIA RECIBIDA: {emergency.patient_phone}")
        
        # PASO 1: Buscar póliza en Notion
        policy = notion_service.get_policy(emergency.patient_phone)
        
        if policy:
            logger.info(f"✅ Póliza encontrada: {policy['insurance_company']}")
            is_insured = True
            policy_status = "VÁLIDA"
            insurance_company = policy.get('insurance_company', 'N/A')
            plan_type = policy.get('plan_type', 'N/A')
            pre_existing = policy.get('pre_existing_conditions', [])
        else:
            logger.warning(f"❌ Sin póliza: {emergency.patient_phone}")
            is_insured = False
            policy_status = "SIN SEGURO"
            insurance_company = "N/A"
            plan_type = "N/A"
            pre_existing = []
        
        # PASO 2: Agente analiza pre-existencias
        agent_analysis = emergency_agent.analyze(
            patient_phone=emergency.patient_phone,
            symptoms=emergency.symptoms,
            pre_existing_conditions=pre_existing,
            is_insured=is_insured
        )
        
        # PASO 3: Crear alerta
        alert = {
            "alert_id": f"ALERT_{datetime.now().timestamp()}",
            "timestamp": datetime.now().isoformat(),
            "patient_phone": emergency.patient_phone,
            "symptoms": emergency.symptoms,
            "hospital": emergency.hospital,
            "is_insured": is_insured,
            "insurance_company": insurance_company,
            "plan_type": plan_type,
            "policy_status": policy_status,
            "pre_existing_conditions": pre_existing,
            "agent_risk_level": agent_analysis['risk_level'],
            "agent_recommendation": agent_analysis['recommendation']
        }
        
        # PASO 4: Notificar hospital + aseguradora
        notifications_sent = notification_service.send_alerts(
            alert=alert,
            hospital_email=emergency.hospital_email,
            insurance_email=insurance_company if is_insured else None
        )
        
        logger.info(f"📧 Notificaciones enviadas: {notifications_sent}")
        
        return EmergencyResponse(
            success=True,
            alert_id=alert['alert_id'],
            message=f"Alerta procesada. {'Asegurado' if is_insured else 'Sin seguro'}.",
            policy_status=policy_status,
            insurance_company=insurance_company,
            risk_level=agent_analysis['risk_level'],
            notifications_sent=notifications_sent,
            timestamp=datetime.now().isoformat()
        )
    
    except Exception as e:
        logger.error(f"❌ Error procesando emergencia: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/alerts/recent")
async def get_recent_alerts(limit: int = 10):
    """Obtiene alertas recientes"""
    # TODO: Implementar persistencia en Elasticsearch o Notion
    return {"message": "Endpoint para obtener alertas recientes"}

@app.get("/stats")
async def get_stats():
    """Estadísticas del sistema"""
    return {
        "total_emergencies": 0,  # TODO: contar desde persistencia
        "insured_count": 0,
        "uninsured_count": 0,
        "high_risk_count": 0
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)