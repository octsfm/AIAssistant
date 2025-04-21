// 用户管理模块
// 确保class导出正确
console.log('[DEBUG] user.js模块已加载');  

export class UserManager {
    static init() {
        console.log('[INIT] 用户管理模块初始化');
        const btn = document.querySelector('.btn-primary[data-action="create-user"]');
        
        if (btn) {
            // 修改事件绑定方式
            btn.addEventListener('click', UserManager.showAddUserModal.bind(UserManager));
        } else {
            console.error('[ERROR] 未找到新建用户按钮');
        }
    }

    static async showAddUserModal() {
        console.log('[DEBUG] 尝试打开新增用户模态框...');
        try {
            const container = document.getElementById('modalContainer');
            if (!container) {
                console.error('[ERROR] 未找到模态框容器');
                return;
            }

            // 清空容器并显示加载状态
            container.innerHTML = '<div class="loading">加载中...</div>';
            
            const response = await fetch('/user/create');
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            
            // 插入模态框内容
            container.innerHTML = await response.text();
            
            // 添加显示动画
            const modal = container.querySelector('#addUserModal');
            if (modal) {
                modal.classList.add('modal-show');
                // 绑定关闭事件
                modal.querySelector('.close-btn')?.addEventListener('click', () => {
                    modal.classList.remove('modal-show');
                    setTimeout(() => container.innerHTML = '', 300);
                });
            }
        } catch (error) {
            console.error('[ERROR] 加载失败:', error);
            container.innerHTML = `<div class="error">加载失败: ${error.message}</div>`;
        }
    }
}
