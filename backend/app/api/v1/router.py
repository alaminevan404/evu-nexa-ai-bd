from fastapi import APIRouter
from app.api.v1.endpoints import auth, markets, analysis, admin, strategies

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(markets.router, prefix="/markets", tags=["Markets"])
api_router.include_router(analysis.router, prefix="/analysis", tags=["AI Analysis"])
api_router.include_router(admin.router, prefix="/admin", tags=["Admin Panel"])
api_router.include_router(strategies.router, prefix="/strategies", tags=["Strategies"])
