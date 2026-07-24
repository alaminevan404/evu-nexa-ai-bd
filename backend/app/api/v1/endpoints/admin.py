import uuid
from datetime import datetime, timedelta, timezone
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.database import get_db
from app.models.domain.models import License, LicenseTierEnum, LicenseStatusEnum
from app.models.schemas.schemas import AdminCreateLicenseRequest, LicenseResponse
from app.api.deps import get_admin_license

router = APIRouter()

@router.get("/licenses", response_model=List[LicenseResponse])
async def list_all_licenses(
    db: AsyncSession = Depends(get_db),
    admin_license: License = Depends(get_admin_license)
):
    stmt = select(License).order_by(License.created_at.desc())
    result = await db.execute(stmt)
    licenses = result.scalars().all()

    return [
        LicenseResponse(
            id=lic.id,
            license_key=lic.license_key,
            owner_name=lic.owner_name,
            tier=lic.tier.value,
            status=lic.status.value,
            max_devices=lic.max_devices,
            active_devices_count=len(lic.sessions),
            expires_at=lic.expires_at,
            is_admin=lic.is_admin
        )
        for lic in licenses
    ]

@router.post("/licenses/create", response_model=LicenseResponse)
async def create_new_license(
    payload: AdminCreateLicenseRequest,
    db: AsyncSession = Depends(get_db),
    admin_license: License = Depends(get_admin_license)
):
    # Generate Unique License Key Format: NEXA-XXXX-XXXX-XXXX
    unique_suffix = str(uuid.uuid4()).upper()[:12]
    formatted_key = f"NEXA-{unique_suffix[:4]}-{unique_suffix[4:8]}-{unique_suffix[8:12]}"

    expires_at = datetime.now(timezone.utc) + timedelta(days=payload.duration_days)

    new_license = License(
        license_key=formatted_key,
        owner_name=payload.owner_name,
        owner_contact=payload.owner_contact,
        tier=LicenseTierEnum[payload.tier],
        status=LicenseStatusEnum.ACTIVE,
        max_devices=payload.max_devices,
        expires_at=expires_at,
        is_admin=payload.is_admin,
        notes=payload.notes
    )

    db.add(new_license)
    await db.commit()
    await db.refresh(new_license)

    return LicenseResponse(
        id=new_license.id,
        license_key=new_license.license_key,
        owner_name=new_license.owner_name,
        tier=new_license.tier.value,
        status=new_license.status.value,
        max_devices=new_license.max_devices,
        active_devices_count=0,
        expires_at=new_license.expires_at,
        is_admin=new_license.is_admin
    )
