import json
import os
import logging
from datetime import datetime
from typing import List, Dict

logger = logging.getLogger(__name__)

class AlertService:
    """Servicio que guarda alertas en JSON para persistencia"""
    
    def __init__(self):
        self.alerts_file = os.path.join(
            os.path.dirname(__file__),
            '..', 'data', 'alerts.json'
        )
        self.alerts = self._load_alerts()
    
    def _load_alerts(self) -> List[Dict]:
        """Carga alertas desde JSON"""
        try:
            if os.path.exists(self.alerts_file):
                with open(self.alerts_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    logger.info(f"✅ {len(data.get('alerts', []))} alertas cargadas")
                    return data.get('alerts', [])
            else:
                logger.info("📝 Archivo de alertas nuevo creado")
                return []
        except Exception as e:
            logger.error(f"❌ Error cargando alertas: {str(e)}")
            return []
    
    def save_alert(self, alert: Dict) -> bool:
        """Guarda una alerta"""
        try:
            self.alerts.append(alert)
            self._save_to_file()
            logger.info(f"✅ Alerta guardada: {alert['alert_id']}")
            return True
        except Exception as e:
            logger.error(f"❌ Error guardando alerta: {str(e)}")
            return False
    
    def get_all_alerts(self) -> List[Dict]:
        """Obtiene todas las alertas"""
        return self.alerts
    
    def get_recent_alerts(self, limit: int = 10) -> List[Dict]:
        """Obtiene últimas alertas"""
        return self.alerts[-limit:]
    
    def get_stats(self) -> Dict:
        """Calcula estadísticas"""
        total = len(self.alerts)
        insured = sum(1 for a in self.alerts if a.get('is_insured', False))
        uninsured = total - insured
        high_risk = sum(1 for a in self.alerts if a.get('risk_level') in ['CRITICAL', 'HIGH'])
        
        return {
            'total_emergencies': total,
            'insured_count': insured,
            'uninsured_count': uninsured,
            'high_risk_count': high_risk
        }
    
    def _save_to_file(self) -> bool:
        """Persiste alertas en archivo"""
        try:
            os.makedirs(os.path.dirname(self.alerts_file), exist_ok=True)
            with open(self.alerts_file, 'w', encoding='utf-8') as f:
                json.dump({'alerts': self.alerts}, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            logger.error(f"❌ Error guardando alertas: {str(e)}")
            return False