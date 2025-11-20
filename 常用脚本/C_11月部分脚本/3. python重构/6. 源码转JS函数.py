#!/usr/bin/env python3
# ==================  唯一需要改的地方  ==================
TARGET_DIR = "/storage/emulated/0/Download/OnePlus Share/03 - 个人测试/常用工具转安卓/常用脚本/B_10月脚本/"
# =======================================================

import os, glob
from datetime import datetime

# 统一工作目录：输入、输出都在 TARGET_DIR
os.chdir(TARGET_DIR)
OUT_FILE = os.path.join(TARGET_DIR, "scripts_library.js")

def esc(s):
    """转义 JS 模板字符串"""
    return s.replace("\\", "\\\\").replace("`", "\\`").replace("${", "\\${")

def main():
    if not os.path.isdir(TARGET_DIR):
        print("❌ 目录不存在:", TARGET_DIR)
        return

    js_vars, idx = [], 1
    # 1. 遍历三种脚本扩展名
    for pat in ("**/*.bash", "**/*.py", "**/*.sh"):
        for f in sorted(glob.glob(pat, recursive=True)):
            if f.endswith((".bak", "~")):          # 跳过备份文件
                continue
            var = f"a{idx:03d}"                   # 变量名：a001, a002, ...
            try:
                txt = open(f, encoding="utf-8", errors="ignore").read()
            except Exception as e:
                print(f"[警告] 读取失败 {f}: {e}")
                continue

            # 2. 拼 JS 变量（带序号注释）
            js_vars.append(
                f"// [{idx:02d}] {f}\n"
                f"var {var} = {{\n"
                f"  index:{idx},                    // 数字序号\n"
                f"  filename:'{f}',                 // 相对路径\n"
                f"  content:`{esc(txt)}`,           // 文件内容\n"
                f"  type:'{'bash' if f.endswith(('.bash','.sh')) else 'python'}',  // 脚本类型\n"
                f"  size:{len(txt)}                 // 字符数\n"
                f"}};"
            )
            print(f"[{idx:02d}] {f}  ({len(txt)} 字符)")
            idx += 1

    if not js_vars:
        print("❌ 未找到任何脚本")
        return

    # 3. 写文件：头部注释 + 所有变量
    hdr = (f"// ==========================================\n"
           f"// 自动生成于 {datetime.now():%F %T}\n"
           f"// 源目录: {TARGET_DIR}\n"
           f"// 共 {len(js_vars)} 个文件\n"
           f"// ==========================================\n\n")
    open(OUT_FILE, "w", encoding="utf-8").write(hdr + "\n\n".join(js_vars))
    print(f"\n✅ 已生成: {OUT_FILE}")

if __name__ == "__main__":
    main()

