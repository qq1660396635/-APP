# 生成项目 函数差异报告，便于AI分析
python3 -x <<'EOF'   #   Python转bash
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import re
import difflib
from datetime import datetime
from pathlib import Path

# ==================== 配置文件区域 ====================
# 用户可以修改以下配置参数

# 基础目录配置
BASE_DIR = "/storage/emulated/0/Download/OnePlus Share/GITHUB 开源项目/项目01/野火小智文档"
REPORT_DIR_NAME = "main函数差异"  # 报告目录名称
BASE_PROJECT = "[8] STM32CubeMX新建MDK工程"  # 基准项目名称
REPORT_EXTENSION = ".c"  # 报告文件扩展名

# 文件扫描配置
SCAN_DIRS = ["Core", "User", "APP"]  # 扫描的目录名称
MAIN_FILE_PATH = "Src"  # main.c文件所在的子目录

# 函数提取配置
FUNCTION_PATTERN = r'(\w+[\w\s*]+\s+\**\s*(\w+)\s*\([^{]*\))\s*\{'  # 匹配函数定义的正则表达式

# 报告格式配置
REPORT_WIDTH = 60  # 报告分隔线宽度
SECTION_WIDTH = 25  # 章节标题宽度

# ==================== 以下为程序代码 ====================

# 计算完整的报告目录路径
REPORT_DIR = os.path.join(BASE_DIR, "项目分析报告", REPORT_DIR_NAME)

def safe_read_file(filepath):
    """安全读取文件，处理编码问题"""
    encodings = ['utf-8', 'gbk', 'gb2312', 'latin-1']
    for encoding in encodings:
        try:
            with open(filepath, 'r', encoding=encoding) as f:
                return f.read(), encoding
        except UnicodeDecodeError:
            continue
    # 如果所有编码都失败，使用忽略错误的方式读取
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read(), 'utf-8'

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

def extract_functions(content):
    """从C代码中提取函数定义"""
    functions = {}
    
    # 查找所有函数定义
    matches = list(re.finditer(FUNCTION_PATTERN, content, re.MULTILINE | re.DOTALL))
    
    for i, match in enumerate(matches):
        func_signature = match.group(1)  # 完整的函数签名
        func_name = match.group(2)      # 函数名
        
        # 查找函数的开始和结束位置
        start_pos = match.start()
        
        # 查找匹配的大括号来确定函数体范围
        brace_count = 0
        func_start = -1
        func_end = -1
        
        # 从匹配位置开始查找函数体的开始
        pos = content.find('{', start_pos)
        if pos != -1:
            func_start = pos
            brace_count = 1
            pos += 1
            
            # 查找匹配的结束大括号
            while pos < len(content) and brace_count > 0:
                if content[pos] == '{':
                    brace_count += 1
                elif content[pos] == '}':
                    brace_count -= 1
                pos += 1
            
            if brace_count == 0:
                func_end = pos
                func_body = content[func_start:func_end]
                functions[func_name] = {
                    'signature': func_signature,
                    'body': func_body,
                    'full_function': func_signature + func_body
                }
    
    return functions

def compare_functions(base_functions, target_functions):
    """比较两个文件中的函数差异"""
    differences = {
        'added': {},      # 目标文件中新增的函数
        'deleted': {},    # 目标文件中删除的函数  
        'modified': {}    # 修改的函数（两个文件中都有但内容不同）
    }
    
    # 查找新增的函数
    for func_name in target_functions:
        if func_name not in base_functions:
            differences['added'][func_name] = target_functions[func_name]
    
    # 查找删除的函数
    for func_name in base_functions:
        if func_name not in target_functions:
            differences['deleted'][func_name] = base_functions[func_name]
    
    # 查找修改的函数
    for func_name in base_functions:
        if func_name in target_functions:
            base_func = base_functions[func_name]['full_function']
            target_func = target_functions[func_name]['full_function']
            
            if base_func != target_func:
                differences['modified'][func_name] = {
                    'base': base_functions[func_name],
                    'target': target_functions[func_name]
                }
    
    return differences

