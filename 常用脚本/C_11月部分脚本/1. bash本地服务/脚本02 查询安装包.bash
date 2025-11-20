#!/bin/bash
# ---------- 可改区域 ----------
CHECK_LIST=(
  android-sdk-build-tools
  openjdk-17
  aapt
  apksigner
  dx
  ecj
)
# ---------- 下面别动 ----------
for name in "${CHECK_LIST[@]}"; do
  # 1. 先问 dpkg
  if dpkg -l | awk '$2==pkg && $1=="ii"{print $3}' pkg="$name" | grep -q .; then
    echo "✅ $name: 官方包 $(dpkg -l | awk '$2==pkg && $1=="ii"{print $3}' pkg="$name")"
    continue
  fi

  # 2. dpkg 没有就扫描 PATH 和常见手动目录
  found="" path_list=""
  # 把可能放手动文件的目录全列出来，想加目录继续往数组里写
  MANUAL_DIR=(
    "$PREFIX/bin"
    "$PREFIX/share"
    "$PREFIX/opt"
    /system/bin
    /system/xbin
  )
  for dir in "${MANUAL_DIR[@]}"; do
    # 精确名字匹配（文件或软链）
    if [[ -e "$dir/$name"      ||
          -e "$dir/${name}.jar" ||
          -e "$dir/${name}.sh"  ]]; then
      found="yes"
      path_list="$path_list$dir/$name "
    fi
  done

  # 3. 也在 PATH 里再扫一次，防止漏掉
  if command -v "$name" >/dev/null 2>&1; then
    real_path=$(command -v "$name")
    found="yes"
    path_list="$path_list$real_path "
  fi

  # 4. 输出结果
  if [[ $found == "yes" ]]; then
    # 去重并打印
    printf "✅ %s: 手动安装，路径：" "$name"
    printf "%s " $(printf "%s" "$path_list" | tr ' ' '\n' | sort -u)
    echo
  else
    echo "❌ $name: 未安装"
  fi
done
