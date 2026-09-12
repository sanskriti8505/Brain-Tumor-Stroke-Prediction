from sqlalchemy import Column,Integer,String,Float,DateTime,Text
from datetime import datetime,timezone
from .database import Base

class Patient(Base):
    __tablename__="patients"
    id=Column(Integer,primary_key=True,index=True)
    patient_id=Column(String,unique=True,nullable=False,index=True)
    name=Column(String,nullable=False)
    age=Column(Integer,nullable=False)
    gender=Column(String,nullable=False)
    phone=Column(String,nullable=True)
    email=Column(String,nullable=True)
    symptoms=Column(Text,nullable=True)
    image_name=Column(String,nullable=False)
    image_path=Column(String,nullable=False)
    prediction=Column(String,nullable=False)
    confidence=Column(Float,nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    status=Column(String,default="Completed",nullable=False)
    
    
    def __repr__(self):
        return(
            f"<Patient("
            f"patient_id='{self.patient_id}', "
            f"name='{self.name}', "
            f"prediction='{self.prediction}')>"
        )