def generate_function_diff_report(file1_info, file2_info, differences, report_path):
    """生成函数级别的差异报告（带序号和表情符号）"""
    with open(report_path, 'w', encoding='utf-8') as report:
        # 报告头部
        report.write("=" * REPORT_WIDTH + "\n")
        report.write("                  函数级别差异分析报告\n")
        report.write("=" * REPORT_WIDTH + "\n")
        report.write(f"生成时间: {datetime.now()}\n")
        report.write(f"比较文件: {file1_info['name']} ↔ {file2_info['name']}\n\n")
        
        # 1. 文件基本信息
        report.write("一、文件基本信息\n")
        report.write("=" * SECTION_WIDTH + "\n")
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
        
        # 2. 函数差异统计
        report.write("二、函数差异统计\n")
        report.write("=" * SECTION_WIDTH + "\n")
        report.write(f"1. 新增函数: {len(differences['added'])} 个\n")
        report.write(f"2. 删除函数: {len(differences['deleted'])} 个\n")
        report.write(f"3. 修改函数: {len(differences['modified'])} 个\n")
        report.write(f"4. 总差异函数: {len(differences['added']) + len(differences['deleted']) + len(differences['modified'])} 个\n\n")
        
        # 3. 详细函数差异（带序号和表情符号）
        report.write("三、详细函数差异\n")
        report.write("=" * SECTION_WIDTH + "\n")
        
        # 3.1 新增函数（使用绿色对勾表情和序号）
        if differences['added']:
            report.write("\n🎯 新增函数:\n")
            report.write("-" * 20 + "\n")
            for i, (func_name, func_info) in enumerate(differences['added'].items(), 1):
                report.write(f"\n🔸 第{i}个新增函数: {func_name}\n")
                report.write(f"完整函数:\n{func_info['full_function']}\n")
                report.write("-" * 40 + "\n")
        
        # 3.2 删除函数（使用红色叉号表情和序号）
        if differences['deleted']:
            report.write("\n🎯 删除函数:\n")
            report.write("-" * 20 + "\n")
            for i, (func_name, func_info) in enumerate(differences['deleted'].items(), 1):
                report.write(f"\n❌ 第{i}个删除函数: {func_name}\n")
                report.write(f"完整函数:\n{func_info['full_function']}\n")
                report.write("-" * 40 + "\n")
        
        # 3.3 修改函数（使用黄色警告表情和序号）
        if differences['modified']:
            report.write("\n🎯 修改函数:\n")
            report.write("-" * 20 + "\n")
            for i, (func_name, func_info) in enumerate(differences['modified'].items(), 1):
                report.write(f"\n⚠️ 第{i}个修改函数: {func_name}\n")
                
                report.write("\n📄 基准项目中的函数:\n")
                report.write(func_info['base']['full_function'])
                
                report.write("\n\n📄 目标项目中的函数:\n")
                report.write(func_info['target']['full_function'])
                
                report.write("\n" + "=" * 50 + "\n")
        
        # 4. 总结
        report.write("\n四、总结\n")
        report.write("=" * SECTION_WIDTH + "\n")
        
        total_changes = len(differences['added']) + len(differences['deleted']) + len(differences['modified'])
        
        if total_changes == 0:
            report.write("✅ 两个文件的函数内容完全一致\n")
        else:
            report.write(f"📊 共发现 {total_changes} 个函数存在差异\n")
            report.write("\n💡 处理建议:\n")
            
            if len(differences['modified']) > 0:
                report.write("   ⚠️  重点关注修改函数，检查逻辑变更\n")
            if len(differences['added']) > 0:
                report.write("   🔸 验证新增函数的功能和必要性\n")
            if len(differences['deleted']) > 0:
                report.write("   ❌ 确认删除函数不会影响现有功能\n")
        
        report.write("\n" + "=" * REPORT_WIDTH + "\n")
        report.write("报告生成完成\n")
        report.write("=" * REPORT_WIDTH + "\n")

def find_project_main_files():
    """查找所有项目中的main.c文件"""
    projects = {}
    base_project_path = None
    
    # 查找所有项目文件夹
    project_dirs = [d for d in os.listdir(BASE_DIR) 
                   if os.path.isdir(os.path.join(BASE_DIR, d)) 
                   and d != "项目分析报告"]
    
    for project_dir in project_dirs:
        full_path = os.path.join(BASE_DIR, project_dir)
        
        # 确定扫描目录
        scan_dir = None
        for possible_dir in SCAN_DIRS:
            if os.path.exists(os.path.join(full_path, possible_dir)):
                scan_dir = os.path.join(full_path, possible_dir)
                break
        
        if not scan_dir:
            continue
        
        # 查找main.c文件
        main_c_path = os.path.join(scan_dir, MAIN_FILE_PATH, "main.c")
        if os.path.isfile(main_c_path):
            projects[project_dir] = main_c_path
            
            # 检查是否是基准项目
            if project_dir == BASE_PROJECT:
                base_project_path = main_c_path
    
    return projects, base_project_path

def compare_with_base_project():
    """将所有项目与基准项目08进行比较"""
    # 确保报告目录存在
    Path(REPORT_DIR).mkdir(parents=True, exist_ok=True)
    
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
    
    # 读取基准项目内容并提取函数
    base_content, base_encoding = safe_read_file(base_project_path)
    base_functions = extract_functions(base_content)
    print(f"基准项目 {BASE_PROJECT} 中找到 {len(base_functions)} 个函数")
    
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
        
        # 读取目标项目内容并提取函数
        project_content, project_encoding = safe_read_file(project_file)
        project_functions = extract_functions(project_content)
        print(f"项目 {project_name} 中找到 {len(project_functions)} 个函数")
        
        # 比较函数差异
        differences = compare_functions(base_functions, project_functions)
        
        # 生成报告文件名
        report_name = f"项目08_vs_{project_name}_函数差异分析{REPORT_EXTENSION}"
        report_path = os.path.join(REPORT_DIR, report_name)
        
        # 生成函数级别分析报告
        generate_function_diff_report(base_info, project_info, differences, report_path)
        
        print(f"已生成函数对比报告: 项目08 vs {project_name}")
        print(f"   - 报告路径: {report_path}")
        print(f"   - 发现差异: 新增{len(differences['added'])}个, 删除{len(differences['deleted'])}个, 修改{len(differences['modified'])}个函数")

def main():
    """主函数 - 协调整个函数差异分析流程"""
    try:
        print("开始扫描项目并与项目08进行函数级别对比...")
        compare_with_base_project()
        print("\n✅ 所有函数差异分析完成！")
        print(f"📊 报告已保存至: {REPORT_DIR}")
        
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

EOF