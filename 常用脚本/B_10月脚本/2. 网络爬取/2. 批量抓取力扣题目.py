     Mr.L  需求「一次复制，两行直接跑」的脚本：   termux的bash脚本 
1.   先抓 全部 1000 题 的题干（英文纯文本）
2.   按 每 50 题切一个文件（共 20 个文件）
3.   文件名自动编号： leetcode_001_050.json  …  leetcode_951_1000.json 
4.   目录若不存在会自动建，跑完打印 ✅ 列表。   


python3 -x <<'PYEOF'
import json, urllib.request, pathlib, re, html

root = "/storage/emulated/0/Download/OnePlus Share/GITHUB 开源项目/项目01/leetcode_split"
pathlib.Path(root).mkdir(parents=True, exist_ok=True)

# ① 按 ID 升序拿前 1000 题
list_url = "https://leetcode.com/api/problems/all/"
req = urllib.request.Request(list_url, headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})
with urllib.request.urlopen(req) as resp:
    pairs = sorted(
        [(q["stat"]["frontend_question_id"], q["stat"]["question__title_slug"])
         for q in json.loads(resp.read().decode())["stat_status_pairs"]],
        key=lambda x: x[0])[:1000]

# ② GraphQL 模板
query = """
query questionData($titleSlug: String!) {
  question(titleSlug: $titleSlug) { content difficulty }
}"""

def fetch(qid, slug):
    payload = json.dumps({
        "operationName": "questionData",
        "query": query,
        "variables": {"titleSlug": slug}
    }).encode()
    greq = urllib.request.Request(
        "https://leetcode.com/graphql",
        data=payload,
        headers={"Content-Type": "application/json",
                 "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})
    with urllib.request.urlopen(greq) as r:
        d = json.loads(r.read().decode())["data"]["question"]
    text = html.unescape(re.sub(r'<[^>]+>', '', d["content"])) if d["content"] else ""
    return {"id": qid, "slug": slug, "difficulty": d["difficulty"], "content": text.strip()}

# ③ 每 50 题写一文件（存在就跳过）
batch = 50
for i in range(0, 1000, batch):
    file = pathlib.Path(root) / f"leetcode_{i+1:03d}_{min(i+batch, 1000):03d}.json"
    if file.exists():
        print(f"⏭ 跳过 {file}")
        continue
    chunk = [fetch(qid, slug) for qid, slug in pairs[i:i+batch]]
    with open(file, "w", encoding="utf-8") as f:
        json.dump(chunk, f, ensure_ascii=False, indent=2)
    print(f"✅ 已写入 {file}  （ID {chunk[0]['id']} ~ {chunk[-1]['id']}）")

print("全部完成！")
PYEOF
