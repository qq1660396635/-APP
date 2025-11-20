python3 - <<'EOF'
import os,sys,pathlib,time,requests,re
from docx import Document

# ==================== 配置区（只改这里） ====================
API_KEY = "sk-哥们你自己🔑🔑🔑🔑"
MODEL   = "kimi-k2-turbo-preview"
ROOT    = pathlib.Path("/storage/emulated/0/Download/OnePlus Share/GITHUB 开源项目/3. ESP32-小智/副本/章节")
TOTAL   = 30
# ===========================================================

DOCX_PATH = pathlib.Path("/storage/emulated/0/Download/OnePlus Share/GITHUB 开源项目/3. ESP32-小智/副本/（合并）g南堂  小说架构（10.2）.docx")
if not DOCX_PATH.exists():
    sys.exit("原始.docx 不存在，请检查路径")

ROOT.mkdir(parents=True, exist_ok=True)
WORLD_TEXT = "\n".join(p.text for p in Document(DOCX_PATH).paragraphs if p.text.strip())

BIBLE = f"""
{WORLD_TEXT}

【补充强制意象】
糖=承诺，琴=家书，纸鸢=归否，桃花=凉安，空锅=执念。
每章必须出现至少1个意象，并翻转其原义。

【反派三级】
①袁潾（门阀） ②赫连曜（流民帅） ③乱世本身

【强制转折表】
1.南风渡夜逃→上巳游园（清谈斗诗）
2.游园→绛台朱门拒入（门阀嘲白衣）
3.绛台→纸鸢盟（城墙双线立誓）
4.纸鸢→流民帅夜袭（火乌鸦第一次）
5.夜袭→镜湖软禁（袁氏做局）
6.镜湖→雪夜断指（凉安断指换她命）
7.断指→南风渡立旗（南棠自封渡主）
"""

TURN_LIST = [l.strip() for l in """
南风渡夜逃→上巳游园（清谈斗诗）
游园→绛台朱门拒入（门阀嘲白衣）
绛台→纸鸢盟（城墙双线立誓）
纸鸢→流民帅夜袭（火乌鸦第一次）
夜袭→镜湖软禁（袁氏做局）
镜湖→雪夜断指（凉安断指换她命）
断指→南风渡立旗（南棠自封渡主）
""".strip().splitlines() if l.strip()]

memory_file = ROOT / "memory.txt"
written     = sorted(ROOT.glob("ch*.txt"), key=lambda x: int(x.stem[2:]))
next_ch     = len(written) + 1
memory      = "\n".join(ch.read_text(encoding='utf-8') for ch in written)

url = "https://api.moonshot.cn/v1/chat/completions"
hdr = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

def chat(prompt: str) -> str:
    for i in range(1, 8):
        try:
            r = requests.post(url, headers=hdr,
                              json={"model": MODEL, "messages": [{"role": "user", "content": prompt}],
                                    "temperature": 0.32}, timeout=300)     # ← 只改这里：120→300
            if r.status_code == 429: time.sleep(2 ** i); continue
            r.raise_for_status()
            return r.json()["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"[ERR] {e}"); time.sleep(2)
    raise RuntimeError("重试失败")

if next_ch > TOTAL:
    print("[*] 卷一已完成"); exit(0)

for ch in range(next_ch, TOTAL + 1):
    turn = TURN_LIST[(ch - 1) // 5] if (ch - 1) // 5 < len(TURN_LIST) else "自由推进"
    temp = "45→60→70→30℃".split("→")[(ch - 1) // 10]

    print(f"[INFO] 正在生成 ch{ch:02d} ...")
    title = chat(f"{BIBLE}\n{memory[-1200:]}\n请起第{ch}章标题（≤12字），仅返回标题。").strip()
    title = re.sub(r"[\"\"''。,，!?？！]", "", title)
    print(f"[INFO] 标题：{title}")

    # ↓↓↓ 只改这里：prompt 加长 + 明确字数/token 上限 ↓↓↓
    body = chat(f"{BIBLE}\n前文摘要：{memory[-1200:]}\n强制转折：{turn}\n感情温度：{temp}\n标题：{title}\n"
                f"要求：\n"
                f"1. 本章《{title}》正文 2200-2600 字；\n"
                f"2. 五个意象“糖/琴/纸鸢/桃花/空锅”只能各出现一次，且必须翻转其原义；\n"
                f"3. 战争描写≤15%，禁用“雪夜断指”做任何标题或情节复用；\n"
                f"4. 结尾留半句，标题必须全新，不得与前面任何章节重复；\n"
                f"5. 禁止自我重复、禁止大段排比、禁止解释性旁白。")
    print(f"[INFO] 返回字数：{len(body)}")

    f = ROOT / f"ch{ch:02d}.txt"
    f.write_text(f"第{ch}章　{title}\n\n{body.strip()}", encoding='utf-8')
    memory += f"\n\n{body.strip()}"
    with memory_file.open("a", encoding='utf-8') as m:
        m.write(f"\n\n{body.strip()}")

    kw = re.findall(r"糖|琴|纸鸢|桃花|空锅", body)
    print(f"[OK] ch{ch:02d}《{title}》{len(body)}字  意象:{kw}")

# 合并终稿
all_txt = "\n".join(ch.read_text(encoding='utf-8') for ch in sorted(ROOT.glob("ch*.txt"), key=lambda x: int(x.stem[2:])))
(ROOT / "VOL1_final.txt").write_text(all_txt, encoding='utf-8')
print("[ALL DONE] 总卷 → ", ROOT / "VOL1_final.txt")
EOF
