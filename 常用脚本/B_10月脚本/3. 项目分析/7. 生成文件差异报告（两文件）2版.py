python3 -x <<'EOF'   #   Python转bash
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import re
import difflib
import argparse
from datetime import datetime
from pathlib import Path

def parse_arguments():
    """处理命令行参数或使用默认路径"""
    if len(sys.argv) == 4:  # 三个参数：文件1、文件2、输出目录
        file1, file2, report_dir = sys.argv[1], sys.argv[2], sys.argv[3]
    elif len(sys.argv) == 1:  # 无参数，使用默认路径
        file1 = "/storage/emulated/0/Download/OnePlus Share/GITHUB 开源项目/项目01/野火小智文档/[19-5]串口接收之中断接收定长数据/Core/Src/main.c"
        file2 = "/storage/emulated/0/Download/OnePlus Share/GITHUB 开源项目/项目01/野火小智文档/[19-7]串口接收之空闲中断接收不定长数据/Core/Src/main.c"
        report_dir = "/storage/emulated/0/Download/OnePlus Share/GITHUB 开源项目/项目01/野火小智文档/项目分析报告/差异文件/"
    else:  # 参数数量不正确
        print(f"用法: {sys.argv[0]} [文件1 文件2 输出目录]")
        print(f"示例: {sys.argv[0]} /path/to/file1.c /path/to/file2.c /path/to/output")
        print("注意: 不带参数使用默认路径")
        sys.exit(1)
    
    return file1, file2, report_dir

def initialize_settings(report_dir):
    """创建时间戳和报告文件路径"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    html_diff_report = os.path.join(report_dir, f"代码差异报告_{timestamp}.html")
    analysis_report = os.path.join(report_dir, f"差异分析报告_{timestamp}.txt")
    
    # 创建输出目录
    Path(report_dir).mkdir(parents=True, exist_ok=True)
    
    return timestamp, html_diff_report, analysis_report

def check_files(file1, file2):
    """验证文件是否存在且可访问"""
    if not os.path.isfile(file1):
        raise FileNotFoundError(f"文件不存在: {file1}")
    if not os.path.isfile(file2):
        raise FileNotFoundError(f"文件不存在: {file2}")

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

def generate_html_diff_report(file1, file2, html_report_path):
    """生成HTML格式的差异报告"""
    file1_lines, enc1 = safe_read_file(file1)
    file2_lines, enc2 = safe_read_file(file2)
    
    # 生成HTML格式的diff报告
    html_diff = difflib.HtmlDiff().make_file(
        file1_lines, file2_lines, 
        fromdesc=file1, todesc=file2,
        context=True, numlines=3
    )
    
    with open(html_report_path, 'w', encoding='utf-8') as html_file:
        html_file.write(html_diff)
    
    return html_diff

def get_file_info(filepath):
    """获取文件基本信息 - 大小、行数等"""
    file_stat = os.stat(filepath)
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        line_count = sum(1 for _ in f)
    
    return {
        'name': os.path.basename(filepath),
        'path': os.path.dirname(filepath),
        'size': file_stat.st_size,
        'lines': line_count
    }

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
        report.write("1. 源文件:\n")
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
        report.write(f"   - 源文件总行数: {file1_info['lines']}\n")
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

def main():
    """主函数 - 协调整个差异分析流程"""
    try:
        # 1. 参数解析
        file1, file2, report_dir = parse_arguments()
        
        # 2. 初始化设置
        timestamp, html_diff_report, analysis_report = initialize_settings(report_dir)
        
        # 3. 文件检查
        check_files(file1, file2)
        
        # 4. 获取文件信息
        file1_info = get_file_info(file1)
        file2_info = get_file_info(file2)
        
        # 5. 生成HTML格式的差异报告
        generate_html_diff_report(file1, file2, html_diff_report)
        
        # 6. 生成内存中的diff内容用于分析
        diff_content = generate_diff_content(file1, file2)
        
        # 7. 生成文本格式的详细分析报告
        generate_analysis_report(file1_info, file2_info, diff_content, analysis_report)
        
        # 8. 输出完成信息
        print("✅ 差异分析完成！\n")
        print("📊 生成的报告文件:")
        print(f"   1. HTML代码差异报告: {html_diff_report}")
        print(f"   2. 文本差异分析报告: {analysis_report}\n")
        print("💡 使用提示:")
        print("   - HTML报告提供直观的代码差异可视化")
        print("   - 文本分析报告包含所有关键差异信息")
        print(f"   - 可通过参数指定文件路径: {sys.argv[0]} 文件1 文件2 输出目录")
        
    except Exception as e:
        print(f"错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

EOF