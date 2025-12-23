from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from app.api import routes_auth, routes_predict
from app.middleware.logging_middleware import LoggingMiddleware
from app.core.exceptions import register_exception_handlers
from app.logging import setup_logging
from contextlib import asynccontextmanager
import logging

logger = logging.getLogger(__name__)

# 1️⃣ Setup logging FIRST
setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application started")
    yield
    logger.info("Application stopped")


# 2️⃣ Create app
app = FastAPI(title="Car Price Prediction API" , lifespan=lifespan , version="1.0.0")

# 3️⃣ Register exception handlers
register_exception_handlers(app)

# 4️⃣ Add middleware
app.add_middleware(LoggingMiddleware)

# 5️⃣ Health / root endpoint
@app.get("/")
def root():
    return {"message": "Welcome to Car Price Prediction API"}

@app.get("/health")
def health():
    return {"status": "ok"}

# 6️⃣ Register routers
app.include_router(routes_auth.router, tags=["Auth"])
app.include_router(routes_predict.router, tags=["Prediction"])

# 7️⃣ Monitoring (Prometheus)
Instrumentator().instrument(app).expose(app)