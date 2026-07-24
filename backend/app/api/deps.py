from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.database import get_db
from app.core.security import decode_token
from app.models.domain.models import License, LicenseStatusEnum

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/activate")

async def get_current_license(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> License:
    payload = decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="INVALID_TOKEN_OR_EXPIRED"
        )
    
    license_id = payload.get("sub")
    stmt = select(License).where(License.id == license_id)
    result = await db.execute(stmt)
    license_obj = result.scalar_one_or_none()

    if not license_obj or license_obj.status != LicenseStatusEnum.ACTIVE:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="LICENSE_REVOKED_OR_INACTIVE"
        )

    return license_obj

async def get_admin_license(
    current_license: License = Depends(get_current_license)
) -> License:
    if not current_license.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ADMIN_PERMISSIONS_REQUIRED"
        )
    return current_license
