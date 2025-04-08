// 登录处理
async function handleLogin(e) {
    e.preventDefault();
    const response = await fetch('/auth/token', {
        method: 'POST',
        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        body: `username=${encodeURI(username.value)}&password=${encodeURI(password.value)}`
    });
    
    if (response.ok) window.location.href = '/';
}

// 动态内容加载
async function loadContent(type) {
    try {
        const response = await fetch(`/admin/${type}`);
        const content = await response.text();
        
        document.getElementById('dynamic-content').innerHTML = content;
        
        // 根据类型初始化功能
        if(type === 'users') initUserList();
        if(type === 'knowledge') initUploader();
    } catch (error) {
        console.error('加载失败:', error);
    }
}

// 初始化用户列表
async function initUserList() {
    const response = await fetch('/api/users');
    const users = await response.json();
    
    const tbody = document.querySelector('#user-table tbody');
    tbody.innerHTML = users.map(user => `
        <tr>
            <td>${user.username}</td>
            <td>${user.role}</td>
            <td>
                <button class="btn edit-btn">编辑</button>
                <button class="btn delete-btn">删除</button>
            </td>
        </tr>
    `).join('');
}

// 初始化上传功能
function initUploader() {
    const uploadBox = document.createElement('div');
    uploadBox.className = 'upload-container';
    uploadBox.innerHTML = `
        <input type="file" multiple accept=".pdf,.docx,.mp4" class="file-input">
        <div class="upload-preview"></div>
        <button class="upload-btn">开始上传</button>
    `;
    document.getElementById('dynamic-content').appendChild(uploadBox);
}

// 文件上传处理
async function handleUpload() {
    const files = document.getElementById('fileInput').files;
    const formData = new FormData();
    
    for (let file of files) {
        formData.append('files', file);
    }

    const response = await fetch('/api/upload', {
        method: 'POST',
        body: formData
    });
    
    if (response.ok) {
        alert('文件上传成功！');
    }
}

// 在DOM加载完成后初始化
document.addEventListener('DOMContentLoaded', () => {
    // 确保侧边栏菜单点击事件绑定
    document.querySelectorAll('.sidebar li').forEach(item => {
        item.addEventListener('click', function() {
            const type = this.dataset.type; // 新增data-type属性
            loadContent(type);
        });
    });
    
    // 初始加载用户列表
    loadContent('users');
    
    document.getElementById('logout-btn').addEventListener('click', async () => {
        try {
            const response = await fetch('/auth/logout', {
                method: 'GET',
                credentials: 'include'  // 修改为include确保发送cookie
            });
            
            // 添加状态检查
            if (response.status === 200 || response.redirected) {
                window.location.href = '/login';
            } else {
                console.error('退出失败:', await response.text());
            }
        } catch (error) {
            console.error('网络错误:', error);
        }
    });
});