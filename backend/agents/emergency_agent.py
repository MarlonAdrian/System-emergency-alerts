import logging

logger = logging.getLogger(__name__)

class EmergencyAgent:
    
    def __init__(self):
        self.critical_keywords = [
            "infarto", "paro cardiaco", "parada cardiaca", "derrame", "stroke",
            "inconsciencia", "inconsciente", "shock", "convulsion", "convulsiones",
            "asfixia", "hemorragia", "sangrado masivo", "edema pulmonar", "aneurisma",
            "embolia", "no respira", "sin pulso", "muerte clinica"
        ]
        
        self.high_keywords = [
            # Trauma / accidentes
            "huesos rotos", "fractura", "fracturas", "accidente", "atropellado",
            "choque", "caida grave", "golpe fuerte", "trauma", "aplastamiento",
            "amputacion", "herida profunda", "herida abierta", "laceracion",
            # Cardio / respiratorio
            "dolor pecho", "dolor de pecho", "opresion pecho",
            "dificultad respiratoria", "dificultad para respirar", "falta de aire",
            "sangrado", "presion baja", "bradicardia", "taquicardia",
            "vomito sangre", "hemorragia digestiva", "quemadura",
            # Neurológico
            "perdida de conciencia", "desmayo", "confusion severa", "paralisis",
            # General grave
            "dolor severo", "dolor intenso", "dolor insoportable"
        ]
        
        self.critical_conditions = {
            "cardiopatia": 0.7,
            "cancer": 0.7,
            "infarto previo": 0.8,
            "diabetes": 0.5,
            "hipertension": 0.5,
            "insuficiencia cardiaca": 0.8,
            "insuficiencia renal": 0.7,
            "epilepsia": 0.6,
            "asma": 0.4,
            "copd": 0.6,
            "vih": 0.7,
            "tuberculosis": 0.6
        }
    
    def analyze(self, patient_phone, symptoms, pre_existing_conditions, is_insured):
        
        # Normalizar: quitar tildes y pasar a minúsculas
        symptoms_clean = self._normalize(symptoms)
        
        symptom_risk = self._analyze_symptoms(symptoms_clean)
        pre_risk = self._analyze_pre_existing(pre_existing_conditions)
        coverage_risk = 0.0 if is_insured else 0.1
        
        total_risk = (symptom_risk * 0.6) + (pre_risk * 0.3) + (coverage_risk * 0.1)
        
        logger.info(f"symptom={symptom_risk:.2f}, pre={pre_risk:.2f}, total={total_risk:.2f}")
        
        risk_level, recommendation = self._get_risk_level(total_risk, symptom_risk, pre_risk)
        
        return {
            "risk_level": risk_level,
            "recommendation": recommendation,
            "symptom_risk": symptom_risk,
            "pre_existing_risk": pre_risk,
            "total_risk_score": total_risk,
            "requires_intervention": total_risk >= 0.5
        }
    
    def _normalize(self, text):
        """Elimina tildes para no depender de acentos"""
        replacements = {
            'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
            'Á': 'a', 'É': 'e', 'Í': 'i', 'Ó': 'o', 'Ú': 'u',
            'ü': 'u', 'ñ': 'n'
        }
        result = text.lower()
        for accented, plain in replacements.items():
            result = result.replace(accented, plain)
        return result
    
    def _analyze_symptoms(self, symptoms):
        
        # CRÍTICOS → 1.0
        for kw in self.critical_keywords:
            kw_clean = self._normalize(kw)
            if kw_clean in symptoms:
                logger.warning(f"⚠️ CRÍTICO: {kw}")
                return 1.0
        
        # ALTOS
        high_count = 0
        for kw in self.high_keywords:
            kw_clean = self._normalize(kw)
            if kw_clean in symptoms:
                high_count += 1
        
        if high_count >= 3:
            return 0.80
        elif high_count >= 2:
            return 0.70
        elif high_count >= 1:
            return 0.60
        
        # GENÉRICOS
        generic = ["dolor", "malestar", "fiebre", "nausea", "mareo", "debilidad", "tos", "vomito"]
        generic_count = sum(1 for kw in generic if kw in symptoms)
        
        if generic_count >= 3:
            return 0.35
        elif generic_count >= 1:
            return 0.20
        
        return 0.10
    
    def _analyze_pre_existing(self, conditions):
        if not conditions:
            return 0.0
        
        max_risk = 0.0
        for condition in conditions:
            condition_clean = self._normalize(condition)
            for disease, risk_score in self.critical_conditions.items():
                disease_clean = self._normalize(disease)
                if disease_clean in condition_clean or condition_clean in disease_clean:
                    max_risk = max(max_risk, risk_score)
        
        if len(conditions) >= 3:
            max_risk = min(max_risk + 0.2, 1.0)
        elif len(conditions) >= 2:
            max_risk = min(max_risk + 0.1, 1.0)
        
        return max_risk
    
    def _get_risk_level(self, total_risk, symptom_risk, pre_risk):
        
        if symptom_risk >= 0.95 or total_risk >= 0.80:
            return "CRITICAL", "🚨 ALERTA CRÍTICA - Intervención inmediata. Activar protocolo de emergencia."
        
        if symptom_risk >= 0.60 or total_risk >= 0.60:
            return "HIGH", "⚠️ RIESGO ALTO - Especialista requerido. Monitoreo continuo. Notificar gestor."
        
        if total_risk >= 0.35 or pre_risk >= 0.5:
            return "MEDIUM", "📌 RIESGO MEDIO - Evaluación prioritaria. Revisar historial clínico."
        
        return "LOW", "✅ RIESGO BAJO - Atención estándar. Triaje normal."