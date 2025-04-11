from fastapi import Depends, HTTPException, Request
from starlette import status

def admin_permission(request: Request):
    """通用管理员权限检查"""
    if not (request.session.get("authenticated") and request.session.get("user_role") == "admin"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="需要管理员权限"
        )
