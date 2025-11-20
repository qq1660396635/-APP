 # 判断视频是否失效，，，或者扫描端口下的资源。
base="https:视频链接"
outdir="/storage/emulated/0/Download/OnePlus Share"
outfile="$outdir/scan_result.txt"
mkdir -p "$outdir"; >"$outfile"

for ((i=87000;i<=87200;i++)); do
  url="$base/$i/index.m3u8"
  # 发 GET，只拉 1k 字节，带跳转
  resp=$(curl -s -r 0-1023 -L --max-time 5 "$url")
  # 简单判断：返回里出现 #EXTM3U 就说明是合法 m3u8
  if grep -q "^#EXTM3U" <<<"$resp"; then
    echo "[OK]  $url" | tee -a "$outfile"
  else
    echo "[404] $url" >> "$outfile"
  fi
done
echo "扫描完成，结果已保存到：$outfile"