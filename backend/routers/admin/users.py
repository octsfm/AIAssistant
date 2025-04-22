from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from sqlalchemy.sql import func 
from sqlalchemy.sql.functions import now
from starlette.templating import Jinja2Templates  # 确保导入
from core.database import get_db
from auth.models import User
from fastapi import APIRouter, Depends, Request, Form 
from fastapi.responses import RedirectResponse
from bleach import clean  # 新增导入
from slugify import slugify  # 新增导入
import uuid

router = APIRouter()
# 确保模板引擎在路由函数之前初始化
templates = Jinja2Templates(directory="templates")

@router.get("/users", include_in_schema=False)
async def user_list(request: Request, db: Session = Depends(get_db)):
    print(f"[users.py][12]user_list") 
    if not request.session.get("authenticated") or request.session.get("user_role") != "admin":
        return RedirectResponse(url="/login")
        # 新增CSRF令牌生成
    csrf_token = str(uuid.uuid4())
    request.session["csrf_token"] = csrf_token
    # 保持现有数据库查询逻辑
    users = db.query(User).order_by(User.created_at.desc()).all()
    
    return templates.TemplateResponse("user/list.html", {  # 现在可以正确引用模板引擎
        "request": request,
        "users": users,
        "csrf_token": csrf_token  # 确保传递到模板
    })
    
@router.get("/users/create")  # 完整路径：/admin/users/create
async def create_user_page(request: Request):
    # 生成并存储CSRF令牌
    csrf_token = str(uuid.uuid4())
    request.session["csrf_token"] = csrf_token
    
    return templates.TemplateResponse("user/create.html", {
        "request": request,
        "csrf_token": csrf_token  # 传递到模板
    })

@router.post("/users/create")
async def create_user_action(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    role: str = Form(...),
    db: Session = Depends(get_db)
):
    print(f"[users.py][48]create_user_action") 
    
    # 添加CSRF令牌验证
    if request.session.get("csrf_token") != (await request.form()).get("csrf_token"):
        return templates.TemplateResponse("user/create.html", {
            "request": request,
            "error": "CSRF令牌无效"
        })
    # 检查用户名是否存在
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        return templates.TemplateResponse("user/create.html", {
            "request": request,
            "error": "用户名已存在",
            "csrf_token": request.session.get("csrf_token")  # 保持令牌传递
        })
    
    # 创建新用户
    hashed_password = User.get_password_hash(password)  # 修正为使用模型类方法
    new_user = User(
        username=username,
        password=hashed_password,
        role=role,
        created_at=func.now()
    )
    db.add(new_user)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        return templates.TemplateResponse("user/create.html", {
            "request": request,
            "error": f"数据库错误: {str(e)}"
        })
    
    return RedirectResponse(url="/admin/users", status_code=303)

@router.post("/users/delete/{user_id}")
async def delete_user(
    request: Request,
    user_id: int,
    db: Session = Depends(get_db)
):
    print(f"\n[DEBUG] 进入删除流程，用户ID: {user_id}")
    print(f"[DEBUG] 会话信息: {dict(request.session)}")  

    form_data = await request.form()
    print(f"[DEBUG] 接收的表单数据: {dict(form_data)}") 
    # CSRF验证（与创建用户保持一致）
    # if request.session.get("csrf_token") != form_data.get("csrf_token"):
    #     users = db.query(User).order_by(User.created_at.desc()).all()
    #     return templates.TemplateResponse("user/list.html", {
    #         "request": request,
    #         "users": users,
    #         "error": "无效的CSRF令牌"
    #     })
    print(f"[users.py][107]delete_user")     
    # 权限验证
    if not request.session.get("authenticated") or request.session.get("user_role") != "admin":
        return RedirectResponse(url="/login")
    print(f"[users.py][111]delete_user") 
    # 获取要删除的用户
    user = db.query(User).filter(User.id == user_id).first()
    print(f"[DEBUG] 查询到的用户对象: {user}") 
    print(f"[users.py][114]delete_user") 
    # 保护admin用户
    if user and user.username == "admin":
        users = db.query(User).order_by(User.created_at.desc()).all()
        return templates.TemplateResponse("user/list.html", {
            "request": request,
            "users": users,
            "error": "无法删除管理员账户"
        })
    print(f"[users.py][123]delete_user") 
    # 执行删除
    if user:
        print(f"[users.py][125]delete_user") 
        db.delete(user)
        db.commit()
    
    return RedirectResponse(url="/admin/users", status_code=303)
