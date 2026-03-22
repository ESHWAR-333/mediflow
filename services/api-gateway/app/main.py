from fastapi import FastAPI
from app.routes import router
from prometheus_fastapi_instrumentator import Instrumentator


app = FastAPI(title="MediFlow API Gateway")

Instrumentator().instrument(app).expose(app)
app.include_router(router)

@app.get("/health")
def health():
    return {"status": "ok"}