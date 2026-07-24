import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, Integer, Numeric, DateTime, ForeignKey, Text, JSON, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum
from app.core.database import Base

class LicenseTierEnum(str, enum.Enum):
    BASIC = "BASIC"
    PRO = "PRO"
    INSTITUTIONAL = "INSTITUTIONAL"
    ADMIN = "ADMIN"

class LicenseStatusEnum(str, enum.Enum):
    ACTIVE = "ACTIVE"
    EXPIRED = "EXPIRED"
    SUSPENDED = "SUSPENDED"
    REVOKED = "REVOKED"

class MarketCategoryEnum(str, enum.Enum):
    FOREX = "FOREX"
    CRYPTO = "CRYPTO"
    COMMODITIES = "COMMODITIES"
    INDICES = "INDICES"
    OTC = "OTC"

class SignalDirectionEnum(str, enum.Enum):
    BULLISH_CALL = "BULLISH_CALL"
    BEARISH_PUT = "BEARISH_PUT"
    NEUTRAL = "NEUTRAL"

class RiskLevelEnum(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    EXTREME = "EXTREME"

class License(Base):
    __tablename__ = "licenses"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    license_key = Column(String(64), unique=True, nullable=False, index=True)
    owner_name = Column(String(100), nullable=True)
    owner_contact = Column(String(100), nullable=True)
    tier = Column(SQLEnum(LicenseTierEnum), default=LicenseTierEnum.PRO, nullable=False)
    status = Column(SQLEnum(LicenseStatusEnum), default=LicenseStatusEnum.ACTIVE, nullable=False, index=True)
    max_devices = Column(Integer, default=2, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    is_admin = Column(Boolean, default=False)
    notes = Column(Text, nullable=True)

    sessions = relationship("DeviceSession", back_populates="license", cascade="all, delete-orphan")
    analyses = relationship("AnalysisRecord", back_populates="license", cascade="all, delete-orphan")

class DeviceSession(Base):
    __tablename__ = "device_sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    license_id = Column(UUID(as_uuid=True), ForeignKey("licenses.id", ondelete="CASCADE"), nullable=False)
    client_fingerprint = Column(String(64), nullable=False, index=True)
    user_agent = Column(Text, nullable=True)
    ip_address = Column(String(45), nullable=True)
    last_active_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    license = relationship("License", back_populates="sessions")

class MarketAsset(Base):
    __tablename__ = "market_assets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    symbol = Column(String(30), unique=True, nullable=False, index=True)
    display_name = Column(String(50), nullable=False)
    category = Column(SQLEnum(MarketCategoryEnum), nullable=False, index=True)
    is_otc = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    payout_percentage = Column(Numeric(5, 2), default=85.00)
    pip_decimal_places = Column(Integer, default=5)
    provider_source = Column(String(50), default="PRIMARY_FEED")

class AnalysisRecord(Base):
    __tablename__ = "analysis_records"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    license_id = Column(UUID(as_uuid=True), ForeignKey("licenses.id", ondelete="CASCADE"), nullable=False)
    asset_symbol = Column(String(30), nullable=False, index=True)
    timeframe = Column(String(10), nullable=False)
    direction = Column(SQLEnum(SignalDirectionEnum), nullable=False)
    confidence_score = Column(Numeric(5, 2), nullable=False)
    risk_level = Column(SQLEnum(RiskLevelEnum), nullable=False)
    ai_reasoning = Column(Text, nullable=False)
    indicators_used = Column(JSON, nullable=False)
    market_snapshot = Column(JSON, nullable=False)
    recommended_expiry = Column(String(20), nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, index=True)
    user_outcome = Column(String(10), default="PENDING")

    license = relationship("License", back_populates="analyses")

class StrategyModule(Base):
    __tablename__ = "strategy_modules"

    id = Column(String(100), primary_key=True)
    name = Column(String(150), nullable=False)
    category = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    is_enabled = Column(Boolean, default=True)
    default_weight = Column(Numeric(3, 2), default=1.00)
    configuration_schema = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    license_key = Column(String(64), nullable=True)
    action = Column(String(100), nullable=False)
    endpoint = Column(String(200), nullable=True)
    ip_address = Column(String(45), nullable=True)
    payload = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, index=True)
