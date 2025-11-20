// 搜索引擎配置 - 简洁数组格式
const engines = [
    // 第一页: [ID, 名称, 图标, 背景色, 基础URL, 搜索URL]
    ['baidu', '百度搜索', 'B', '#4e6ef2', 'https://www.baidu.com', 'https://www.baidu.com/s?wd='],
    ['bing', '必应搜索', 'B', '#00809d', 'https://www.bing.com', 'https://www.bing.com/search?q='],
    ['360-search', '360搜索', '360', '#19be6b', 'https://www.so.com', 'https://www.so.com/s?q='],
    ['shenma', '神马搜索', '神', '#ff6a00', 'https://www.sm.cn', 'https://www.sm.cn/s?q='],
    ['github', 'GitHub搜索', 'G', '#24292e', 'https://github.com/search?q=&type=repositories', 'https://github.com/search?q='],
    // 第二页
    ['duckduckgo', 'DuckDuckGo搜索', 'D', '#de5833', 'https://duckduckgo.com', 'https://duckduckgo.com/?origin=funnel_home_website&t=h_&we_feature_name=search-from-homepage&we_started_at=05-15-59_137&q='],
    ['yandex', 'Yandex搜索', 'Я', '#ffcc00', 'https://yandex.com', 'https://yandex.com/search/?text='],
    ['yahoo-jp', '雅虎日本', 'Y', '#ff0033', 'https://www.yahoo.co.jp', 'https://search.yahoo.co.jp/search?&ei=UTF-8&p=']
];

// AI搜索引擎配置
const aiEngines = [
    ['baidu-ai', '百度AI搜索', 'AI', '#4e6ef2', 'https://chat.baidu.com', 'https://chat.baidu.com/search?pd=csaitab&setype=csaitab&word='],
    //['meta-ai', '秘塔AI搜索', 'M', '#0066ff', 'https://metaso.cn', 'https://metaso.cn/search-v2/']
];

// 分页配置
const pageConfig = {
    page1: engines.slice(0, 5),
    page2: engines.slice(5)
};

// 生成标准配置格式
function getConfig() {
    const config = {};
    for (let page in pageConfig) {
        config[page] = pageConfig[page].map(([id, name, icon, iconBg, baseUrl, searchUrl]) => {
            return { id, name, icon, iconBg, baseUrl, searchUrl };
        });
    }
    return config;
}

// 获取随机AI引擎
function getRandomAIEngine() {
    const randomIndex = Math.floor(Math.random() * aiEngines.length);
    const [id, name, icon, iconBg, baseUrl, searchUrl] = aiEngines[randomIndex];
    return { id, name, icon, iconBg, baseUrl, searchUrl };
}

// 导出
window.searchEnginesConfig = getConfig();
window.getRandomAIEngine = getRandomAIEngine;
