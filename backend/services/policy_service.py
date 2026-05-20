import json
import os
import logging
from typing import Optional, Dict

logger = logging.getLogger(__name__)

class PolicyService:
    """Servicio que gestiona pólizas desde JSON (simulando Notion)"""
    
    def __init__(self):
        # Ruta al archivo de pólizas
        self.policies_file = os.path.join(
            os.path.dirname(__file__), 
            '..', 'data', 'policies.json'
        )
        self.policies = self._load_policies()
    
    def _load_policies(self) -> Dict:
        """Carga pólizas desde JSON"""
        try:
            if os.path.exists(self.policies_file):
                with open(self.policies_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    logger.info(f"✅ {len(data.get('policies', []))} pólizas cargadas")
                    return data.get('policies', [])
            else:
                logger.warning(f"⚠️ Archivo de pólizas no encontrado: {self.policies_file}")
                return []
        except Exception as e:
            logger.error(f"❌ Error cargando pólizas: {str(e)}")
            return []
    
    def get_policy(self, phone: str) -> Optional[Dict]:
        """
        Busca una póliza por teléfono
        
        Retorna:
        {
            'phone': '+593999999999',
            'name': 'Juan Pérez',
            'insurance_company': 'Saludsa',
            'plan_type': 'Star Plus',
            'policy_number': 'POL-12345',
            'status': 'active',
            'pre_existing_conditions': ['diabetes', 'hipertensión']
        }
        
        O None si no existe
        """
        for policy in self.policies:
            if policy['phone'] == phone:
                logger.info(f"✅ Póliza encontrada: {policy['name']} ({policy['insurance_company']})")
                return policy
        
        logger.warning(f"❌ Póliza NO encontrada: {phone}")
        return None
    
    def is_insured(self, phone: str) -> bool:
        """Verifica si una persona está asegurada"""
        policy = self.get_policy(phone)
        if policy and policy['status'] == 'active':
            return True
        return False
    
    def get_insurance_company(self, phone: str) -> str:
        """Obtiene la aseguradora de una persona"""
        policy = self.get_policy(phone)
        if policy:
            return policy['insurance_company']
        return "N/A"
    
    def get_pre_existing(self, phone: str) -> list:
        """Obtiene pre-existencias de una persona"""
        policy = self.get_policy(phone)
        if policy:
            return policy.get('pre_existing_conditions', [])
        return []
    
    def add_policy(self, phone: str, name: str, insurance: str, 
                   plan: str, policy_num: str, pre_existing: list = None) -> bool:
        """Agrega una nueva póliza"""
        try:
            new_policy = {
                'phone': phone,
                'name': name,
                'insurance_company': insurance,
                'plan_type': plan,
                'policy_number': policy_num,
                'status': 'active',
                'pre_existing_conditions': pre_existing or []
            }
            
            # Verificar que no exista
            if self.get_policy(phone):
                logger.warning(f"⚠️ Póliza ya existe: {phone}")
                return False
            
            self.policies.append(new_policy)
            self._save_policies()
            logger.info(f"✅ Póliza agregada: {name}")
            return True
        
        except Exception as e:
            logger.error(f"❌ Error agregando póliza: {str(e)}")
            return False
    
    def _save_policies(self) -> bool:
        """Guarda pólizas en JSON"""
        try:
            os.makedirs(os.path.dirname(self.policies_file), exist_ok=True)
            with open(self.policies_file, 'w', encoding='utf-8') as f:
                json.dump({'policies': self.policies}, f, indent=2, ensure_ascii=False)
            logger.info("✅ Pólizas guardadas")
            return True
        except Exception as e:
            logger.error(f"❌ Error guardando pólizas: {str(e)}")
            return False