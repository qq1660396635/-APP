#!/bin/bash
# 〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓
#  凉安 H5 游戏站 一键“去远程化”脚本
#  作用：把 CDN/远程/上级相对路径 全部改成本地相对路径，解决 ERR_CONNECTION_REFUSED
#  用法：bash fix_local.sh
# 〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓

########### ① 用户配置区（下次换目录/换文件，只改这里即可） ###########
ROOT_DIR="/storage/emulated/0/Download/OnePlus Share/2025.淘宝80个_H5游戏 源码"  # 游戏根目录
JS_DIR="./js"                       # 本地 JS 放置位置（相对于网页）
CSS_DIR="./css"                     # 本地 CSS 放置位置
IMG_DIR="./images"                  # 本地图片放置位置
GAME_DIR="./yxmb"                   # 本地小游戏目录
###########################################################################

########### ② 函数：打印带序号步骤 #######################################
step=0
log(){
  step=$((step+1))
  printf "\n[%02d] %s\n" "$step" "$1"
}
###########################################################################

log "开始扫描 *.html …"
find "$ROOT_DIR" -type f -name "*.html" | while read -r file; do
  echo "  处理：${file##*/}"

  # ③ 把常见 CDN 远程域名全部截断，改成本地目录
  sed -i -E 's|https://cdn\.jsdelivr\.net/npm/[^"]*|'${JS_DIR}/jquery.min.js'|g' "$file"
  sed -i -E 's|https://stackpath\.bootstrapcdn\.com/[^"]*|'${CSS_DIR}/bootstrap.min.css'|g' "$file"
  sed -i -E 's|https://code\.jquery\.com/[^"]*|'${JS_DIR}/jquery.min.js'|g' "$file"

  # ④ 通用远程 src/href 截断（保留文件名，目录指向本地）
  sed -i -E 's|src="https://[^"]*/([^/]*\.js)"|src="'${JS_DIR}'/\1"|g' "$file"
  sed -i -E 's|href="https://[^"]*/([^/]*\.css)"|href="'${CSS_DIR}'/\1"|g' "$file"
  sed -i -E 's|src="https://[^"]*/([^/]*\.(png|jpg|gif|svg))"|src="'${IMG_DIR}'/\1"|g' "$file"

  # ⑤ 把 ../ 上级相对路径改成当前目录 ./ （兼容 iframe 与普通链接）
  sed -i 's|href="../yxmb/|href="'${GAME_DIR}'/|g' "$file"
  sed -i 's|src="../images/|src="'${IMG_DIR}'/|g' "$file"
  sed -i 's|src="../js/|src="'${JS_DIR}'/|g' "$file"
  sed -i 's|href="../css/|href="'${CSS_DIR}'/|g' "$file"

  # ⑥ 修复 iframe 动态拼接路径：yxmb/${gameId}/ → ./yxmb/${gameId}/index.html
  sed -i "s|attr('src', *'\`yxmb/\${gameId}/\`')|attr('src', \`'${GAME_DIR}/\${gameId}/index.html'\`)|g" "$file"
  # 也照顾双引号版本
  sed -i "s|attr(\"src\", *\"\`yxmb/\${gameId}/\`\")|attr(\"src\", \`${GAME_DIR}/\${gameId}/index.html\`)|g" "$file"

done

log "全部替换完成！现在可直接双击 index.html 离线运行。"