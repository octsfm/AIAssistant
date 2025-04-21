from fastapi import APIRouter, Request, Depends  # 添加Request导入
from sqlalchemy.orm import Session
from core.database import get_db
from fastapi.responses import RedirectResponse
from starlette.templating import Jinja2Templates


router = APIRouter(prefix="", tags=["admin_settings"])
templates = Jinja2Templates(directory="templates")

@router.get("/settings")
async def system_settings(request: Request, db: Session = Depends(get_db)):
    # 移除数据库查询，使用硬编码示例数据
    settings = {
        "system_name": "AI管理助手",
        "session_timeout": 60,
        "backup_interval": 24
    }
    return templates.TemplateResponse("system_settings.html", {
        "request": request,
        "settings": settings
    })