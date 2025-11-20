python3 -c "
import requests
import re
import random

try:
    # 尝试多个可能的笑话网站
    urls = [
        'http://xiaohua.zol.com.cn/lengxiaohua/',
        'https://www.xiaohua.com/duanzi',
        'https://www.lengxiaohua.com/'
    ]
    
    # 尝试不同的用户代理
    user_agents = [
        'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X)',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    ]
    
    for url in urls:
        try:
            response = requests.get(
                url, 
                headers={'User-Agent': random.choice(user_agents)}, 
                timeout=10
            )
            html_content = response.text
            
            # 尝试多种提取方法
            patterns = [
                r'<div class=\"article-text\">(.*?)</div>',
                r'<div class=\"content\">(.*?)</div>',
                r'<p>(.*?)</p>',
                r'<div class=\"detail-text\">(.*?)</div>'
            ]
            
            jokes = []
            for pattern in patterns:
                found = re.findall(pattern, html_content, re.S)
                if found:
                    jokes.extend(found)
            
            if jokes:
                # 清理HTML标签
                clean_jokes = []
                for joke in jokes:
                    joke = re.sub(r'<[^>]+>', '', joke)
                    joke = re.sub(r'\s+', ' ', joke)
                    joke = joke.strip()
                    if len(joke) > 20 and '笑话' not in joke and 'http' not in joke:
                        clean_jokes.append(joke)
                
                if clean_jokes:
                    selected_joke = random.choice(clean_jokes)
                    print('='*50)
                    print('随机笑话:')
                    print('='*50)
                    print(selected_joke)
                    print('='*50)
                    exit(0)  # 成功找到笑话，退出程序
            
            print(f'在 {url} 未找到笑话，尝试下一个网站...')
            
        except Exception as e:
            print(f'访问 {url} 失败: {e}')
            continue
    
    # 如果所有网站都失败，使用备用笑话
    backup_jokes = [
        '为什么数学书总是很悲伤？因为它有太多的问题。',
        '程序员去商店买牛奶，店员问：要不要来点面包？程序员回答：不用了，我家还有。',
        '有一天，三角形、圆形和正方形比赛跑步。圆形滚得最快，正方形卡住了，三角形一直转圈。',
        '为什么电脑永远不会感冒？因为它有Windows，但总是会打开。'
    ]
    
    print('='*50)
    print('网络笑话获取失败，使用备用笑话:')
    print('='*50)
    print(random.choice(backup_jokes))
    print('='*50)

except Exception as e:
    print(f'程序执行失败: {e}')
"
