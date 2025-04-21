from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from starlette.templating import Jinja2Templates  # 确保导入
from core.database import get_db
from auth.models import User

router = APIRouter()
# 确保模板引擎在路由函数之前初始化
templates = Jinja2Templates(directory="templates")

@router.get("/", include_in_schema=False)
async def user_list(request: Request, db: Session = Depends(get_db)):
    print(f"[users.py][12]user_list") 
    if not request.session.get("authenticated") or request.session.get("user_role") != "admin":
        return RedirectResponse(url="/login")
    
    # 保持现有数据库查询逻辑
    users = db.query(User).order_by(User.created_at.desc()).all()
    return templates.TemplateResponse("user/list.html", {  # 现在可以正确引用模板引擎
        "request": request,
        "users": users
    })
