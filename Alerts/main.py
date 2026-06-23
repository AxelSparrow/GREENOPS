from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from sqlalchemy.orm import Session
from fastapi import Depends

from database import engine, get_db
from models import Base, Alert
from schemas import EnergyData

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="GreenOps Alerts Service",
    description="Service de détection et gestion des alertes GreenOps",
    version="1.0.0"
)

Instrumentator().instrument(app).expose(app)

@app.get("/", tags=["Health"])
def root():
    return {
        "message": "Alert Service Running"
        }

@app.post("/alerts/check", tags=["Alerts"])
def check_alert(
    data: EnergyData,
    db: Session = Depends(get_db)
):

    if data.energy > 300:

        new_alert = Alert(
            level="critical",
            message="Energy threshold exceeded"
        )
            

        db.add(new_alert)
        db.commit()
        db.refresh(new_alert)

        return {
            "message": "Alert created",
            "alert": {
                "id": new_alert.id,
                "level": new_alert.level,
                "message": new_alert.message
            }
        }

    return {
        "message": "No alert detected"
    }

@app.get("/alerts", tags=["Alerts"])
def get_alerts(db: Session = Depends(get_db)):

    alerts = db.query(Alert).all()

    return [
        {
            "id": alert.id,
            "level": alert.level,
            "message": alert.message
        }
        for alert in alerts
    ]

@app.delete("/alerts/{alert_id}", tags=["Alerts"])
def delete_alert(
    alert_id: int,
    db: Session = Depends(get_db)
):
    
    alert = db.query(Alert).filter(
        Alert.id == alert_id
    ).first()

    if not alert:
        return {
            "error": "Alert not found"
        }
    db.delete(alert)
    db.commit()

    return {
        "message": f"Alert {alert_id} deleted"
    }