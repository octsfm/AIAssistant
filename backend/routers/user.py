from fastapi import APIRouter

user_router = APIRouter(prefix="/api/user", tags=["用户模块"])

@user_router.get("/profile")
async def user_profile():
    return {"profile": {...}}
