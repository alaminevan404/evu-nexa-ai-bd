from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.models.schemas.schemas import LicenseActivateRequest, TokenResponse, LicenseResponse
from app.services.license_service import license_service
from app.api.deps import get_current_license
from app.models.domain.models import License

router = APIRouter()

@router.post("/activate", response_model=TokenResponse)
async def activate_license_key(
    payload: LicenseActivateRequest,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    ip_addr = request.client.host if request.client else "127.0.0.1"
    user_agent = request.headers.get("user-agent", "Unknown")
    
    result = await license_service.activate_license(
        db=db,
        license_key=payload.license_key,
        client_fingerprint=payload.client_fingerprint,
        user_agent=user_agent,
        ip_address=ip_addr
    )
    return result

@router.get("/me", response_model=LicenseResponse)
async def get_license_session_info(
    current_license: License = Depends(get_current_license)
):
    return LicenseResponse(
        id=current_license.id,
        license_key=current_license.license_key,
        owner_name=current_license.owner_name,
        tier=current_license.tier.value,
        status=current_license.status.value,
        max_devices=current_license.max_devices,
        active_devices_count=len(current_license.sessions),
        expires_at=current_license.expires_at,
        is_admin=current_license.is_admin
    )
