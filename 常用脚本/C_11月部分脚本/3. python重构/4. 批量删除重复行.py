import re
import os

def clean_line(line):
    # 去掉行号前缀，如 "123. "
    return re.sub(r'^\d+\.\s*', '', line).strip()

def deduplicate_file_lines(input_filename):
    # 自动加双引号防止空格问题
    input_filename = f'"{input_filename}"'
    input_filename = input_filename.strip('"')  # 去掉多余引号，防止重复加

    if not os.path.isfile(input_filename):
        print(f"❌ 文件不存在：{input_filename}")
        return

    seen = set()
    output_filename = input_filename.replace('.txt', '_dedup.txt')

    with open(input_filename, 'r', encoding='utf-8') as infile, \
         open(output_filename, 'w', encoding='utf-8') as outfile:
        
        for line in infile:
            cleaned = clean_line(line)
            if cleaned and cleaned not in seen:
                seen.add(cleaned)
                outfile.write(cleaned + '\n')

    print(f"✅ 去重完成，输出文件：{output_filename}")

# === 主程序 ===
if __name__ == "__main__":
    filename = input("请输入要处理的文件名（如：python_libraries_part1.txt）：\n").strip()
    deduplicate_file_lines(filename)
