from fastapi import FastAPI
from app.api.v1.health import router as health_router
from app.api.v1.evaluate import router as eval_router

app = FastAPI() 

# routes
app.include_router(health_router, prefix="/api/v1")
app.include_router(eval_router, prefix="/api/v1")