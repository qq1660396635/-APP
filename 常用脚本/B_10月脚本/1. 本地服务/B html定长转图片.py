python3 -x <<'EOF'
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
2000×3000 固定截图（一次成型）
"""
import os, subprocess, sys
from PIL import Image

# ---------- 可配参数 ----------
HTML_FILE   = "/storage/emulated/0/Download/OnePlus Share/GITHUB 开源项目/项目01/野火小智文档/项目分析报告/main差异分析HTML/项目08_vs_[25-2] TIM通道捕获应用之超声波测距_差异分析.html"
OUTPUT_FILE = "/storage/emulated/0/Download/QQ/项目08_vs_[16] 火焰传感器触发蜂鸣器_差异分析_optimized.png"
WIDTH       = 2000   # 固定宽度
HEIGHT      = 3000   # 固定高度
# ------------------------------

def shoot(html, out, width=2000, height=3000):
    cmd = ["chromium-browser", "--headless", "--disable-gpu", "--no-sandbox",
           "--run-all-compositor-stages-before-draw", "--virtual-time-budget=30000",
           f"--window-size={width},{height}", f"--screenshot={out}", f"file://{html}"]
    return subprocess.run(cmd, capture_output=True).returncode == 0

def main():
    print(f"截图 {WIDTH}×{HEIGHT} …")
    if shoot(HTML_FILE, OUTPUT_FILE, WIDTH, HEIGHT):
        print(f"✅ 完成！{WIDTH}×{HEIGHT}\n📁 {OUTPUT_FILE}")
    else:
        print("截图失败")

if __name__ == "__main__":
    main()
EOF





#   脚本二  ，遍历整个目录下的html合并
python3 -x <<'EOF'
import os, subprocess, glob, tempfile, shutil

# ① 路径带空格 → 用引号包起来
DIR   = "/storage/emulated/0/Download/OnePlus Share/GITHUB 开源项目/项目01/野火小智文档/项目分析报告/main差异分析HTML"
WIDTH = 2000
HEIGHT = 3000
PDF   = os.path.join(DIR, "merged.pdf")

# ② 找 chromium
chromium = shutil.which("chromium-browser") or shutil.which("chrome") or "chromium-browser"

def shot(html, png):
    cmd = [chromium, "--headless", "--disable-gpu", "--no-sandbox",
           "--run-all-compositor-stages-before-draw", "--virtual-time-budget=30000",
           f"--window-size={WIDTH},{HEIGHT}", f"--screenshot={png}", f"file://{html}"]
    cp = subprocess.run(cmd, capture_output=True, text=True)
    if cp.returncode != 0:
        print("!!! chromium 报错:\n", cp.stderr[:400])
    return cp.returncode == 0

with tempfile.TemporaryDirectory() as tmp:
    pngs = []
    for f in sorted(glob.glob(os.path.join(DIR, "*.html"))):
        png = os.path.join(tmp, os.path.basename(f).replace(".html", ".png"))
        if shot(f, png):
            pngs.append(png)
        else:
            break
    if not pngs:
        print("❌ 无 PNG"); exit()

    subprocess.run(["magick"] + pngs + [PDF], check=True)
    print("✅ merged.pdf 完成 →", os.path.basename(PDF))

# 临时 PNG 随 tmp 目录自动消失
EOF
