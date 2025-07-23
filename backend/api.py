import logging
from fastapi import APIRouter, HTTPException, Depends, Body, status
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import Session
from backend.db import Base, SessionLocal
from backend.schemas import Bot, BotCreate
import pandas as pd
from backend.strategy import Strategy

logger = logging.getLogger("api_audit")
logger.setLevel(logging.INFO)

router = APIRouter(prefix="/bots", tags=["Bots"])

# SQLAlchemy model
class BotORM(Base):
    __tablename__ = "bots"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(20), default="paused")  # "running", "paused"

# Dependency pro získání DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CRUD operace
@router.get("/", response_model=list[Bot])
def list_bots(db: Session = Depends(get_db)):
    try:
        bots = db.query(BotORM).all()
        log_audit(db, user="system", action="list_bots", detail=f"Listed {len(bots)} bots", status="success")
        return [Bot.from_orm(bot) for bot in bots]
    except Exception as e:
        log_audit(db, user="system", action="list_bots", detail="Failed to list bots", status="error", error=str(e))
        raise

@router.post("/", response_model=Bot, status_code=status.HTTP_201_CREATED)
def create_bot(bot: BotCreate, db: Session = Depends(get_db)):
    try:
        db_bot = BotORM(name=bot.name, description=bot.description)
        db.add(db_bot)
        db.commit()
        log_audit(db, user="system", action="create_bot", detail=f"Created bot {bot.name}", status="success")
        return Bot.from_orm(db_bot)
    except Exception as e:
        log_audit(db, user="system", action="create_bot", detail=f"Failed to create bot {bot.name}", status="error", error=str(e))
        raise
# AuditLog ORM model
class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True, index=True)
    user = Column(String(100), nullable=True)
    action = Column(String(100), nullable=False)
    detail = Column(Text, nullable=True)
    status = Column(String(20), nullable=False)
    error = Column(Text, nullable=True)

def log_audit(db: Session, user: str, action: str, detail: str = None, status: str = "success", error: str = None):
    audit = AuditLog(user=user, action=action, detail=detail, status=status, error=error)
    db.add(audit)
    db.commit()
    db.commit()
    db.refresh(db_bot)
    logger.info(f"Vytvořen bot: id={db_bot.id}, name={db_bot.name}")
    return Bot.from_orm(db_bot)

@router.get("/{bot_id}", response_model=Bot)
def get_bot(bot_id: int, db: Session = Depends(get_db)):
    bot = db.query(BotORM).filter(BotORM.id == bot_id).first()
    if not bot:
        raise HTTPException(status_code=404, detail="Bot nenalezen")
    return Bot.from_orm(bot)

@router.put("/{bot_id}", response_model=Bot)
def update_bot(bot_id: int, bot_update: BotCreate, db: Session = Depends(get_db)):
    bot = db.query(BotORM).filter(BotORM.id == bot_id).first()
    if not bot:
        raise HTTPException(status_code=404, detail="Bot nenalezen")
    old_name = bot.name
    bot.name = bot_update.name
    bot.description = bot_update.description
    db.commit()
    db.refresh(bot)
    logger.info(f"Upraven bot: id={bot.id}, old_name={old_name}, new_name={bot.name}")
    return Bot.from_orm(bot)

