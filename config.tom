from database import get_db, PriceAlert, AlertCondition, Cryptocurrency
from datetime import datetime
from sqlalchemy.orm import joinedload

def create_price_alert(coin_id: str, target_price: float, condition: str) -> PriceAlert:
    db = get_db()
    try:
        # Get cryptocurrency
        crypto = db.query(Cryptocurrency).filter_by(coin_id=coin_id).first()
        if not crypto:
            raise ValueError(f"Cryptocurrency with ID {coin_id} not found")

        # Create alert
        alert = PriceAlert(
            cryptocurrency=crypto,
            target_price=target_price,
            condition=AlertCondition(condition),
            is_active=True
        )
        db.add(alert)
        db.commit()
        db.refresh(alert)
        return alert
    finally:
        db.close()

def get_active_alerts():
    db = get_db()
    try:
        # Use joinedload to eagerly load the cryptocurrency relationship
        alerts = (db.query(PriceAlert)
                 .options(joinedload(PriceAlert.cryptocurrency))
                 .join(Cryptocurrency)
                 .filter(PriceAlert.is_active == True)
                 .all())

        # Convert to list of dictionaries to avoid detached instance issues
        alert_data = []
        for alert in alerts:
            alert_data.append({
                'id': alert.id,
                'crypto_name': alert.cryptocurrency.name,
                'target_price': alert.target_price,
                'condition': alert.condition.value
            })
        return alert_data
    finally:
        db.close()

def check_alert_conditions(crypto_id: str, current_price: float):
    db = get_db()
    try:
        alerts = (db.query(PriceAlert)
                 .join(Cryptocurrency)
                 .filter(
                     Cryptocurrency.coin_id == crypto_id,
                     PriceAlert.is_active == True
                 ).all())

        triggered_alerts = []
        for alert in alerts:
            is_triggered = False
            if alert.condition == AlertCondition.ABOVE and current_price >= alert.target_price:
                is_triggered = True
            elif alert.condition == AlertCondition.BELOW and current_price <= alert.target_price:
                is_triggered = True

            if is_triggered:
                alert.is_active = False
                alert.triggered_at = datetime.utcnow()
                triggered_alerts.append({
                    'crypto_name': alert.cryptocurrency.name,
                    'target_price': alert.target_price,
                    'condition': alert.condition.value
                })

        if triggered_alerts:
            db.commit()

        return triggered_alerts
    finally:
        db.close()