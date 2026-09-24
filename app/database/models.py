from sqlalchemy import Column, Integer, Float, String, DateTime
from app.database.db import Base
from datetime import datetime

class RiceInfo(Base):
    __tablename__ = "rice_info"

    id = Column(Integer, primary_key=True)
    variety = Column(String, unique=True)
    water = Column(String)
    fertilizer = Column(String)
class PredictionHistory(Base):
    __tablename__ = "prediction_history"

    id = Column(Integer, primary_key=True)
    image_name = Column(String)
    rice_type = Column(String)
    confidence = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)