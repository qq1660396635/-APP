#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import re
import difflib
import glob
from datetime import datetime
from pathlib import Path

# 基础目录配置
BASE_DIR = "/storage/emulated/0/Download/OnePlus Share/GITHUB 开源项目/项目01/野火小智文档"
REPORT_DIR = os.path.join(BASE_DIR, "项目分析报告", "main差异分析")
HTML_REPORT_DIR = os.path.join(BASE_DIR, "项目分析报告", "main差异分析HTML")  # HTML报告目录
BASE_PROJECT = "[8] STM32CubeMX新建MDK工程"  # 基准项目名称

def safe_read_file(filepath):
    """安全读取文件，处理编码问题"""
    encodings = ['utf-8', 'gbk', 'gb2312', 'latin-1']
    for encoding in encodings:
        try:
            with open(filepath, 'r', encoding=encoding) as f:
                return f.readlines(), encoding
        except UnicodeDecodeError:
            continue
    # 如果所有编码都失败，使用忽略错误的方式读取
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        return f.readlines(), 'utf-8'

def get_file_info(filepath):
    """获取文件基本信息 - 大小、行数等"""
    if not os.path.isfile(filepath):
        return None
    
    file_stat = os.stat(filepath)
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        line_count = sum(1 for _ in f)
    
    return {
        'name': os.path.basename(filepath),
        'path': os.path.dirname(filepath),
        'size': file_stat.st_size,
        'lines': line_count
    }

def generate_html_diff_report(file1, file2, html_report_path):
    """生成HTML格式的差异报告"""
    file1_lines, enc1 = safe_read_file(file1)
    file2_lines, enc2 = safe_read_file(file2)
    
    # 生成HTML格式的diff报告
    html_diff = difflib.HtmlDiff(
        tabsize=4,
        wrapcolumn=80,
        linejunk=None,
        charjunk=difflib.IS_CHARACTER_JUNK
    ).make_file(
        file1_lines, file2_lines, 
        fromdesc=os.path.basename(file1), 
        todesc=os.path.basename(file2),
        context=True, numlines=5
    )
    
    # 添加自定义CSS样式
    html_diff = html_diff.replace(
        '</head>',
        '<style>\n'
        '  body { font-family: Arial, sans-serif; }\n'
        '  table.diff { width: 100%; border-collapse: collapse; }\n'
        '  .diff_header { background-color: #f0f0f0; font-weight: bold; }\n'
        '  td.diff_header { text-align: right; padding: 4px 8px; }\n'
        '  .diff_next { background-color: #c0c0c0; }\n'
        '  .diff_add { background-color: #aaffaa; }\n'
        '  .diff_chg { background-color: #ffff77; }\n'
        '  .diff_sub { background-color: #ffaaaa; }\n'
        '  .diff_pagenav { text-align: center; padding: 10px; }\n'
        '  .diff_add:hover, .diff_chg:hover, .diff_sub:hover { background-color: #ffd700; }\n'
        '  .diff_line { font-family: "Courier New", monospace; font-size: 14px; }\n'
        '</style>\n'
        '</head>'
    )
    
    with open(html_report_path, 'w', encoding='utf-8') as html_file:
        html_file.write(html_diff)
    
    return html_diff

def generate_diff_content(file1, file2):
    """生成内存中的diff内容用于分析"""
    file1_lines, enc1 = safe_read_file(file1)
    file2_lines, enc2 = safe_read_file(file2)
    
    # 生成unified diff格式
    diff = difflib.unified_diff(file1_lines, file2_lines, 
                               fromfile=file1, tofile=file2, n=3)
    
    return list(diff)

def analyze_diff_statistics(diff_content):
    """分析差异统计 - 统计新增行、删除行、变更区块"""
    added = sum(1 for line in diff_content if line.startswith('+') and not line.startswith('+++'))
    deleted = sum(1 for line in diff_content if line.startswith('-') and not line.startswith('---'))
    changed_blocks = sum(1 for line in diff_content if line.startswith('@@'))
    
    return added, deleted, changed_blocks

def parse_diff_blocks(diff_content, limit=50):
    """解析diff区块 - 提取变更的详细位置信息"""
    blocks = []
    current_block = {}
    
    for line in diff_content[:limit]:  # 限制分析行数
        if line.startswith('@@'):
            # 解析区块头信息：@@ -开始行,行数 +开始行,行数 @@
            match = re.match(r'@@ -(\d+),?(\d*) \+(\d+),?(\d*) @@', line)
            if match:
                if current_block:  # 保存上一个区块
                    blocks.append(current_block)
                
                # 解析行号信息
                start1 = int(match.group(1))
                count1 = int(match.group(2)) if match.group(2) else 1
                start2 = int(match.group(3))
                count2 = int(match.group(4)) if match.group(4) else 1
                
                current_block = {
                    'header': line.strip(),
                    'start1': start1,
                    'end1': start1 + count1 - 1,
                    'start2': start2,
                    'end2': start2 + count2 - 1,
                    'changes': []
                }
        elif line.startswith('-') and not line.startswith('---'):
            current_block['changes'].append(('delete', line[1:].rstrip()))
        elif line.startswith('+') and not line.startswith('+++'):
            current_block['changes'].append(('add', line[1:].rstrip()))
    
    if current_block:
        blocks.append(current_block)
    
    return blocks

