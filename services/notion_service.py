import os
import logging
from typing import Optional, Dict
import requests

logger = logging.getLogger(__name__)

class NotionService:
    """
    Servicio para consultar pólizas desde Notion
    
    SETUP:
    1. Crear tabla en Notion con columnas:
       - Phone (text)
       - Name (text)
       - Insurance Company (text)
       - Plan Type (text)
       - Policy Number (text)
       - Pre-existing Conditions (multi-select)
       - Status (select: Active/Inactive)
    
    2. Obtener Notion API key: https://www.notion.so/my-integrations
    3. Compartir tabla con la integración
    4. Copiar Database ID desde URL: https://notion.so/{database_id}
    """
    
    def __init__(self):
        self.api_key = os.getenv("NOTION_API_KEY", "")
        self.database_id = os.getenv("NOTION_DATABASE_ID", "")
        self.base_url = "https://api.notion.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Notion-Version": "2022-06-28"
        }
        
        if not self.api_key or not self.database_id:
            logger.warning("⚠️ Notion credentials not configured. Using mock data.")
            self.mock_mode = True
        else:
            self.mock_mode = False
        
        logger.info(f"Notion Service initialized. Mock mode: {self.mock_mode}")
    
    def get_policy(self, phone: str) -> Optional[Dict]:
        """
        Busca una póliza por número de teléfono
        
        Retorna:
        {
            'phone': '+593XXXXXXXXX',
            'patient_name': 'Juan Pérez',
            'insurance_company': 'Saludsa',
            'plan_type': 'Star',
            'policy_number': 'POL-12345',
            'pre_existing_conditions': ['diabetes', 'hipertensión'],
            'status': 'active'
        }
        """
        
        if self.mock_mode:
            return self._get_mock_policy(phone)
        
        try:
            # Query Notion database
            url = f"{self.base_url}/databases/{self.database_id}/query"
            
            payload = {
                "filter": {
                    "property": "Phone",
                    "text": {
                        "equals": phone
                    }
                }
            }
            
            response = requests.post(url, json=payload, headers=self.headers, timeout=5)
            
            if response.status_code != 200:
                logger.error(f"Notion API error: {response.status_code}")
                return None
            
            results = response.json().get("results", [])
            
            if not results:
                logger.info(f"Póliza no encontrada: {phone}")
                return None
            
            # Parsear primer resultado
            page = results[0]
            properties = page["properties"]
            
            policy = {
                "phone": phone,
                "patient_name": self._get_property(properties, "Name"),
                "insurance_company": self._get_property(properties, "Insurance Company"),
                "plan_type": self._get_property(properties, "Plan Type"),
                "policy_number": self._get_property(properties, "Policy Number"),
                "pre_existing_conditions": self._get_multi_select(properties, "Pre-existing Conditions"),
                "status": self._get_property(properties, "Status")
            }
            
            logger.info(f"✅ Póliza encontrada: {policy['patient_name']} - {policy['insurance_company']}")
            return policy
        
        except Exception as e:
            logger.error(f"Error consultando Notion: {str(e)}")
            return None
    
    def _get_mock_policy(self, phone: str) -> Optional[Dict]:
        """Retorna datos de prueba (para desarrollo sin Notion API)"""
        
        mock_policies = {
            "+593999999999": {
                "phone": "+593999999999",
                "patient_name": "Juan Pérez García",
                "insurance_company": "Saludsa",
                "plan_type": "Star Plus",
                "policy_number": "POL-SALUDSA-2024-001",
                "pre_existing_conditions": ["diabetes tipo 2", "hipertensión"],
                "status": "active"
            },
            "+593988888888": {
                "phone": "+593988888888",
                "patient_name": "María López Rodríguez",
                "insurance_company": "Humana",
                "plan_type": "Premium",
                "policy_number": "POL-HUMANA-2024-002",
                "pre_existing_conditions": ["asma", "alergia"],
                "status": "active"
            },
            "+593977777777": {
                "phone": "+593977777777",
                "patient_name": "Carlos Reyes Morales",
                "insurance_company": "Bupa",
                "plan_type": "Global",
                "policy_number": "POL-BUPA-2024-003",
                "pre_existing_conditions": ["cardiopatía", "hipertensión"],
                "status": "active"
            }
        }
        
        if phone in mock_policies:
            logger.info(f"✅ (MOCK) Póliza encontrada: {mock_policies[phone]['patient_name']}")
            return mock_policies[phone]
        
        logger.warning(f"❌ (MOCK) Póliza no encontrada: {phone}")
        return None
    
    def _get_property(self, properties: Dict, prop_name: str) -> str:
        """Extrae valor de propiedad Notion"""
        try:
            prop = properties.get(prop_name, {})
            if prop.get("type") == "title":
                return "".join([t["plain_text"] for t in prop.get("title", [])])
            elif prop.get("type") == "rich_text":
                return "".join([t["plain_text"] for t in prop.get("rich_text", [])])
            elif prop.get("type") == "select":
                return prop.get("select", {}).get("name", "")
            else:
                return ""
        except:
            return ""
    
    def _get_multi_select(self, properties: Dict, prop_name: str) -> list:
        """Extrae multi-select de Notion"""
        try:
            prop = properties.get(prop_name, {})
            if prop.get("type") == "multi_select":
                return [item["name"] for item in prop.get("multi_select", [])]
            return []
        except:
            return []