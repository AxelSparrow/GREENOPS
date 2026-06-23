from sqlalchemy import Column, Integer, String
from database import Base

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    level = Column(String)
    message = Column(String)