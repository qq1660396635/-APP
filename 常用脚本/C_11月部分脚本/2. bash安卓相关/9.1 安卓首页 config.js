// 游戏配置文件
window.gameConfig = {
    // 常用工具 - 固定在第一位
    tools: [
        { 
            name: '常用工具', 
            file: 'tools/index.html',
            category: 'tools',
            fixed: true
        }
    ],
    
    // 脚本网站B 合集
    siteB: [
        { name: '消消乐', file: '脚本网站B 合集 单页面/01_消消乐.html', category: 'siteB' },
        { name: '推箱子', file: '脚本网站B 合集 单页面/02_推箱子.html', category: 'siteB' },
        { name: '俄罗斯方块', file: '脚本网站B 合集 单页面/03_俄罗斯方块.html', category: 'siteB' },
        { name: '打地鼠', file: '脚本网站B 合集 单页面/04_打地鼠.html', category: 'siteB' },
        { name: '点灯游戏', file: '脚本网站B 合集 单页面/05_点灯游戏.html', category: 'siteB' },
        { name: '飞机大战', file: '脚本网站B 合集 单页面/06.飞机大战.html', category: 'siteB' },
        { name: '跳一跳', file: '脚本网站B 合集 单页面/07_跳一跳.html', category: 'siteB' },
        { name: '星际逃生', file: '脚本网站B 合集 单页面/08_星际逃生.html', category: 'siteB' },
        { name: '切水果', file: '脚本网站B 合集 单页面/09_切水果.html', category: 'siteB' },
        { name: '塔防游戏', file: '脚本网站B 合集 单页面/10_塔防游戏.html', category: 'siteB' },
        { name: '打砖块max', file: '脚本网站B 合集 单页面/11_打砖块max.html', category: 'siteB' },
        { name: '尼姆博弈', file: '脚本网站B 合集 单页面/12_尼姆博弈.html', category: 'siteB' },
        { name: '台球', file: '脚本网站B 合集 单页面/13_台球.html', category: 'siteB' }
    ],
    
    // 脚本网站D 合集
    siteD: [
        { name: '安卓浏览器', file: '脚本网站D 合集 单页面耐玩/1_安卓浏览器.html', category: 'siteD' },
        { name: 'AI数独', file: '脚本网站D 合集 单页面耐玩/2_AI数独.html', category: 'siteD' },
        { name: '扫雷', file: '脚本网站D 合集 单页面耐玩/3_扫雷.html', category: 'siteD' },
        { name: '中国象棋', file: '脚本网站D 合集 单页面耐玩/4_中国象棋.html', category: 'siteD' },
        { name: '科幻国际象棋', file: '脚本网站D 合集 单页面耐玩/5_科幻国际象棋.html', category: 'siteD' },
        { name: '解谜猜数字', file: '脚本网站D 合集 单页面耐玩/6_解谜猜数字.html', category: 'siteD' },
        { name: '生命游戏', file: '脚本网站D 合集 单页面耐玩/7_生命游戏「规则！」.html', category: 'siteD' }
    ],
    
    // 脚本网站C 合集
    siteC: [
        { name: '记忆翻牌大师', file: '脚本网站C 合集 单页面/20_记忆翻牌大师.html', category: 'siteC' },
        { name: '坦克大战', file: '脚本网站C 合集 单页面/21_坦克大战.html', category: 'siteC' },
        { name: '跳棋', file: '脚本网站C 合集 单页面/22_跳棋［后端算法暂未优化］.html', category: 'siteC' },
        { name: '3D迷宫', file: '脚本网站C 合集 单页面/23_3D迷宫「1.2版」.html', category: 'siteC' },
        { name: '32关跑酷', file: '脚本网站C 合集 单页面/24_32关跑酷.html', category: 'siteC' },
        { name: '斗兽棋', file: '脚本网站C 合集 单页面/25_斗兽棋［算法未引入］.html', category: 'siteC' },
        { name: '军棋', file: '脚本网站C 合集 单页面/26_军棋（算法未引入）.html', category: 'siteC' },
        { name: '迷宫逃离', file: '脚本网站C 合集 单页面/27_迷宫逃离.html', category: 'siteC' },
        { name: '青蛙过河', file: '脚本网站C 合集 单页面/28_青蛙过河.html', category: 'siteC' },
        { name: '猜黑红', file: '脚本网站C 合集 单页面/29_猜黑红.html', category: 'siteC' }
    ],
    
    // 获取所有游戏（工具固定在第一位，其他随机）
    getAllGames() {
        // 合并所有游戏
        const allGames = [
            ...this.tools,
            ...this.siteB,
            ...this.siteD,
            ...this.siteC
        ];
        
        // 分离固定项和可随机项
        const fixedGames = allGames.filter(game => game.fixed);
        const randomGames = allGames.filter(game => !game.fixed);
        
        // 随机打乱可随机项
        const shuffled = this.shuffleArray(randomGames);
        
        // 返回固定项在前，随机项在后的数组
        return [...fixedGames, ...shuffled];
    },
    
    // Fisher-Yates 洗牌算法
    shuffleArray(array) {
        const newArray = [...array];
        for (let i = newArray.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [newArray[i], newArray[j]] = [newArray[j], newArray[i]];
        }
        return newArray;
    }
};
