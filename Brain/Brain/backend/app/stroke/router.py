from typing import Annotated,Literal
from fastapi import APIRouter,Depends,File,Form,HTTPException,UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from .database import get_db
from .schemas import PatientBase,PredictionResponse
from .service import predict_brain_stroke,delete_patient_service,get_patient_image
from . import crud

router=APIRouter(prefix='/stroke',tags=['Brain Stroke'])

@router.post('/predict',response_model=PredictionResponse,summary='Predict Brain Stroke')
async def predict(
    name: Annotated[str, Form(...)],
    age: Annotated[int, Form(...)],
    gender: Annotated[Literal["Male", "Female", "Other"],Form(...)],
    phone: Annotated[str | None, Form()] = None,
    email: Annotated[str | None, Form()] = None,
    symptoms: Annotated[str | None, Form()] = None,
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    allowed_extensions=['.jpg','.jpeg','.png']
    extension=image.filename.lower().split(".")[-1]
    if f".{extension}" not in allowed_extensions:
        raise HTTPException(status_code=400,detail='Only JPG,JPEG,PNG required')
    
    patient=PatientBase(
        name=name,
        age=age,
        gender=gender,
        phone=phone,
        email=email,
        symptoms=symptoms
    )
    return predict_brain_stroke(db=db,patient=patient,image=image)

@router.get('/patient/{patient_id}',response_model=PredictionResponse)
def get_patient(patient_id:str,db:Session=Depends(get_db)):
    patient=crud.get_patient(db,patient_id)
    if patient is None:
        raise HTTPException(status_code=404,detail='Patient not found')
    return patient

@router.get('/patients',response_model=list[PredictionResponse])
def get_all_patients(db:Session=Depends(get_db)):
    return crud.get_all_patients(db)

@router.delete('/patient/{patient_id}',summary='Delete patient')
def delete_patient(patient_id:str,db:Session=Depends(get_db)):
    return delete_patient_service(db=db,patient_id=patient_id)

@router.get('/image/{patient_id}',summary='View stroke MRI')
def view_patient_image(patient_id:str,db:Session=Depends(get_db)):
    return get_patient_image(db=db,patient_id=patient_id)