def detect_key_changes(diff_content, keywords):
    """检测关键变更 - 识别特定的代码模式（如串口相关变更）"""
    key_changes = []
    for line in diff_content:
        if any(keyword.lower() in line.lower() for keyword in keywords):
            change_type = 'delete' if line.startswith('-') else 'add' if line.startswith('+') else 'context'
            key_changes.append((change_type, line.rstrip()))
    
    return key_changes

def generate_analysis_report(file1_info, file2_info, diff_content, analysis_report_path):
    """生成文本格式的详细分析报告"""
    with open(analysis_report_path, 'w', encoding='utf-8') as report:
        # 报告头部
        report.write("=" * 60 + "\n")
        report.write("                  代码差异分析报告\n")
        report.write("=" * 60 + "\n")
        report.write(f"生成时间: {datetime.now()}\n")
        report.write(f"比较文件: {file1_info['name']} ↔ {file2_info['name']}\n\n")
        
        # 1. 文件基本信息
        report.write("一、文件基本信息\n")
        report.write("=" * 25 + "\n")
        report.write("1. 源文件 (基准项目08):\n")
        report.write(f"   - 文件名: {file1_info['name']}\n")
        report.write(f"   - 路径: {file1_info['path']}\n")
        report.write(f"   - 大小: {file1_info['size']} 字节\n")
        report.write(f"   - 行数: {file1_info['lines']} 行\n\n")
        
        report.write("2. 目标文件:\n")
        report.write(f"   - 文件名: {file2_info['name']}\n")
        report.write(f"   - 路径: {file2_info['path']}\n")
        report.write(f"   - 大小: {file2_info['size']} 字节\n")
        report.write(f"   - 行数: {file2_info['lines']} 行\n\n")
        
        # 2. 差异统计
        added, deleted, changed_blocks = analyze_diff_statistics(diff_content)
        report.write("二、差异统计摘要\n")
        report.write("=" * 25 + "\n")
        report.write("1. 基本统计:\n")
        report.write(f"   - 基准文件总行数: {file1_info['lines']}\n")
        report.write(f"   - 目标文件总行数: {file2_info['lines']}\n")
        report.write(f"   - 行数差异: {file2_info['lines'] - file1_info['lines']} 行\n\n")
        
        report.write("2. 变更统计:\n")
        report.write(f"   - 新增行数: {added}\n")
        report.write(f"   - 删除行数: {deleted}\n")
        report.write(f"   - 变更区块数: {changed_blocks}\n\n")
        
        # 3. 详细差异分析
        report.write("三、详细差异分析\n")
        report.write("=" * 25 + "\n")
        
        if added == 0 and deleted == 0:
            report.write("✅ 两个文件内容完全一致\n")
        else:
            report.write(f"❌ 文件存在差异，共发现 {changed_blocks} 个变更区块\n\n")
            
            blocks = parse_diff_blocks(diff_content)
            for i, block in enumerate(blocks, 1):
                if i > 1:
                    report.write("\n\n")  # 区块间空行
                
                report.write(f"【变更区块 {i}】@@{block['start1']}-{block['end1']}行 ↔ {block['start2']}-{block['end2']}行@@\n")
                
                for change_type, content in block['changes'][:10]:  # 限制每个区块显示10个变更
                    if change_type == 'delete':
                        report.write(f"  ❌ 删除: {content}\n")
                    else:
                        report.write(f"      ✅ 新增: {content}\n")
            report.write("\n")
        
        # 4. 关键变更识别
        report.write("四、关键变更识别\n")
        report.write("=" * 25 + "\n")
        uart_keywords = ['HAL_UART', 'USART', '中断', 'interrupt']
        key_changes = detect_key_changes(diff_content, uart_keywords)
        
        if key_changes:
            report.write("🔧 检测到串口相关变更:\n")
            for change_type, content in key_changes[:5]:  # 显示前5个关键变更
                if change_type == 'delete':
                    report.write(f"  ❌ 删除: {content}\n")
                elif change_type == 'add':
                    report.write(f"     ✅ 新增: {content}\n")
        else:
            report.write("   未检测到明显的串口相关变更\n")
        report.write("\n")
        
        # 5. 总结与建议
        report.write("五、总结与建议\n")
        report.write("=" * 25 + "\n")
        
        if added == 0 and deleted == 0:
            report.write("✅ 文件完全相同，无需进一步操作\n")
        else:
            total_changes = added + deleted
            total_lines = max(file1_info['lines'], 1)  # 避免除零
            change_ratio = (total_changes * 100) // total_lines
            
            report.write("📊 变更程度分析:\n")
            report.write(f"   - 总变更行数: {total_changes}\n")
            report.write(f"   - 变更率: {change_ratio}%\n\n")
            report.write("💡 处理建议:\n")
            
            if change_ratio < 10:
                report.write("   轻微变更 - 建议重点审查具体变更行\n")
            elif change_ratio < 30:
                report.write("   中等变更 - 需要仔细审查变更逻辑\n")
            else:
                report.write("   重大变更 - 建议全面测试验证\n")
        
        report.write("\n" + "=" * 60 + "\n")
        report.write("报告生成完成\n")
        report.write("=" * 60 + "\n")
        
        # 添加HTML报告提示
        report.write("\n提示: 更直观的HTML格式差异报告可在 main差异分析HTML 目录中查看\n")

