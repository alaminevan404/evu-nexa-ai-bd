from fastapi import APIRouter, Depends
from typing import List, Dict, Any
from app.engine.registry import strategy_registry
from app.api.deps import get_current_license
from app.models.domain.models import License

router = APIRouter()

@router.get("/modules")
async def list_strategy_modules(
    current_license: License = Depends(get_current_license)
) -> List[Dict[str, Any]]:
    modules = strategy_registry.get_all_modules()
    return [
        {
            "id": mod.module_id,
            "name": mod.name,
            "category": mod.category,
            "is_enabled": True
        }
        for mod in modules
    ]
