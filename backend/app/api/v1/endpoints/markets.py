from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.database import get_db
from app.models.domain.models import MarketAsset, License
from app.models.schemas.schemas import MarketAssetResponse, CandleData
from app.api.deps import get_current_license
from app.services.market_data_service import market_data_service

router = APIRouter()

@router.get("/assets", response_model=List[MarketAssetResponse])
async def list_market_assets(
    category: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_license: License = Depends(get_current_license)
):
    stmt = select(MarketAsset).where(MarketAsset.is_active == True)
    if category and category.upper() != "ALL":
        stmt = stmt.where(MarketAsset.category == category.upper())
    result = await db.execute(stmt)
    assets = result.scalars().all()
    
    return [
        MarketAssetResponse(
            id=a.id,
            symbol=a.symbol,
            display_name=a.display_name,
            category=a.category.value,
            is_otc=a.is_otc,
            payout_percentage=float(a.payout_percentage),
            pip_decimal_places=a.pip_decimal_places,
            provider_source=a.provider_source
        )
        for a in assets
    ]

@router.get("/candles", response_model=List[CandleData])
async def get_market_candles(
    symbol: str = Query(..., example="EURUSD_OTC"),
    timeframe: str = Query("1m", example="1m"),
    limit: int = Query(100, ge=10, le=500),
    current_license: License = Depends(get_current_license)
):
    candles_df = market_data_service.generate_synthetic_candles(symbol, timeframe, limit)
    records = candles_df.to_dict(orient="records")
    return [CandleData(**r) for r in records]