def find_project_main_files():
    """查找所有项目中的main.c文件 - 使用Bash脚本相同的扫描逻辑"""
    projects = {}
    base_project_path = None
    
    # 查找所有项目文件夹
    project_dirs = [d for d in os.listdir(BASE_DIR) 
                   if os.path.isdir(os.path.join(BASE_DIR, d)) 
                   and d != "项目分析报告"]
    
    for project_dir in project_dirs:
        full_path = os.path.join(BASE_DIR, project_dir)
        
        # 确定扫描目录 - 与Bash脚本相同的逻辑
        scan_dir = None
        if os.path.exists(os.path.join(full_path, "Core")):
            scan_dir = os.path.join(full_path, "Core")
        elif os.path.exists(os.path.join(full_path, "User")):
            scan_dir = os.path.join(full_path, "User")
        elif os.path.exists(os.path.join(full_path, "APP")):
            scan_dir = os.path.join(full_path, "APP")
        
        if not scan_dir:
            continue
        
        # 查找main.c文件
        main_c_path = os.path.join(scan_dir, "Src", "main.c")
        if os.path.isfile(main_c_path):
            # 保存项目信息
            projects[project_dir] = main_c_path
            
            # 检查是否是基准项目
            if project_dir == BASE_PROJECT:
                base_project_path = main_c_path
    
    return projects, base_project_path

def compare_with_base_project():
    """将所有项目与基准项目08进行比较"""
    # 确保报告目录存在
    Path(REPORT_DIR).mkdir(parents=True, exist_ok=True)
    Path(HTML_REPORT_DIR).mkdir(parents=True, exist_ok=True)  # 创建HTML报告目录
    
    # 查找所有项目中的main.c文件
    projects, base_project_path = find_project_main_files()
    if not projects:
        print("未找到任何项目中的main.c文件")
        return
    
    if not base_project_path:
        print(f"错误: 未找到基准项目 {BASE_PROJECT} 的 main.c 文件")
        return
    
    # 获取基准项目文件信息
    base_info = get_file_info(base_project_path)
    if not base_info:
        print(f"错误: 无法读取基准项目文件 {base_project_path}")
        return
    
    # 比较所有项目与基准项目
    for project_name, project_file in projects.items():
        # 跳过基准项目自身
        if project_name == BASE_PROJECT:
            continue
        
        # 获取项目文件信息
        project_info = get_file_info(project_file)
        if not project_info:
            print(f"跳过对比: {project_file} 不存在")
            continue
        
        # 生成文本报告文件名
        report_name = f"项目08_vs_{project_name}_差异分析.txt"
        report_path = os.path.join(REPORT_DIR, report_name)
        
        # 生成HTML报告文件名
        html_report_name = f"项目08_vs_{project_name}_差异分析.html"
        html_report_path = os.path.join(HTML_REPORT_DIR, html_report_name)
        
        # 生成差异内容
        diff_content = generate_diff_content(base_project_path, project_file)
        
        # 生成HTML差异报告
        generate_html_diff_report(base_project_path, project_file, html_report_path)
        
        # 生成文本分析报告
        generate_analysis_report(base_info, project_info, diff_content, report_path)
        
        print(f"已生成对比报告: 项目08 vs {project_name}")
        print(f"   - 文本报告: {report_path}")
        print(f"   - HTML报告: {html_report_path}")

def main():
    """主函数 - 协调整个差异分析流程"""
    try:
        print("开始扫描项目并与项目08进行对比...")
        compare_with_base_project()
        print("\n✅ 所有差异分析完成！")
        print(f"📊 文本报告已保存至: {REPORT_DIR}")
        print(f"🌐 HTML报告已保存至: {HTML_REPORT_DIR}")
        
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()  # 打印详细的错误堆栈
        sys.exit(1)

if __name__ == "__main__":
    main()
