from fastapi import FastAPI
from app.routes.analyze import router as analyze_router

app = FastAPI(title="Code Analysis Service")
app.include_router(analyze_router)


@app.get("/")
def read_root():
    return {"message": "Code Analysis Service is running"}
