from pydantic import BaseModel
from typing import Optional

class BotBase(BaseModel):
    name: str
    description: Optional[str] = None

class BotCreate(BotBase):
    pass

class Bot(BotBase):
    id: int

    class Config:
        orm_mode = True
class UserBase(BaseModel):
    username: str
    email: Optional[str] = None

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

class TradeBase(BaseModel):
    user_id: int
    symbol: str
    side: str  # 'buy' or 'sell'
    quantity: float
    price: float
    timestamp: str

class TradeCreate(TradeBase):
    pass

class Trade(TradeBase):
    id: int

    class Config:
        orm_mode = True

class LogBase(BaseModel):
    user_id: Optional[int] = None
    action: str
    timestamp: str
    details: Optional[str] = None

class LogCreate(LogBase):
    pass

class Log(LogBase):
    id: int

    class Config:
        orm_mode = True

class InfluxDBData(BaseModel):
    measurement: str
    time: str
    fields: dict
    tags: Optional[dict] = None