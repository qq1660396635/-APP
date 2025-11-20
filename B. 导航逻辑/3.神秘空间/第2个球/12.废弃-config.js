window.triangleNavConfig = {
    tools: [
        { name: '废弃导航', file: '废弃导航.html', icon: '🧭', color: '#FFD700' },
        { name: '废弃留言板', file: '废弃留言板.html', icon: '📝', color: '#00CED1' },
        { name: '神秘工具3', file: '#', icon: '🔮', color: '#9370DB' },
        { name: '神秘工具4', file: '#', icon: '⚡', color: '#FF6347' },
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
console.log('可用工具:', window.triangleNavConfig.getAllTools().filter(tool => window.triangleNavConfig.isToolAvailable(tool)).map(t => t.name));
