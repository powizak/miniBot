from apscheduler.schedulers.asyncio import AsyncIOScheduler
from backend.model import ts_model
import numpy as np
import pandas as pd
from backend.db import SessionLocal
from backend.api import log_audit

scheduler = AsyncIOScheduler()

def retrain_model():
    db = SessionLocal()
    try:
        # Fetch real market data from Pionex for retraining
        from backend.pionex import PionexAPI
        api = PionexAPI()
        klines = api.get_klines(symbol="BTCUSDT", interval="1m", limit=100)
        df = pd.DataFrame(klines)
        # Example: use close prices as y, time index as X
        X = np.arange(len(df)).reshape(-1, 1)
        y = df["close"].astype(float).values
        ts_model.fit(X, y)
        log_audit(db, user="system", action="ml_retrain", detail="Model retrained successfully", status="success")
        print("ML model retrénován s reálnými daty z Pionex.")
    except Exception as e:
        log_audit(db, user="system", action="ml_retrain", detail="Model retraining failed", status="error", error=str(e))
        print(f"Chyba při retrénování ML modelu: {e}")
    finally:
        db.close()

def start_scheduler():
    if not scheduler.running:
        # Spustí retrénink každých 10 minut
        scheduler.add_job(retrain_model, "interval", minutes=10, id="ml_retrain", replace_existing=True)
        scheduler.start()