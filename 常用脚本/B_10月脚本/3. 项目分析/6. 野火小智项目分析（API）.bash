下面这段 直接复制进 Termux 回车即可跑：
1. 一次性扫描
 /storage/emulated/0/Download/OnePlus Share/GITHUB 开源项目/项目01/野火小智文档/ 
下 所有 项目文件夹（不管编号是多少）：
 
如果目录里有  Core  → 扫  Core 
 
如果目录里有  User  → 扫  User 
 
如果目录里有  APP  → 扫  APP 

2. 每个项目生成一份 独立报告，文件名就是 项目文件夹名字.txt，统一放到：
 /storage/emulated/0/Download/OnePlus Share/GITHUB 开源项目/项目01/野火小智文档/项目分析报告/ 
 
3. 路径只保留最后三级，报告格式和你刚才 最满意的那版完全一致。

# 一次性复制即可
BASE="/storage/emulated/0/Download/OnePlus Share/GITHUB 开源项目/项目01/野火小智文档"
OUT_DIR="$BASE/项目分析报告"
mkdir -p "$OUT_DIR"

# 遍历所有项目文件夹
find "$BASE" -maxdepth 1 -type d ! -path "$BASE" | while read -r proj; do
  proj_name=$(basename "$proj")
  report_file="$OUT_DIR/${proj_name}.txt"

  # 决定到底扫哪个子目录
  if   [ -d "$proj/Core" ]; then SCAN_DIR="$proj/Core"
  elif [ -d "$proj/User" ]; then SCAN_DIR="$proj/User"
  elif [ -d "$proj/APP"  ]; then SCAN_DIR="$proj/APP"
  else continue; fi

  # 写报告头
  {
    echo "文件分析报告"
    echo "生成时间: $(date)"
    echo "========================================================="
    echo ""
  } > "$report_file"

  # 逐个文件分析
  find "$SCAN_DIR" -type f \( -name '*.c' -o -name '*.h' \) | sort -V | nl -w1 -s'. ' | while read -r idx f; do
    short=$(echo "$f" | sed -E 's|.*(/[^/]+/[^/]+/[^/]+/[^/]+)$|\1|')
    {
      echo ""
      echo "🟢 $idx $(basename "$f")"
      echo "🔻🔻🔻🔻🔻🔻🔻"
      echo "📁 $short"
      echo "┌────────────────────────────────────────────────────────────┐"
      echo "│                    文件分析                               │"
      echo "├────────────────────────────────────────────────────────────┤"
      echo "│ 文件: $short"
      echo "├────────────────────────────────────────────────────────────┤"

      ctags --output-format=json --fields=+KnzSst --kinds-c=+cdefglmnpstuvxL --extras=+qF "$f" 2>/dev/null |
      jq -r 'select(.name|startswith("__anon")|not) | (.kind+"\t"+.name+"\t"+(.scope//"-")+"\t"+(.line|tostring)+"\t"+(.static//"no"))' |
      awk '
      $1=="prototype" {prototypes[++pcount] = $0; next}
      $1=="function" && $3=="-" {functions[++fcount] = $0; next}
      $1=="macro"   {macros[++mcount] = $0; next}
      $1=="struct"  {structs[++scount] = $0; next}
      $1=="union"   {unions[++ucount] = $0; next}
      $1=="enum"    {enums[++ecount] = $0; next}
      $1=="enumerator"{enumerators[++evcount] = $0; next}
      $1=="typedef" {typedefs[++tcount] = $0; next}
      $1=="variable"&&$5=="yes"&&$3=="-"{static_globals[++sgcount] = $0; next}
      $1=="variable"&&$5=="no"&&$3=="-" {globals[++gcount] = $0; next}
      $1=="local"   {locals[++lcount] = $0; next}
      END{
        if (pcount > 0) {
          print "│"; print "│ [函数原型]"
          for (i=1; i<=pcount; i++) {split(prototypes[i], parts, "\t"); printf "│   %-40s (原型)\n", parts[2]}
        }
        if (fcount > 0) {
          print "│"; print "│ [全局函数]"
          for (i=1; i<=fcount; i++) {split(functions[i], parts, "\t"); printf "│   %-40s (函数)\n", parts[2]}
        }
        if (mcount > 0) {
          print "│"; print "│ [宏定义]"
          for (i=1; i<=mcount; i++) {split(macros[i], parts, "\t"); printf "│   %-40s (宏)\n", parts[2]}
        }
        if (scount > 0) {
          print "│"; print "│ [结构体]"
          for (i=1; i<=scount; i++) {split(structs[i], parts, "\t"); printf "│   %-40s (结构体)\n", parts[2]}
        }
        if (ucount > 0) {
          print "│"; print "│ [联合体]"
          for (i=1; i<=ucount; i++) {split(unions[i], parts, "\t"); printf "│   %-40s (联合体)\n", parts[2]}
        }
        if (ecount > 0) {
          print "│"; print "│ [枚举类型]"
          for (i=1; i<=ecount; i++) {split(enums[i], parts, "\t"); printf "│   %-40s (枚举)\n", parts[2]}
        }
        if (evcount > 0) {
          print "│"; print "│ [枚举值]"
          for (i=1; i<=evcount; i++) {split(enumerators[i], parts, "\t"); printf "│   %-40s (枚举值)\n", parts[2]}
        }
        if (tcount > 0) {
          print "│"; print "│ [类型定义]"
          for (i=1; i<=tcount; i++) {split(typedefs[i], parts, "\t"); printf "│   %-40s (typedef)\n", parts[2]}
        }
        if (sgcount > 0) {
          print "│"; print "│ [静态全局变量]"
          for (i=1; i<=sgcount; i++) {split(static_globals[i], parts, "\t"); printf "│   %-40s (static 全局)\n", parts[2]}
        }
        if (gcount > 0) {
          print "│"; print "│ [全局变量]"
          for (i=1; i<=gcount; i++) {split(globals[i], parts, "\t"); printf "│   %-40s (全局)\n", parts[2]}
        }
        if (lcount > 0) {
          print "│"; print "│ [局部变量]"
          for (i=1; i<=lcount; i++) {split(locals[i], parts, "\t"); printf "│   %-40s (局部，位于: %s)\n", parts[2], parts[3]}
        }
        print "└────────────────────────────────────────────────────────────┘"
        print ""
        print "========================================================="
      }'
    } >> "$report_file"
  done
done

echo "全部完成！报告已集中放到：$OUT_DIR"
