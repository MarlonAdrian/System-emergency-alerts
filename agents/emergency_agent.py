import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

class EmergencyAgent:
    """Agente que analiza emergencias y pre-existencias"""
    
    def __init__(self):
        self.high_risk_keywords = [
            "pecho", "infarto", "derrame", "convulsion", "shock",
            "inconsciencia", "parada cardiaca", "sangrado", "trauma grave",
            "dificultad respiratoria", "asfixia"
        ]
        
        self.pre_existing_risk = {
            "diabetes": 0.3,
            "hipertensión": 0.3,
            "cardiopatía": 0.5,
            "cáncer": 0.4,
            "asma": 0.3,
            "epilepsia": 0.4,
            "insuficiencia renal": 0.5
        }
    
    def analyze(self, patient_phone: str, symptoms: str, 
                pre_existing_conditions: List[str], is_insured: bool) -> Dict:
        """
        Analiza síntomas + pre-existencias
        
        Retorna: {risk_level, recommendation, requires_intervention}
        """
        
        symptoms_lower = symptoms.lower()
        
        # 1. Análisis de síntomas
        symptom_risk = self._analyze_symptoms(symptoms_lower)
        
        # 2. Análisis de pre-existencias
        pre_existing_risk_score = self._analyze_pre_existing(pre_existing_conditions)
        
        # 3. Análisis de cobertura
        insurance_risk = 0.0 if is_insured else 0.3  # Sin seguro = riesgo adicional
        
        # 4. Risk score final
        total_risk = (symptom_risk * 0.5) + (pre_existing_risk_score * 0.3) + (insurance_risk * 0.2)
        
        # 5. Determinar nivel de riesgo
        if total_risk >= 0.75:
            risk_level = "CRITICAL"
            recommendation = "⚠️ ALERTA CRÍTICA - Intervención inmediata del gestor de casos"
        elif total_risk >= 0.5:
            risk_level = "HIGH"
            recommendation = "🚨 RIESGO ALTO - Notificar a médico especialista"
        elif total_risk >= 0.3:
            risk_level = "MEDIUM"
            recommendation = "📌 RIESGO MEDIO - Monitoreo cercano recomendado"
        else:
            risk_level = "LOW"
            recommendation = "✅ RIESGO BAJO - Procesamiento estándar"
        
        logger.info(f"🔍 Análisis: {patient_phone} - Risk: {risk_level}")
        
        return {
            "risk_level": risk_level,
            "recommendation": recommendation,
            "symptom_risk": symptom_risk,
            "pre_existing_risk": pre_existing_risk_score,
            "insurance_risk": insurance_risk,
            "total_risk_score": round(total_risk, 2),
            "requires_intervention": total_risk >= 0.5,
            "pre_existing_alert": len(pre_existing_conditions) > 0
        }
    
    def _analyze_symptoms(self, symptoms: str) -> float:
        """Analiza síntomas y retorna risk score 0-1"""
        risk_score = 0.0
        
        for keyword in self.high_risk_keywords:
            if keyword in symptoms:
                risk_score += 0.2
        
        # Capped at 1.0
        return min(risk_score, 1.0)
    
    def _analyze_pre_existing(self, conditions: List[str]) -> float:
        """Analiza pre-existencias y retorna risk score 0-1"""
        if not conditions:
            return 0.0
        
        max_risk = 0.0
        for condition in conditions:
            condition_lower = condition.lower()
            for disease, risk in self.pre_existing_risk.items():
                if disease in condition_lower:
                    max_risk = max(max_risk, risk)
        
        return max_risk