from fastapi import FastAPI
from app.api.attorney import router as attorneys_router

app = FastAPI()
app.include_router(attorneys_router)