import shutil
from pathlib import Path
from fastapi import UploadFile,HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from . import crud
from .predictor import predict_tumor


CURRENT_DIR=Path(__file__).resolve().parent
UPLOAD_FOLDER=CURRENT_DIR/"uploads"
UPLOAD_FOLDER.mkdir(exist_ok=True)

def predict_brain_tumor(db:Session,patient,image:UploadFile):
    patient_id=crud.generate_patient_id(db)
    patient_folder=UPLOAD_FOLDER/patient_id
    patient_folder.mkdir(parents=True,exist_ok=True)
    image_name=image.filename
    image_path=patient_folder/image_name
    with open(image_path,"wb") as buffer:
        shutil.copyfileobj(image.file,buffer)
    result=predict_tumor(str(image_path))
    patient_record={
        "patient_id": patient_id,
        "name": patient.name,
        "age": patient.age,
        "gender": patient.gender,
        "phone": patient.phone,
        "email": patient.email,
        "symptoms": patient.symptoms,
        "image_name": image_name,
        "image_path": str(image_path),
        "prediction": result["prediction"],
        "confidence": result["confidence"],
        "status": "Completed"

    }
    saved_patient=crud.create_patient(db=db,patient_data=patient_record)
    return saved_patient

def delete_patient_service(db:Session,patient_id:str):
    patient=crud.get_patient(db,patient_id)
    if patient is None:
        raise HTTPException(status_code=404,detail='Patient not found.')
    image_path=Path(patient.image_path)
    if image_path.exists():
        image_path.unlink()
    patient_folder=image_path.parent
    if patient_folder.exists():
        shutil.rmtree(patient_folder)
    crud.delete_patient(db,patient)
    return{'message':'Patient deleted successfully'}

def get_patient_image(db:Session,patient_id:str):
    patient=crud.get_patient(db,patient_id)
    if patient is None:
        raise HTTPException(status_code=404,detail='Patient not found.')
    image_path=Path(patient.image_path)
    if not image_path.exists():
        raise HTTPException(status_code=404,detail='MRI image not found.')
    return FileResponse(image_path)
    