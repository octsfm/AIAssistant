from fastapi import APIRouter
from .dashboard import router as dashboard_router
from .users import router as users_router
from .knowledge import router as knowledge_router
from .settings import router as settings_router  # 新增settings路由导入

# 当前路由配置问题分析：
# 1. 父路由已设置prefix="/admin"
# 2. 子路由本身已包含prefix声明（如knowledge_router）
# 3. 注册时再次添加prefix会导致路径重复

router = APIRouter(prefix="/admin", tags=["Admin"])

# 正确注册方式（移除所有子路由前缀参数）
router.include_router(dashboard_router)
router.include_router(users_router, prefix="/users")
router.include_router(knowledge_router, prefix="/knowledge")
router.include_router(settings_router, prefix="/settings")  # 添加正确的前缀