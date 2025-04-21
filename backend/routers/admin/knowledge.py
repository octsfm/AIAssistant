from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from fastapi.responses import RedirectResponse
from starlette.templating import Jinja2Templates
from auth.models import Document  # 新增导入Document模型

router = APIRouter(prefix="", tags=["admin_knowledge"])
templates = Jinja2Templates(directory="templates")

@router.get("/knowledge")
async def knowledge_management(request: Request, db: Session = Depends(get_db)):
    if not request.session.get("authenticated") or request.session.get("user_role") != "admin":
        return RedirectResponse(url="/login")
    documents = db.query(Document).all()
    return templates.TemplateResponse("knowledge_upload.html", {
        "request": request,
        "documents": documents
    })