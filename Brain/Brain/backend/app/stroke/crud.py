from sqlalchemy.orm import Session
from .models import Patient

def generate_patient_id(db:Session) -> str:
    last_patient=(db.query(Patient).order_by(Patient.id.desc()).first())
    if last_patient is None:
        return "BS00001"
    last_number=int(last_patient.patient_id[2:])
    return f"BS{last_number+1:05d}"

def create_patient(db:Session,patient_data:dict):
    patient=Patient(**patient_data)
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient

def get_patient(db:Session,patient_id:str):
    return db.query(Patient).filter(Patient.patient_id==patient_id).first()

def get_all_patients(db:Session):
    return db.query(Patient).order_by(Patient.created_at.desc()).all()

def delete_patient(db:Session,patient:Patient):
    db.delete(patient)
    db.commit()
    
def get_patient_image_path(db:Session,patient_id:str):
    patient=db.query(Patient).filter(Patient.patient_id==patient_id).first()
    if patient is None:
        return None
    return patient.image_path