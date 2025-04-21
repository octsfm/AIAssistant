from fastapi import APIRouter
from .dashboard import router as dashboard_router
from .users import router as users_router
from .knowledge import router as knowledge_router
from .settings import router as settings_router  # 新增settings路由导入


# 保持现有管理后台路由结构
router = APIRouter(prefix="/admin", tags=["Admin"])

# 统一注册管理后台子路由
router.include_router(dashboard_router)  # 处理 /admin/ 根路径
router.include_router(users_router)
router.include_router(knowledge_router)
router.include_router(settings_router)