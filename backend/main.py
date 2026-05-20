from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="🚨 Alerta Temprana", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from agents.emergency_agent import EmergencyAgent

emergency_agent = EmergencyAgent()
ALERTS = []

# BD de pólizas - SIMPLE
POLICIES = {
    "+593999999999": {"name": "Juan Pérez", "company": "Saludsa", "pre_existing": ["diabetes", "hipertensión"]},
    "+593988888888": {"name": "María López", "company": "Humana", "pre_existing": ["asma"]},
    "+593977777777": {"name": "Carlos Reyes", "company": "Bupa", "pre_existing": ["cardiopatía"]}
}

class EmergencyRequest(BaseModel):
    patient_phone: str
    symptoms: str
    pre_existing: Optional[str] = ""
    hospital: str
    hospital_email: str

class EmergencyResponse(BaseModel):
    success: bool
    alert_id: str
    message: str
    policy_status: str
    insurance_company: str
    risk_level: str
    recommendation: str
    notifications_sent: int
    timestamp: str

@app.on_event("startup")
async def startup():
    logger.info("✅ Sistema iniciado")

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/webhook/emergency", response_model=EmergencyResponse)
async def emergency(data: EmergencyRequest):
    logger.info(f"\n{'='*60}")
    logger.info(f"EMERGENCIA: {data.patient_phone}")
    
    # Verificar si está en BD
    policy = POLICIES.get(data.patient_phone)
    
    if policy:
        insured = True
        company = policy["company"]
        status = "VÁLIDA"
        logger.info(f"✅ ASEGURADO: {policy['name']} ({company})")
    else:
        insured = False
        company = "N/A"
        status = "SIN SEGURO"
        logger.info(f"❌ SIN SEGURO")
    
    # PRE-EXISTENCIAS: SOLO del formulario, NUNCA de la BD
    pre_existing = []
    if data.pre_existing.strip():
        pre_existing = [c.strip() for c in data.pre_existing.split(',') if c.strip()]
    
    logger.info(f"Pre-existencias: {pre_existing}")
    logger.info(f"Síntomas: {data.symptoms}")
    
    # Agente analiza (SOLO con lo que el usuario envía)
    analysis = emergency_agent.analyze(
        patient_phone=data.patient_phone,
        symptoms=data.symptoms,
        pre_existing_conditions=pre_existing,  # SOLO del formulario
        is_insured=insured
    )
    
    logger.info(f"Riesgo: {analysis['risk_level']}")
    logger.info(f"{'='*60}\n")
    
    # Guardar alerta
    alert = {
        "alert_id": f"ALERT_{datetime.now().timestamp()}",
        "timestamp": datetime.now().isoformat(),
        "patient_phone": data.patient_phone,
        "symptoms": data.symptoms,
        "risk_level": analysis['risk_level'],
        "is_insured": insured,
        "insurance_company": company
    }
    ALERTS.append(alert)
    
    return EmergencyResponse(
        success=True,
        alert_id=alert['alert_id'],
        message="Alerta procesada",
        policy_status=status,
        insurance_company=company,
        risk_level=analysis['risk_level'],
        recommendation=analysis['recommendation'],
        notifications_sent=1,
        timestamp=datetime.now().isoformat()
    )

@app.get("/alerts/recent")
async def get_alerts(limit: int = 10):
    return ALERTS[-limit:]

@app.get("/stats")
async def stats():
    total = len(ALERTS)
    insured = sum(1 for a in ALERTS if a['is_insured'])
    uninsured = total - insured
    high_risk = sum(1 for a in ALERTS if a['risk_level'] in ['CRITICAL', 'HIGH'])
    
    return {
        "total_emergencies": total,
        "insured_count": insured,
        "uninsured_count": uninsured,
        "high_risk_count": high_risk
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)