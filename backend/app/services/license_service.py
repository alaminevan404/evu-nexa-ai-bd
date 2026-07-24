from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status
from app.models.domain.models import License, DeviceSession, LicenseStatusEnum
from app.core.security import create_access_token

class LicenseService:
    @staticmethod
    async def activate_license(
        db: AsyncSession,
        license_key: str,
        client_fingerprint: str,
        user_agent: str = None,
        ip_address: str = None
    ) -> dict:
        stmt = select(License).where(License.license_key == license_key)
        result = await db.execute(stmt)
        license_obj = result.scalar_one_or_none()

        if not license_obj:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="INVALID_LICENSE_KEY"
            )

        if license_obj.status != LicenseStatusEnum.ACTIVE:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="LICENSE_SUSPENDED_OR_REVOKED"
            )

        now = datetime.now(timezone.utc)
        if license_obj.expires_at < now:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="LICENSE_EXPIRED"
            )

        # Device Binding Check
        session_stmt = select(DeviceSession).where(
            DeviceSession.license_id == license_obj.id,
            DeviceSession.client_fingerprint == client_fingerprint
        )
        session_result = await db.execute(session_stmt)
        existing_session = session_result.scalar_one_or_none()

        if existing_session:
            existing_session.last_active_at = now
            if ip_address:
                existing_session.ip_address = ip_address
            await db.commit()
        else:
            # Count current active sessions for license
            count_stmt = select(DeviceSession).where(DeviceSession.license_id == license_obj.id)
            count_result = await db.execute(count_stmt)
            active_count = len(count_result.scalars().all())

            if active_count >= license_obj.max_devices:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="ERR_DEVICE_LIMIT_EXCEEDED"
                )

            new_session = DeviceSession(
                license_id=license_obj.id,
                client_fingerprint=client_fingerprint,
                user_agent=user_agent,
                ip_address=ip_address,
                last_active_at=now
            )
            db.add(new_session)
            await db.commit()

        # Issue JWT Access Token
        jwt_payload = {
            "sub": str(license_obj.id),
            "license_key": license_obj.license_key,
            "tier": license_obj.tier.value,
            "fingerprint": client_fingerprint,
            "is_admin": license_obj.is_admin
        }
        token = create_access_token(jwt_payload)

        return {
            "access_token": token,
            "token_type": "bearer",
            "expires_in": 12 * 3600,
            "license_key": license_obj.license_key,
            "tier": license_obj.tier.value,
            "is_admin": license_obj.is_admin,
            "expires_at": license_obj.expires_at
        }

license_service = LicenseService()
