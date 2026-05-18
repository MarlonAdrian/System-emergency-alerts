# 🚨 Sistema de Alerta Temprana de Ingresos a Emergencias

**Reto 4 - hackIAthon 2026 Ecuador**

## ¿Qué hace?

Un webhook que se activa cuando un asegurado ingresa a la emergencia del hospital.

**Flujo:**
1. Hospital envía webhook: "Paciente llegó a emergencia"
2. Sistema valida póliza en Notion en **10 segundos**
3. Agente IA revisa pre-existencias
4. Notifica **simultáneamente** a hospital + aseguradora
5. Gestor de casos puede intervenir **INMEDIATAMENTE**

## Problema que resuelve (Ecuador)

En Quito, cuando paciente llega a emergencia:
- ❌ Hospital NO sabe si tiene seguro
- ❌ Aseguradora NO sabe que llegó
- ❌ Gestor se entera DESPUÉS
- ❌ Resultado: 30+ minutos de caos

Con nuestro sistema:
- ✅ **10 segundos** de validación
- ✅ **Notificación simultánea** a todos
- ✅ **Gestor puede intervenir YA**
- ✅ Paciente atendido sin fricción

## Impacto en números (Quito)

- 200 emergencias/noche en hospitales privados
- 30+ minutos por emergencia = **100+ horas/noche**
- Nuestro sistema: 10 segundos = **Ahorro de 99+ horas/noche**
- En dinero: Aseguradora ahorra ~$200-500/emergencia en gestión

## Quick Start

### Prerequisites
- Python 3.9+
- pip
- Notion account (para base de datos de pólizas)
- (Opcional) Gmail account para notificaciones

### Instalación

```bash
# 1. Clonar repo
git clone https://github.com/[tu-usuario]/reto-4-alerta-emergencias.git
cd reto-4-alerta-emergencias

# 2. Crear virtual env
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar .env
cp .env.example .env
# Editar .env con tus credenciales

# 5. Ejecutar
python main.py
```

El servidor corre en `http://localhost:8000`

## API Endpoints

### POST `/webhook/emergency`
Recibe notificación de paciente en emergencia

**Request:**
```json
{
  "patient_phone": "+593999999999",
  "symptoms": "Dolor en pecho, dificultad respiratoria",
  "hospital": "Hospital Metropolitano",
  "hospital_email": "emergencias@hospitalmetropolitano.ec"
}
```

**Response:**
```json
{
  "success": true,
  "alert_id": "ALERT_1234567890.123",
  "message": "Alerta procesada. Asegurado.",
  "policy_status": "VÁLIDA",
  "insurance_company": "Saludsa",
  "risk_level": "HIGH",
  "notifications_sent": 2,
  "timestamp": "2026-05-20T14:30:45.123Z"
}
```

### GET `/health`
Health check

### GET `/alerts/recent`
Obtiene alertas recientes

### GET `/stats`
Estadísticas del sistema

## Setup Notion

1. Ir a https://www.notion.so/my-integrations
2. Crear "New Integration"
3. Dar permisos de lectura
4. Copiar "Internal Integration Token"
5. Crear tabla en Notion con columnas:
   - `Phone` (text): Número de teléfono
   - `Name` (text): Nombre del paciente
   - `Insurance Company` (select): Aseguradora
   - `Plan Type` (text): Tipo de plan
   - `Policy Number` (text): Número de póliza
   - `Pre-existing Conditions` (multi-select): Pre-existencias
   - `Status` (select): Estado de póliza

6. Compartir tabla con la integración
7. Copiar Database ID desde URL: `https://notion.so/{database-id}?v=...`
8. En `.env`:
   ```
   NOTION_API_KEY=token
   NOTION_DATABASE_ID=database_id
   ```

## Testing

### Test Manual con curl

```bash
curl -X POST http://localhost:8000/webhook/emergency \
  -H "Content-Type: application/json" \
  -d '{
    "patient_phone": "+593999999999",
    "symptoms": "Dolor en pecho severo",
    "hospital": "Hospital Metropolitano",
    "hospital_email": "emergencias@test.ec"
  }'
```

### Test sin Notion (Mock Mode)

Si no tienes Notion configurado, el sistema usa datos de prueba:
- `+593999999999`: Juan Pérez - Saludsa (con pre-existencias)
- `+593988888888`: María López - Humana
- `+593977777777`: Carlos Reyes - Bupa

## Lógica del Agente IA

El agente analiza:

1. **Síntomas críticos:** Pecho, derrame, convulsión, etc. → Risk +0.2
2. **Pre-existencias:** Cardiopatía=0.5, Diabetes=0.3, etc.
3. **Cobertura:** Sin seguro → Risk +0.3
4. **Risk Score Final:**
   - ≥0.75: CRITICAL (intervención inmediata)
   - ≥0.5: HIGH (especialista)
   - ≥0.3: MEDIUM (monitoreo)
   - <0.3: LOW (estándar)

## Notificaciones

**Hospital recibe:** Estado de seguro, póliza, recomendaciones clínicas

**Aseguradora recibe:** Notificación de admisión, análisis de riesgo, necesidad de gestor

## Arquitectura

```
Hospital
    ↓ (webhook)
FastAPI Server
    ├→ Notion (valida póliza)
    ├→ Agent IA (analiza riesgo)
    └→ Email (notifica)
       ├→ Hospital
       └→ Aseguradora
```

## Entregables para hackIAthon

- Enlace Agente funcional (público)
- Repositorio GitHub (público)

## Tech Stack

- **Backend:** FastAPI + Python
- **Database:** Notion API
- **AI Agent:** Lógica local (sin API externa)
- **Notifications:** SMTP (Email)
- **Deployment:** Render/Heroku/Digital Ocean

## Licencia

MIT - Libre para usar en hackathon y después

## Equipo

- Marlon Tuquerres & Noe Gordon

