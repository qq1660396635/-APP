#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件名: file_splitter.py
作者: 脚本助手
功能: 文件拆分工具 - 还原合并的文件
创建时间: 2025年11月
描述: 解析合并后的文件，将其拆分为原始的独立文件
"""

import os
import re
import sys
from pathlib import Path
from datetime import datetime

# 尝试导入Word处理库
try:
    from docx import Document
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False

class FileSplitter:
    """文件拆分器"""
    
    def __init__(self):
        self.input_file = ""
        self.output_dir = ""
        
    def display_menu(self):
        """显示主菜单"""
        print("=" * 60)
        print("           文件拆分工具")
        print("=" * 60)
        print("\n请选择要拆分的文件类型：")
        print("1. 拆分TXT合并文件")
        print("2. 拆分Python合并文件")
        print("3. 拆分除HTML外所有文件的合并")
        print("4. 拆分DOCX合并文件（实验性功能）")
        print("q. 退出程序")
        
    def get_user_choice(self):
        """获取用户选择"""
        self.display_menu()
        
        while True:
            choice = input("\n请输入选择 (1/2/3/4/q): ").strip()
            
            if choice.lower() == 'q':
                return None
            
            if choice in ['1', '2', '3', '4']:
                if choice == '4' and not DOCX_AVAILABLE:
                    print("❌ DOCX拆分功能不可用，请先安装库：")
                    print("   pip install python-docx")
                    continue
                return choice
            
            print("❌ 无效选择，请重新输入！")
    
    def get_input_file(self):
        """获取输入文件路径"""
        default_file = "/storage/emulated/0/Download/合并_TXT文件.txt"
        
        print(f"\n请输入要拆分的文件路径：")
        print(f"（直接回车使用默认文件: {default_file}）")
        
        while True:
            user_input = input("> ").strip()
            
            if not user_input:
                self.input_file = default_file
            else:
                self.input_file = user_input
            
            if os.path.exists(self.input_file):
                print(f"✅ 使用文件: {self.input_file}")
                return True
            else:
                print(f"❌ 文件不存在: {self.input_file}")
                print("请重新输入或按 Ctrl+C 退出")
    
    def get_output_directory(self):
        """获取输出目录"""
        # 基于输入文件名创建输出目录
        input_path = Path(self.input_file)
        base_name = input_path.stem
        parent_dir = input_path.parent
        
        default_output = parent_dir / f"{base_name}_拆分结果"
        
        print(f"\n请输入拆分文件的输出目录：")
        print(f"（直接回车使用默认目录: {default_output}）")
        
        while True:
            user_input = input("> ").strip()
            
            if not user_input:
                self.output_dir = str(default_output)
            else:
                self.output_dir = user_input
            
            # 创建输出目录
            try:
                os.makedirs(self.output_dir, exist_ok=True)
                print(f"✅ 输出目录: {self.output_dir}")
                return True
            except Exception as e:
                print(f"❌ 无法创建目录 {self.output_dir}: {e}")
                print("请重新输入")
    
    def parse_text_merged_file(self, file_path):
        """解析文本合并文件的结构"""
        files_info = []
        current_file = None
        content_lines = []
        reading_content = False
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except UnicodeDecodeError:
            try:
                with open(file_path, 'r', encoding='gbk') as f:
                    lines = f.readlines()
            except:
                print("❌ 无法读取文件，编码不支持")
                return []
        
        for line in lines:
            line = line.rstrip('\n\r')
            
            # 检测文件分隔符
            if line.startswith('--- ') and ' ⬇️⬇️⬇️⬇️⬇️ ---' in line:
                # 保存前一个文件的内容
                if current_file and content_lines:
                    current_file['content'] = '\n'.join(content_lines)
                    files_info.append(current_file)
                
                # 开始新文件
                filename = line.replace('--- ', '').replace(' ⬇️⬇️⬇️⬇️⬇️ ---', '').strip()
                current_file = {
                    'filename': filename,
                    'size': 0,
                    'mod_time': '',
                    'content': ''
                }
                content_lines = []
                reading_content = False
                continue
            
            # 检测文件信息
            if current_file and not reading_content:
                if line.startswith('文件大小:'):
                    current_file['size'] = line.split(':', 1)[1].strip().replace(' 字节', '')
                elif line.startswith('修改时间:'):
                    current_file['mod_time'] = line.split(':', 1)[1].strip()
                elif line == '-------------------------':
                    reading_content = True
                continue
            
            # 收集文件内容
            if reading_content and current_file:
                content_lines.append(line)
        
        # 保存最后一个文件
        if current_file and content_lines:
            current_file['content'] = '\n'.join(content_lines)
            files_info.append(current_file)
        
        return files_info
    
    def split_text_files(self):
        """拆分文本合并文件"""
        print("\n🔄 正在解析合并文件结构...")
        
        # 解析文件结构
        files_info = self.parse_text_merged_file(self.input_file)
        
        if not files_info:
            print("❌ 未能解析出任何文件信息")
            return False
        
        print(f"📁 发现 {len(files_info)} 个文件，开始拆分...")
        
        success_count = 0
        
        for i, file_info in enumerate(files_info, 1):
            try:
                filename = file_info['filename']
                content = file_info['content']
                
                output_path = os.path.join(self.output_dir, filename)
                
                # 写入文件
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                # 尝试设置文件时间（如果有的话）
                if file_info['mod_time']:
                    try:
                        mod_time = datetime.strptime(file_info['mod_time'], '%Y-%m-%d %H:%M:%S')
                        timestamp = mod_time.timestamp()
                        os.utime(output_path, (timestamp, timestamp))
                    except:
                        pass  # 忽略时间设置错误
                
                print(f"✅ {i:2d}. {filename}")
                success_count += 1
                
            except Exception as e:
                print(f"❌ {i:2d}. {file_info['filename']} - 错误: {e}")
        
        print(f"\n🎉 拆分完成！成功: {success_count}/{len(files_info)}")
        print(f"📂 输出目录: {self.output_dir}")
        return True
    
    def split_docx_files(self):
        """拆分DOCX合并文件（实验性功能）"""
        if not DOCX_AVAILABLE:
            print("❌ DOCX拆分功能不可用")
            return False
        
        try:
            print("\n🔄 正在解析DOCX合并文件...")
            doc = Document(self.input_file)
            
            files_info = []
            current_file = None
            current_content = []
            
            for paragraph in doc.paragraphs:
                text = paragraph.text.strip()
                
                # 检测文件分隔符
                if text.startswith('--- ') and ' ⬇️⬇️⬇️⬇️⬇️ ---' in text:
                    # 保存前一个文件
                    if current_file and current_content:
                        current_file['content'] = '\n'.join(current_content)
                        files_info.append(current_file)
                    
                    # 开始新文件
                    filename = text.replace('--- ', '').replace(' ⬇️⬇️⬇️⬇️⬇️ ---', '').strip()
                    current_file = {'filename': filename, 'content': ''}
                    current_content = []
                    continue
                
                # 收集内容（跳过分隔线等）
                if current_file and text and text != '-------------------------':
                    current_content.append(text)
            
            # 保存最后一个文件
            if current_file and current_content:
                current_file['content'] = '\n'.join(current_content)
                files_info.append(current_file)
            
            if not files_info:
                print("❌ 未能解析出任何文件信息")
                return False
            
            print(f"📁 发现 {len(files_info)} 个文件，开始拆分...")
            
            success_count = 0
            for i, file_info in enumerate(files_info, 1):
                try:
                    filename = file_info['filename']
                    content = file_info['content']
                    
                    # 确保有扩展名
                    if not '.' in filename:
                        filename += '.txt'
                    
                    output_path = os.path.join(self.output_dir, filename)
                    
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    print(f"✅ {i:2d}. {filename}")
                    success_count += 1
                    
                except Exception as e:
                    print(f"❌ {i:2d}. {file_info['filename']} - 错误: {e}")
            
            print(f"\n🎉 拆分完成！成功: {success_count}/{len(files_info)}")
            print(f"📂 输出目录: {self.output_dir}")
            return True
            
        except Exception as e:
            print(f"❌ 拆分DOCX文件时出错: {e}")
            return False
    
    def run_split(self, choice):
        """执行拆分操作"""
        # 根据选择执行不同的拆分
        if choice == "4":  # DOCX文件
            print(f"\n🔄 开始拆分DOCX文件...")
            success = self.split_docx_files()
        else:  # 文本文件
            print(f"\n🔄 开始拆分文本文件...")
            success = self.split_text_files()
        
        if success:
            print("\n✨ 拆分任务完成！")
            return True
        else:
            print("\n❌ 拆分失败！")
            return False

def main():
    """主函数"""
    splitter = FileSplitter()
    
    # 获取用户选择
    choice = splitter.get_user_choice()
    if choice is None:
        print("👋 程序已退出")
        return
    
    # 获取输入文件
    if not splitter.get_input_file():
        return
    
    # 获取输出目录
    if not splitter.get_output_directory():
        return
    
    # 执行拆分
    splitter.run_split(choice)

if __name__ == "__main__":
    main()
