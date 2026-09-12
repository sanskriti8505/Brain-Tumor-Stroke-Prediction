from datetime import datetime
from typing import Optional,Literal
from pydantic import BaseModel,ConfigDict,Field,EmailStr

class PatientBase(BaseModel):
    name:str=Field(...,min_length=2,max_length=100,description='Patient full name')
    age:int=Field(...,ge=1,le=120,description='patient Age')
    gender:Literal['Male','Female','Other']
    phone:Optional[str]=Field(default=None,min_length=10,max_length=12)
    email:Optional[EmailStr]=None
    symptoms:Optional[str]=Field(default=None,max_length=1000)

class PredictionResponse(PatientBase):
    patient_id:str
    image_name:str
    prediction:str
    confidence:float
    status:Literal[
    "Pending",
    "Processing",
    "Completed",
    "Failed"]
    created_at:datetime
    model_config=ConfigDict(from_attributes=True)
    
class ErrorResponse(BaseModel):
    detail:str
    