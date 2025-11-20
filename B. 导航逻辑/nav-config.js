window.navConfig = {
    // 按钮配置 - 只保留第一个按钮
    buttons: {
        left: [
            { name: '余额修改器', path: '3.神秘空间/第1个球/12.破解导航.html', icon: '💰', color: 0x00ff00 },
            { name: '废弃空间站', path: '3.神秘空间/第2个球/12.废弃仓库.html', icon: '🚀', color: 0x888888 },
            { name: '数据修改', path: null, icon: '📊', color: 0x888888 },
            { name: '账号管理', path: null, icon: '👤', color: 0x888888 },
            { name: 'VIP特权', path: null, icon: '👑', color: 0x888888 },
            { name: '破解工具', path: null, icon: '🔓', color: 0x888888 },
            { name: '脚本中心', path: null, icon: '📜', color: 0x888888 },
            { name: '资源下载', path: null, icon: '⬇️', color: 0x888888 }
        ],
        front: [
            { name: '系统优化', path: null, icon: '⚙️', color: 0x888888 },
            { name: '安全防护', path: null, icon: '🛡️', color: 0x888888 },
            { name: '网络工具', path: null, icon: '🌐', color: 0x888888 },
            { name: '文件管理', path: null, icon: '📁', color: 0x888888 },
            { name: '清理工具', path: null, icon: '🧹', color: 0x888888 },
            { name: '备份恢复', path: null, icon: '💾', color: 0x888888 },
            { name: '性能监控', path: null, icon: '📈', color: 0x888888 },
            { name: '设备信息', path: null, icon: '📱', color: 0x888888 }
        ],
        right: [
            { name: '图片处理', path: null, icon: '🖼️', color: 0x888888 },
            { name: '视频编辑', path: null, icon: '🎬', color: 0x888888 },
            { name: '音频工具', path: null, icon: '🎵', color: 0x888888 },
            { name: 'PDF工具', path: null, icon: '📄', color: 0x888888 },
            { name: '二维码', path: null, icon: '📱', color: 0x888888 },
            { name: '翻译工具', path: null, icon: '🌍', color: 0x888888 },
            { name: '计算器', path: null, icon: '🧮', color: 0x888888 },
            { name: '记事本', path: null, icon: '📝', color: 0x888888 }
        ]
    },
    
    // 获取指定墙的按钮
    getButtonsByWall(wall) {
        return this.buttons[wall] || [];
    },
    
    // 获取所有按钮
    getAllButtons() {
        let allButtons = [];
        Object.keys(this.buttons).forEach(wall => {
            allButtons = allButtons.concat(this.buttons[wall]);
        });
        return allButtons;
    }
};
