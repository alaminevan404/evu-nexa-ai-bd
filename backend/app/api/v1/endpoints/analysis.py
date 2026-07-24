import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.database import get_db
from app.models.domain.models import License, AnalysisRecord, SignalDirectionEnum, RiskLevelEnum
from app.models.schemas.schemas import RunAnalysisRequest, AnalysisResultResponse, IndicatorOutputSchema
from app.api.deps import get_current_license
from app.services.market_data_service import market_data_service
from app.engine.registry import strategy_registry
from app.engine.aggregator import aggregate_signals
from app.engine.reasoning_engine import generate_ai_reasoning
from app.services.telegram_service import telegram_service

router = APIRouter()

@router.post("/run", response_model=AnalysisResultResponse)
async def execute_ai_market_analysis(
    payload: RunAnalysisRequest,
    db: AsyncSession = Depends(get_db),
    current_license: License = Depends(get_current_license)
):
    # Fetch latest OHLCV candle data
    candles_df = market_data_service.generate_synthetic_candles(payload.symbol, payload.timeframe, 100)
    
    # Execute Strategy Modules
    indicator_outputs = strategy_registry.execute_all(candles_df, payload.custom_module_ids)
    
    # Aggregate Signals & Compute Confidence Score
    direction, confidence_score, risk_level = aggregate_signals(indicator_outputs)

    # Latest Candle Snapshot
    last_candle = candles_df.iloc[-1].to_dict()

    # Generate Natural Language AI Reasoning
    reasoning_text = generate_ai_reasoning(
        symbol=payload.symbol,
        timeframe=payload.timeframe,
        direction=direction,
        confidence_score=confidence_score,
        indicators=indicator_outputs,
        snapshot=last_candle
    )

    recommended_expiry = "1 - 3 Minutes" if payload.timeframe in ["1m", "2m"] else "5 - 15 Minutes"

    # Store Record in DB
    analysis_record = AnalysisRecord(
        license_id=current_license.id,
        asset_symbol=payload.symbol,
        timeframe=payload.timeframe,
        direction=SignalDirectionEnum[direction],
        confidence_score=confidence_score,
        risk_level=RiskLevelEnum[risk_level],
        ai_reasoning=reasoning_text,
        indicators_used=[out.model_dump() for out in indicator_outputs],
        market_snapshot=last_candle,
        recommended_expiry=recommended_expiry,
        created_at=datetime.now(timezone.utc)
    )
    db.add(analysis_record)
    await db.commit()
    await db.refresh(analysis_record)

    response_data = AnalysisResultResponse(
        id=analysis_record.id,
        asset_symbol=analysis_record.asset_symbol,
        timeframe=analysis_record.timeframe,
        direction=analysis_record.direction.value,
        confidence_score=float(analysis_record.confidence_score),
        risk_level=analysis_record.risk_level.value,
        ai_reasoning=analysis_record.ai_reasoning,
        indicators_used=[IndicatorOutputSchema(**out.model_dump()) for out in indicator_outputs],
        market_snapshot=analysis_record.market_snapshot,
        recommended_expiry=analysis_record.recommended_expiry,
        created_at=analysis_record.created_at
    )

    # Async Dispatch to Telegram if High Confidence (>= 80%)
    if confidence_score >= 80.0:
        await telegram_service.send_signal_notification(response_data.model_dump())

    return response_data
