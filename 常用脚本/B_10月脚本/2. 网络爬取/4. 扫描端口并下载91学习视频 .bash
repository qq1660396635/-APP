#!/data/data/com.termux/files/usr/bin/bash
# -*- coding: utf-8 -*-
# 87000 固定，87100-87200 随到随下
# 单线程 + 极简提示 + 跳过 >500 MB 文件

BASE_URL="https://视频地址🔗🔗🔗/87000"
START_ID=87100
END_ID=87200
SAVE_ROOT="/storage/emulated/0/Download/OnePlus Share/GITHUB 开源项目/项目01/脚本/02 不可描述"
UA="Mozilla/5.0 (Linux; Android 13; SM-G973F) AppleWebKit/537.36"

mkdir -p "$SAVE_ROOT"

#---- 1-2 秒快速估算大小 ----
get_size_mb(){
  local m3u8="$1"
  seg=$(curl -sL -H "User-Agent: $UA" "$m3u8" | sed -n '/^[^#]/p' | head -1)
  [ -z "$seg" ] && { echo 0; return; }
  seg_url=$(dirname "$m3u8")/$seg

  # 拿 bitrate，失败就给 1 Mbps
  br=$(curl -sL -r 0-1023 -H "User-Agent: $UA" "$seg_url" \
       | ffprobe -v error -show_entries format=bit_rate -of csv=p=0 - 2>/dev/null)
  case "$br" in ''|*[!0-9]*) br=1000000 ;; esac

  # 拿总时长，失败给 0
  dur=$(curl -sL -H "User-Agent: $UA" "$m3u8" \
        | awk -F: '/^#EXTINF:/{s+=$2} END{printf "%.0f",s}')
  [ -z "$dur" ] && dur=0

  echo $(( br * dur / 8 / 1024 / 1024 ))
}

for id in $(seq "$START_ID" "$END_ID"); do
  m3u8_url="$BASE_URL/$id/index.m3u8"

  curl -s -r 0-1023 -L --max-time 5 -H "User-Agent: $UA" "$m3u8_url" | grep -q "^#EXTM3U" || {
    echo "[跳过] $id  无法获取 m3u8"; continue
  }

  folder_start=$((START_ID + ((id - START_ID) / 20) * 20))
  folder="$SAVE_ROOT/${folder_start}-$((folder_start+19))"
  mkdir -p "$folder"
  out="$folder/$id.mp4"
  [ -f "$out" ] && { echo "[存在] $id.mp4"; continue; }

  echo "[探测] $id  估算大小中..."
  size_mb=$(get_size_mb "$m3u8_url")
  [ "$size_mb" -gt 500 ] && {
    echo "[跳过] $id  估算 ${size_mb}MB (>500MB)"; continue
  }

  echo "[下载] $id  估算 ${size_mb}MB → $out"
  ffmpeg -hide_banner -loglevel error -nostats -nostdin -y \
    -user_agent "$UA" -i "$m3u8_url" -c copy "$out" && \
    echo "[完成] $id.mp4" || echo "[失败] $id.mp4"
done

echo ">>> 全部结束！"
