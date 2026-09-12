from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .tumor.database import Base as TumorBase, engine as tumor_engine
from .tumor import models as tumor_models
from .tumor.router import router as tumor_router

from .stroke.database import Base as StrokeBase, engine as stroke_engine
from .stroke import models as stroke_models
from .stroke.router import router as stroke_router


# Ensure both DB schemas are created at startup
TumorBase.metadata.create_all(bind=tumor_engine)
StrokeBase.metadata.create_all(bind=stroke_engine)


app = FastAPI(
    title="Brain Disease AI Platform",
    description="""AI Powered Brain Disease Detection System
    Modules
    --------
    • Brain Tumor Detection
    • Stroke Prediction
    """,
    version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tumor_router)
app.include_router(stroke_router)

@app.get('/')
def home():
    return{
        "message": "Brain Disease AI Platform",
        "version": "1.0.0",
        "status": "Running"
    }