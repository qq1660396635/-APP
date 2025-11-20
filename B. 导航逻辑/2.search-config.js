window.toolsConfig = {
    tools: [
        { name: '安卓浏览器', file: '2.信息聚合/1_安卓浏览器.html', icon: '🌐', description: '轻量级浏览器工具' },
        { name: '聚合搜索', file: '2.信息聚合/2_聚合搜索.html', icon: '🔍', description: '多功能搜索聚合页面' },
        { name: '提示词工具', file: '2.信息聚合/3_提示词.html', icon: '💭', description: 'AI提示词管理和生成工具' },
        { name: '导航页', file: '2.信息聚合/4_导航页.html', icon: '🧭', description: '快速导航与书签管理' },
        { name: '在线视频', file: '2.信息聚合/5_在线视频.html', icon: '📺', description: '在线视频资源聚合' },
        { name: '用户导航中心', file: '2.信息聚合/6_用户导航中心.html', icon: '🧑‍💻', description: '个性化用户导航中心' },
        { name: '生命倒计时', file: '2.信息聚合/7_生命倒计时.html', icon: '⏳', description: '可视化生命时间流逝' },
        { name: '在阅书籍', file: '2.信息聚合/8_在阅书籍.html', icon: '📚', description: '阅读进度管理和书籍信息记录' }
    ],
    gradients: [
        'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
        'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
        'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
        'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
        'linear-gradient(135deg, #30cfd0 0%, #330867 100%)',
        'linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)',
        'linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%)',
        'linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%)',
        'linear-gradient(135deg, #ff6e7f 0%, #bfe9ff 100%)',
        'linear-gradient(135deg, #e0c3fc 0%, #8ec5fc 100%)',
        'linear-gradient(135deg, #f8b195 0%, #c06c84 100%)',
        'linear-gradient(135deg, #f5af19 0%, #f12711 100%)',
        'linear-gradient(135deg, #9795f0 0%, #fbc8d4 100%)',
        'linear-gradient(135deg, #74ebd5 0%, #ACB6E5 100%)'
    ],
    getAllTools() {
        return this.tools;
    },
    getRandomGradient() {
        return this.gradients[Math.floor(Math.random() * this.gradients.length)];
    }
};
