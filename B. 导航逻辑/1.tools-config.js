window.toolsConfig = {
  /* --------------------- 工具列表 --------------------- */
  tools: [
    { name: '10月脚本',         file: '1.辅助工具/1_10月脚本.html',         icon: '📜', description: '10月脚本合集，一键即查' },
    { name: 'TXT阅读器',        file: '1.辅助工具/2. TXT阅读器.html',       icon: '📖', description: '本地TXT文件阅读工具' },
    { name: '剪切板管家',       file: '1.辅助工具/3_剪切板管家.html',       icon: '📋', description: '剪切板历史管理工具' },
    { name: '本地答题',         file: '1.辅助工具/4_本地答题.html',         icon: '📚', description: '本地答题和测试工具' },
    { name: '网页源码分析',     file: '1.辅助工具/5_网页源码分析.html',     icon: '🔍', description: '快速查看网页源码' },
    { name: '网页在线渲染',     file: '1.辅助工具/6_网页在线渲染.html',     icon: '🎨', description: '实时预览网页代码' },
    { name: '在线游戏',         file: '1.辅助工具/7_在线游戏.html',         icon: '🎮', description: '休闲小游戏合集' },
    { name: '在线音乐',        file: '1.辅助工具/8_在线音乐.html', icon: '🎵', description: '在线音乐播放工具' },
    { name: '广告位招租',       file: '1.辅助工具/11_广告位招租.html',      icon: '📢', description: '广告合作信息展示' },
    { name: '开发者日志',       file: '1.辅助工具/12_开发者日志.html',      icon: '📝', description: '项目更新历史记录' }
  ],

  /* --------------------- 背景渐变 --------------------- */
  gradients: [
    'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
    'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
    'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
    'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
    'linear-gradient(135deg, #30cfd0 0%, #330867 100%)'
  ],

  /* --------------------- 公共方法 --------------------- */
  getAllTools() {
    return this.tools;
  },
  getRandomGradient() {
    return this.gradients[Math.floor(Math.random() * this.gradients.length)];
  }
};
