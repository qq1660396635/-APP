# 单文件 ，先ctags,jq分析 ，   再  文件＋ctags＋提示词分析
# 粘贴termux直接运行,  .py格式为了便于阅读
python3 - <<'EOF'
import os, subprocess, pathlib, requests, time, sys
from requests.exceptions import HTTPError

API_KEY = 'sk-哥们儿，别薅羊毛了。我也没钱🔑🔑🔑'
MODEL   = 'kimi-k2-turbo-preview'
SRC     = pathlib.Path('/storage/emulated/0/Download/OnePlus Share/GITHUB 开源项目/3. ESP32-小智/副本/xiaozhi-esp32-main/main/application.cc')
OUT_DIR = pathlib.Path('/storage/emulated/0/Download/OnePlus Share/GITHUB 开源项目/3. ESP32-小智/副本/xiaozhi-esp32-main/项目分析报告')

OUT_DIR.mkdir(parents=True, exist_ok=True)
TAGS_FILE = OUT_DIR / f'{SRC.stem}.cc_ctags.txt'
BRAIN_FILE= OUT_DIR / f'{SRC.stem}.cc_脑图.txt'

mode = 'c' if SRC.suffix == '.c' else 'cpp'
# 1. 完整 ctags + jq + awk 管道（含 macro）
cmd = f'''
ctags --output-format=json --kinds-c++=+c+d+e+f+g+l+m+n+p+s+t+u+v+x "{SRC}" 2>/dev/null |
jq -r \'select((.kind=="function" or .kind=="member" or .kind=="macro" or .kind=="struct" or .kind=="typedef" or .kind=="variable") and (.name|startswith("__anon")|not))
        | . as $$r
        | if   $$r.kind=="macro"    then "MACRO\\t\\($$r.name)"
          elif $$r.kind=="function" then "FUNC\\t\\($$r.name)\\t\\($$r.scope//"-")"
          elif $$r.kind=="member"   then "MEMBER\\t\\($$r.name)\\t\\($$r.scope)"
          elif $$r.kind=="struct"   then "STRUCT\\t\\($$r.name)"
          elif $$r.kind=="typedef"  then "TYPEDEF\\t\\($$r.name)"
          elif $$r.kind=="variable" then "VAR\\t\\($$r.name)"
          else empty end\' |
awk -v mode="{mode}" \'
BEGIN{{print "[宏定义]"}}
$1=="MACRO"   {{printf "  %-30s （宏）\\n",$2; next}}
$1=="STRUCT"  {{if(!s_h){{print "\\n[结构体]";s_h=1}} printf "  %-30s （结构体）\\n",$2; next}}
$1=="TYPEDEF" {{if(!t_h){{print "\\n[类型别名]";t_h=1}} printf "  %-30s （类型别名）\\n",$2; next}}
$1=="VAR"     {{if(!v_h){{print "\\n[变量]";v_h=1}} printf "  %-30s （变量）\\n",$2; next}}
mode=="c" && $1=="FUNC" {{if(!f_h){{print "\\n[函数]";f_h=1}} printf "  %-30s （函数）\\n",$2; next}}
mode=="cpp" && $1=="FUNC" {{
    cls=$3; if(cls=="-"){{if(!g_h){{print "\\n[全局函数]";g_h=1}} printf "  %-30s （函数）\\n",$2; next}}
    else{{if(!(cls in done)){{printf "\\n[类 %s]\\n",cls; done[cls]=1}} printf "  %-30s （成员函数）\\n",$2; next}}
}}
mode=="cpp" && $1=="MEMBER" {{
    cls=$3; if(!(cls in done)){{printf "\\n[类 %s]\\n",cls; done[cls]=1}} printf "  %-30s （成员变量）\\n",$2; next}}
\'
'''
symbols = subprocess.check_output(cmd, shell=True, text=True)
TAGS_FILE.write_text(symbols, encoding='utf-8')
print('[OK] 符号 →', TAGS_FILE)

code = SRC.read_text(encoding='utf-8', errors='ignore')

def chat(msgs):
    attempt = 0
    while True:
        try:
            r = requests.post(
                'https://api.moonshot.cn/v1/chat/completions',
                headers={'Authorization': f'Bearer {API_KEY}', 'Content-Type': 'application/json'},
                json={'model': MODEL, 'messages': msgs, 'temperature': 0.1},
                timeout=90)
            r.raise_for_status()
            return r.json()['choices'][0]['message']['content']
        except HTTPError as e:
            if e.response.status_code == 429:
                attempt += 1
                wait = 2 ** attempt
                print(f'\n！429限速，{wait}s后重试(第{attempt}次)', file=sys.stderr)
                time.sleep(wait)
                continue
            raise

prompt = f"""下方给出两份材料：
1. ctags 抓取的符号清单（已去重）；
2. 完整 C/C++ 源码。

请以符号清单为基准，对照源码，按下面 3 点返回中文说明（英文标识符保留，括号内中文）：
1. 每个引入头文件的作用；
2. 所有自定义常量/宏；
3. 成员（含类型/函数/回调/变量）。

格式示例（必须严格照此输出，不要多一行解释）：
【头文件】
freertos/FreeRTOS.h（FreeRTOS主要头文件）

【宏常量】
TAG → "APP"（日志标签）

【类】
class Application（应用主类）：
- void start()（启动函数）
- static QueueHandle_t msgq（消息队列句柄）

符号清单（{symbols.count(chr(10))} 行）：
{symbols}

源码：
{code}"""

BRAIN_FILE.write_text(chat([{'role': 'user', 'content': prompt}]), encoding='utf-8')
print('[OK] 脑图 →', BRAIN_FILE)
EOF
