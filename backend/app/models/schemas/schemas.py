from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID

# License & Authentication Schemas
class LicenseActivateRequest(BaseModel):
    license_key: str = Field(..., example="NEXA-PRO-89F2-44A1-9B2C")
    client_fingerprint: str = Field(..., example="a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e")
    device_info: Optional[Dict[str, Any]] = None

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    license_key: str
    tier: str
    is_admin: bool
    expires_at: datetime

class LicenseResponse(BaseModel):
    id: UUID
    license_key: str
    owner_name: Optional[str]
    tier: str
    status: str
    max_devices: int
    active_devices_count: int
    expires_at: datetime
    is_admin: bool

# Market Asset Schemas
class MarketAssetResponse(BaseModel):
    id: UUID
    symbol: str
    display_name: str
    category: str
    is_otc: bool
    payout_percentage: float
    pip_decimal_places: int
    provider_source: str

class CandleData(BaseModel):
    timestamp: int
    open: float
    high: float
    low: float
    close: float
    volume: float

# Analysis & Strategy Schemas
class RunAnalysisRequest(BaseModel):
    symbol: str = Field(..., example="EURUSD_OTC")
    timeframe: str = Field(..., example="1m")
    custom_module_ids: Optional[List[str]] = None

class IndicatorOutputSchema(BaseModel):
    module_id: str
    name: str
    category: str
    signal: str  # BULLISH, BEARISH, NEUTRAL
    score: float  # 0.0 - 100.0
    weight: float
    metrics: Dict[str, Any]
    reasoning_fragment: str

class AnalysisResultResponse(BaseModel):
    id: UUID
    asset_symbol: str
    timeframe: str
    direction: str  # BULLISH_CALL, BEARISH_PUT, NEUTRAL
    confidence_score: float
    risk_level: str  # LOW, MEDIUM, HIGH, EXTREME
    ai_reasoning: str
    indicators_used: List[IndicatorOutputSchema]
    market_snapshot: Dict[str, Any]
    recommended_expiry: str
    created_at: datetime

# Admin License Creation Schema
class AdminCreateLicenseRequest(BaseModel):
    owner_name: str
    owner_contact: str
    tier: str = "PRO"
    duration_days: int = 30
    max_devices: int = 2
    is_admin: bool = False
    notes: Optional[str] = None
