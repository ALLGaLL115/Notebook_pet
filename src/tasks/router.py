from fastapi import APIRouter, Depends

from ..auth.shemas import UserRead
from ..auth.crud_utils import get_current_active_user
from .task import send_email_report_dashboard


router = APIRouter(
    prefix="/report"
)

@router.get("/dashboard")
async def get_dashboard_report(user:UserRead=   Depends(get_current_active_user)):
    send_email_report_dashboard(user.username)
    return{
        "status": 200,
        "data" : "Letter is sended",
        "details" : None
    }