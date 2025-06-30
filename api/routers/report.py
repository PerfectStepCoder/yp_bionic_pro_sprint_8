from fastapi import APIRouter, Depends, HTTPException, status
from auth import get_current_user, has_role

router = APIRouter()

@router.get("/reports")
def get_report(user=Depends(get_current_user)):
    if not has_role(user, "prothetic_user"):
        raise HTTPException(status_code=403, detail="Access denied")
    return {"report": "Protected report for prothetic_user"}
