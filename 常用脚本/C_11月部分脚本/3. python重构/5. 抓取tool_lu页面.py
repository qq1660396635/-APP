import requests
from bs4 import BeautifulSoup
import re
import os
import time

def scrape_python_libraries_realtime():
    # 设置请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # 基础路径
    base_dir = "/storage/emulated/0/Download/OnePlus Share/03 - 个人测试/常用工具转安卓"
    os.makedirs(base_dir, exist_ok=True)
    
    # 文件计数和记录计数
    file_num = 1
    record_count = 0
    current_file = None
    
    def open_new_file():
        nonlocal current_file, file_num
        if current_file:
            current_file.close()
        
        file_path = os.path.join(base_dir, f"python_libraries_part{file_num}.txt")
        current_file = open(file_path, 'w', encoding='utf-8')
        current_file.write(f"Python类库排行榜 - 第{file_num}部分 (按Star数排序)\n")
        current_file.write("=" * 80 + "\n\n")
        print(f"创建新文件: {file_path}")
        return current_file
    
    # 打开第一个文件
    current_file = open_new_file()
    
    # 从第1页开始
    page = 1
    
    while True:
        # 构建分页URL
        if page == 1:
            url = "https://tool.lu/library/?language=Python&sort=stars"
        else:
            url = f"https://tool.lu/library/?language=Python&sort=stars&page={page}"
        
        print(f"正在抓取第 {page} 页: {url}")
        
        try:
            # 发送请求
            response = requests.get(url, headers=headers)
            response.encoding = 'utf-8'
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 查找所有library-item
                library_items = soup.find_all('div', class_='library-item')
                
                # 如果没有找到项目，说明已经到最后一页
                if not library_items:
                    print(f"第 {page} 页没有找到数据，停止抓取")
                    break
                
                page_libraries = []
                
                for item in library_items:
                    try:
                        # 提取仓库名
                        title_element = item.find('h3', class_='library-title')
                        if title_element:
                            title_link = title_element.find('a')
                            if title_link:
                                repo_name = title_link.get_text().strip()
                        
                        # 提取描述
                        desc_element = item.find('div', class_='library-description')
                        description = desc_element.get_text().strip() if desc_element else "无描述"
                        
                        # 提取star数
                        meta_items = item.find_all('div', class_='library-meta-item')
                        star_count = 0
                        for meta_item in meta_items:
                            if 'star' in meta_item.get_text().lower():
                                star_text = meta_item.get_text().strip()
                                # 提取数字
                                star_match = re.search(r'(\d+,?\d*)', star_text)
                                if star_match:
                                    star_count = int(star_match.group(1).replace(',', ''))
                                break
                        
                        page_libraries.append({
                            'name': repo_name,
                            'description': description,
                            'stars': star_count
                        })
                        
                    except Exception as e:
                        print(f"解析单个项目时出错: {e}")
                        continue
                
                if page_libraries:
                    # 按star数排序当前页的数据
                    page_libraries.sort(key=lambda x: x['stars'], reverse=True)
                    
                    # 实时写入文件
                    for lib in page_libraries:
                        record_count += 1
                        
                        # 每500条创建新文件
                        if record_count % 500 == 1 and record_count > 1:
                            file_num += 1
                            current_file = open_new_file()
                        
                        # 写入当前记录
                        line = f"{record_count}. {lib['name']} {lib['description']}\n"
                        current_file.write(line)
                        current_file.flush()  # 立即写入磁盘
                        
                        # 每写入100条显示一次进度
                        if record_count % 100 == 0:
                            print(f"已写入 {record_count} 条记录")
                    
                    print(f"第 {page} 页处理完成，本页 {len(page_libraries)} 条，总计: {record_count}")
                else:
                    print(f"第 {page} 页没有有效数据，停止抓取")
                    break
                
                page += 1
                
                # 添加延迟避免被封
                time.sleep(1)
                
                # 检查是否有下一页（查看分页导航）
                pagination = soup.find('div', class_='pagination')
                if pagination:
                    next_link = pagination.find('a', text='»')
                    if not next_link or 'disabled' in next_link.get('class', []):
                        print("已到达最后一页，停止抓取")
                        break
                
            else:
                print(f"请求失败，状态码: {response.status_code}")
                break
                
        except Exception as e:
            print(f"抓取第 {page} 页时出错: {e}")
            break
    
    # 关闭文件
    if current_file:
        current_file.close()
    
    print(f"\n抓取完成！总共写入 {record_count} 条记录，保存到 {file_num} 个文件")
    print(f"保存目录: {base_dir}")
    
    return record_count

# 执行抓取
if __name__ == "__main__":
    print("开始抓取Python类库...")
    total_records = scrape_python_libraries_realtime()
    
    if total_records > 0:
        print(f"成功抓取并保存了 {total_records} 条Python类库记录")
    else:
        print("抓取失败")