@router.delete("/{bot_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_bot(bot_id: int, db: Session = Depends(get_db)):
    bot = db.query(BotORM).filter(BotORM.id == bot_id).first()
    if not bot:
        raise HTTPException(status_code=404, detail="Bot nenalezen")
    db.delete(bot)
    db.commit()
    logger.info(f"Smazán bot: id={bot.id}, name={bot.name}")
    return

@router.post("/{bot_id}/start", response_model=Bot)
def start_bot(bot_id: int, db: Session = Depends(get_db)):
    bot = db.query(BotORM).filter(BotORM.id == bot_id).first()
    if not bot:
        raise HTTPException(status_code=404, detail="Bot nenalezen")
    bot.status = "running"
    db.commit()
    db.refresh(bot)
    logger.info(f"Spuštěn bot: id={bot.id}, name={bot.name}")
    return Bot.from_orm(bot)

@router.post("/{bot_id}/pause", response_model=Bot)
def pause_bot(bot_id: int, db: Session = Depends(get_db)):
    bot = db.query(BotORM).filter(BotORM.id == bot_id).first()
    if not bot:
        raise HTTPException(status_code=404, detail="Bot nenalezen")
    bot.status = "paused"
    db.commit()
    db.refresh(bot)
    logger.info(f"Pozastaven bot: id={bot.id}, name={bot.name}")
    return Bot.from_orm(bot)

@router.post("/{bot_id}/manual_trade")

def manual_trade(
    bot_id: int,
    db: Session = Depends(get_db),
    symbol: str = Body(...),
    side: str = Body(...),
    price: float = Body(...),
    quantity: float = Body(...),
    type_: str = Body("LIMIT")
):
    bot = db.query(BotORM).filter(BotORM.id == bot_id).first()
    if not bot:
        raise HTTPException(status_code=404, detail="Bot nenalezen")
    try:
        from backend.pionex import PionexAPI
        pionex = PionexAPI()
        order = pionex.place_order(symbol, side, price, quantity, type_)
        # Optionally update bot status or log trade in DB
        bot.status = "manual_trade"
        db.commit()
        return {"id": bot.id, "order": order}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Trade failed: {str(e)}")

@router.post("/strategy/demo")
async def strategy_demo(
    prices: list[float] = Body(..., example=[100, 102, 101, 105, 107, 110, 108, 112, 115, 117, 120, 119, 121, 123, 125, 124, 126, 128, 130, 129, 127])
):
    """
    Demo výpočtu indikátorů a řízení rizika.
    """
    df = pd.DataFrame({"close": prices})
    strat = Strategy()
    df = strat.compute_indicators(df)
    stop_loss = strat.check_stop_loss(entry_price=prices[0], current_price=prices[-1])
    can_open = strat.can_open_position(open_positions=2)
    panic = strat.check_panic_mode(df)
    return {
        "indicators": df.tail(1).to_dict(),
        "stop_loss_triggered": stop_loss,
        "can_open_position": can_open,
        "panic_mode": panic
    }
# --- Pionex Endpoints ---
from backend.pionex import PionexAPI, PionexAPIError
from fastapi import Query

@router.get("/pionex/orders")
def get_pionex_orders(symbol: str = Query(None)):
    try:
        api = PionexAPI()
        return api.get_orders(symbol)
    except Exception as e:
        logger.error(f"Pionex get_orders error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/pionex/order")
def place_pionex_order(
    symbol: str = Body(...),
    side: str = Body(...),
    price: float = Body(...),
    quantity: float = Body(...),
    type_: str = Body("LIMIT")
):
    try:
        api = PionexAPI()
        return api.place_order(symbol, side, price, quantity, type_)
    except Exception as e:
        logger.error(f"Pionex place_order error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/pionex/orders")
def cancel_pionex_orders(symbol: str = Query(None)):
    try:
        api = PionexAPI()
        return api.cancel_all_orders(symbol)
    except Exception as e:
        logger.error(f"Pionex cancel_orders error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/pionex/market_trades")
def get_pionex_market_trades(symbol: str = Query(...), limit: int = Query(50)):
    try:
        api = PionexAPI()
        return api.get_market_trades(symbol, limit)
    except Exception as e:
        logger.error(f"Pionex get_market_trades error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/pionex/market_depth")
def get_pionex_market_depth(symbol: str = Query(...), limit: int = Query(20)):
    try:
        api = PionexAPI()
        return api.get_market_depth(symbol, limit)
    except Exception as e:
        logger.error(f"Pionex get_market_depth error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# --- Gemini Endpoints ---
from backend.gemini import GeminiClient

@router.post("/gemini/sentiment")
def gemini_sentiment(text: str = Body(...)):
    try:
        client = GeminiClient()
        return client.analyze_sentiment(text)
    except Exception as e:
        logger.error(f"Gemini analyze_sentiment error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/gemini/hypotheses")
def gemini_hypotheses(prompt: str = Body(...)):
    try:
        client = GeminiClient()
        return client.generate_hypotheses(prompt)
    except Exception as e:
        logger.error(f"Gemini generate_hypotheses error: {e}")
        raise HTTPException(status_code=500, detail=str(e))