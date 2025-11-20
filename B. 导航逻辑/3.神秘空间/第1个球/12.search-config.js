window.triangleNavConfig = {
    tools: [
        { name: '余额修改器', file: '1_余额修改器.html', icon: '💰', color: '#FFD700' },
        { name: '聊天修改器', file: '2_聊天修改器.html', icon: '💬', color: '#00CED1' },
        { name: '二维码生成器', file: '3.二维码生成器.html', icon: '🔮', color: '#9370DB' },
        { name: '密码生成器', file: '4.密码生成器.html', icon: '⚡', color: '#FF6347' }, // 修改后的第四个工具
        { name: '神秘工具5', file: '#', icon: '🌟', color: '#32CD32' },
        { name: '神秘工具6', file: '#', icon: '🔥', color: '#FF4500' },
        { name: '神秘工具7', file: '#', icon: '💎', color: '#1E90FF' },
        { name: '神秘工具8', file: '#', icon: '🚀', color: '#FF1493' }
    ],
    
    getAllTools() {
        return this.tools;
    },
    
    getToolByIndex(index) {
        return this.tools[index] || null;
    },
    
    isToolAvailable(tool) {
        return tool && tool.file && tool.file !== '#';
    }
};

// 添加调试信息
console.log('配置文件已加载，工具数量:', window.triangleNavConfig.getAllTools().length);
console.log('第三个工具已更新为二维码生成器');
console.log('第四个工具已更新为密码生成器');
