需求   一次性 bash 内嵌 Python3脚本
1.     一次性读取 30 个问题（自动校验，不足 30 个直接退出）。
2.    每问一次 Moonshot API，不携带历史，保证全新回答。
3.    回答按「教科书大纲：章节速览 → 一级→二级→正文（TXT 代码块，人话+名词解释）」格式输出。
4.    结果保存在
 /storage/emulated/0/Download/OnePlus Share/GITHUB 开源项目/项目01/回答/YYYYmmdd_HHMMSS/ 
文件名为  Q01.txt  …  Q30.txt ，序号与 questions.txt 严格对应。
---------------- 复制即跑 ----------------


python3 - <<'EOF'
# ---------- 唯一需要改的 ----------
API_KEY = "sk-哥们你自己的要是🔑🔑🔑"
QUESTIONS_FILE = "/storage/emulated/0/Download/OnePlus Share/GITHUB 开源项目/项目01/questions.txt"
OUTPUT_DIR_PARENT = "/storage/emulated/0/Download/OnePlus Share/GITHUB 开源项目/项目01"
# ----------------------------------

import sys, time, pathlib, requests, datetime

q_path = pathlib.Path(QUESTIONS_FILE)
if not q_path.exists():
    sys.exit(f"[ERR] 问题文件不存在：{q_path}")

# 轻量校验：必须恰好 30 行非空问题
with q_path.open(encoding='utf-8') as f:
    questions = [line.strip() for line in f if line.strip()]
if len(questions) != 30:
    sys.exit(f"[ERR] 问题数量必须是 30 个，当前 {len(questions)} 个")

# 创建输出目录：项目01/回答/YYYYmmdd_HHMMSS/
ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
out_dir = pathlib.Path(OUTPUT_DIR_PARENT) / "回答" / ts
out_dir.mkdir(parents=True, exist_ok=True)

url = "https://api.moonshot.cn/v1/chat/completions"
hdr = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

def ask_once(q: str) -> str:
    """单问单答，失败抛异常"""
    prompt = f"""
【教科书大纲示例】（EXT4 进化史）
结论一句话：EXT4 就是把 32 位限制砸掉、再给小文件“拼车”、给大文件“包机”的 EXT3 超级升级版，至今仍是 Linux 默认根文件系统老大哥。
----------------------------------------------------------------
第0章 读前防呆
0.1 只聊“EXT 家史”+EXT4 质变，不教 mkfs 参数
0.2 生词→右侧“人话卡”秒懂
0.3 每章末尾“快问快答”——面试/装系统/吹水前背两句
----------------------------------------------------------------
第1章 四代同堂一张图
1.1 1992 EXT——婴儿期
（以下继续照此风格展开）

你是一位「Linux 内存管理」课程助教，请把回答整理成“教科书”风格：
1. 先给【章节速览】一句话总结；
2. 正文按 一级标题→二级标题→正文 逐级展开；
3. 正文使用 TXT 代码块（```txt ... ```）包裹；
4. 遇到专业名词，用括号插播一句“人话解释”；
5. 保持口语化，禁止跑题；
6. 不输出任何与课程无关的寒暄。

问题：{q}
"""
    payload = {
        "model": "kimi-k2-turbo-preview",
        "messages": [{"role": "user", "content": prompt.strip()}],
        "temperature": 0.35,
        "max_tokens": 32000
    }
    for attempt in range(1, 6):
        try:
            r = requests.post(url, headers=hdr, json=payload, timeout=180)
            if r.status_code == 429:
                time.sleep(2 ** attempt)
                continue
            r.raise_for_status()
            return r.json()["choices"][0]["message"]["content"].strip()
        except Exception as e:
            print(f"[WARN] 第{attempt}次失败: {e}")
            time.sleep(2)
    raise RuntimeError("多次重试仍失败")

# 再读一次文件，逐条处理，保证“一次只读一个问题”
with q_path.open(encoding='utf-8') as f:
    for idx, raw_line in enumerate(f, 1):
        q = raw_line.strip()
        if not q:           # 跳过空行
            continue
        print(f"[{idx:02}/30] 提问：{q}")
        ans = ask_once(q)
        out_file = out_dir / f"Q{idx:02d}.txt"
        out_file.write_text(ans, encoding='utf-8')
        print(f"      已写入：{out_file.name}  （{len(ans)} 字）")

print(f"\n[ALL DONE] 30 个回答已保存到 → {out_dir}")
EOF
