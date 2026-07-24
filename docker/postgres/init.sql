-- EVU NEXA AI - PostgreSQL Production DDL Migration Script
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Enum Types
DO $$ BEGIN
    CREATE TYPE license_tier_enum AS ENUM ('BASIC', 'PRO', 'INSTITUTIONAL', 'ADMIN');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE license_status_enum AS ENUM ('ACTIVE', 'EXPIRED', 'SUSPENDED', 'REVOKED');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE market_category_enum AS ENUM ('FOREX', 'CRYPTO', 'COMMODITIES', 'INDICES', 'OTC');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE signal_direction_enum AS ENUM ('BULLISH_CALL', 'BEARISH_PUT', 'NEUTRAL');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE risk_level_enum AS ENUM ('LOW', 'MEDIUM', 'HIGH', 'EXTREME');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- 1. Licenses Table
CREATE TABLE IF NOT EXISTS licenses (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    license_key VARCHAR(64) UNIQUE NOT NULL,
    owner_name VARCHAR(100),
    owner_contact VARCHAR(100),
    tier license_tier_enum NOT NULL DEFAULT 'PRO',
    status license_status_enum NOT NULL DEFAULT 'ACTIVE',
    max_devices INT NOT NULL DEFAULT 2,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    notes TEXT
);

CREATE INDEX IF NOT EXISTS idx_licenses_key ON licenses(license_key);
CREATE INDEX IF NOT EXISTS idx_licenses_status ON licenses(status);

-- Seed Default Master Admin Key & Pro Key
INSERT INTO licenses (license_key, owner_name, owner_contact, tier, status, max_devices, expires_at, is_admin, notes)
VALUES 
('NEXA-ADMIN-9999-MASTER', 'System Admin', '@et_evu', 'ADMIN', 'ACTIVE', 10, '2099-12-31 23:59:59+00', TRUE, 'Master Admin Access Key'),
('NEXA-PRO-89F2-44A1-9B2C', 'Demo User', '@et_evu', 'PRO', 'ACTIVE', 2, '2028-12-31 23:59:59+00', FALSE, 'Demo License Key')
ON CONFLICT (license_key) DO NOTHING;

-- 2. Bound Devices / Sessions Table
CREATE TABLE IF NOT EXISTS device_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    license_id UUID NOT NULL REFERENCES licenses(id) ON DELETE CASCADE,
    client_fingerprint VARCHAR(64) NOT NULL,
    user_agent TEXT,
    ip_address VARCHAR(45),
    last_active_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_license_fingerprint UNIQUE(license_id, client_fingerprint)
);

CREATE INDEX IF NOT EXISTS idx_device_fingerprint ON device_sessions(client_fingerprint);

-- 3. Market Assets Table
CREATE TABLE IF NOT EXISTS market_assets (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    symbol VARCHAR(30) UNIQUE NOT NULL,
    display_name VARCHAR(50) NOT NULL,
    category market_category_enum NOT NULL,
    is_otc BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    payout_percentage NUMERIC(5, 2) DEFAULT 85.00,
    pip_decimal_places INT DEFAULT 5,
    provider_source VARCHAR(50) DEFAULT 'PRIMARY_FEED'
);

CREATE INDEX IF NOT EXISTS idx_assets_category ON market_assets(category);

-- Seed Default Market Assets
INSERT INTO market_assets (symbol, display_name, category, is_otc, payout_percentage, pip_decimal_places)
VALUES
('EURUSD', 'EUR / USD', 'FOREX', FALSE, 87.00, 5),
('GBPJPY', 'GBP / JPY', 'FOREX', FALSE, 85.00, 3),
('AUDCAD', 'AUD / CAD', 'FOREX', FALSE, 82.00, 5),
('EURUSD_OTC', 'EUR / USD (OTC)', 'OTC', TRUE, 92.00, 5),
('GBPUSD_OTC', 'GBP / USD (OTC)', 'OTC', TRUE, 90.00, 5),
('BTCUSDT', 'BTC / USDT', 'CRYPTO', FALSE, 88.00, 2),
('ETHUSDT', 'ETH / USDT', 'CRYPTO', FALSE, 86.00, 2),
('XAUUSD', 'Gold (XAU/USD)', 'COMMODITIES', FALSE, 84.00, 2)
ON CONFLICT (symbol) DO NOTHING;

-- 4. Analysis Records Table
CREATE TABLE IF NOT EXISTS analysis_records (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    license_id UUID NOT NULL REFERENCES licenses(id) ON DELETE CASCADE,
    asset_symbol VARCHAR(30) NOT NULL,
    timeframe VARCHAR(10) NOT NULL,
    direction signal_direction_enum NOT NULL,
    confidence_score NUMERIC(5, 2) NOT NULL,
    risk_level risk_level_enum NOT NULL,
    ai_reasoning TEXT NOT NULL,
    indicators_used JSONB NOT NULL,
    market_snapshot JSONB NOT NULL,
    recommended_expiry VARCHAR(20) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    user_outcome VARCHAR(10) DEFAULT 'PENDING'
);

CREATE INDEX IF NOT EXISTS idx_analysis_license ON analysis_records(license_id);
CREATE INDEX IF NOT EXISTS idx_analysis_symbol_timeframe ON analysis_records(asset_symbol, timeframe);
CREATE INDEX IF NOT EXISTS idx_analysis_created ON analysis_records(created_at DESC);

-- 5. Strategy Modules Registry Table
CREATE TABLE IF NOT EXISTS strategy_modules (
    id VARCHAR(100) PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    category VARCHAR(50) NOT NULL,
    description TEXT,
    is_enabled BOOLEAN DEFAULT TRUE,
    default_weight NUMERIC(3, 2) DEFAULT 1.00,
    configuration_schema JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 6. Audit Logs Table
CREATE TABLE IF NOT EXISTS audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    license_key VARCHAR(64),
    action VARCHAR(100) NOT NULL,
    endpoint VARCHAR(200),
    ip_address VARCHAR(45),
    payload JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_audit_logs_created ON audit_logs(created_at DESC);
