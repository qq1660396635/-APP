#!/data/data/com.termux/files/usr/bin/bash
# ========== 轻量公共端口扫描 ==========

# 0) 目标变量——只改这里即可
TARGET=你要扫描的网站.com

# 1) 默认目标
HOST=${1:-$TARGET}

# 2) 端口列表 + 中文说明（按端口从小到大展示）
declare -A MAP=(
  [22]="SSH-远程登录"
  [80]="HTTP-网站"
  [443]="HTTPS-加密网站"
  [3306]="MySQL-数据库"
  [5432]="PostgreSQL-数据库"
  [6379]="Redis-缓存"
  [8080]="HTTP-备用网站"
  [8443]="HTTPS-备用加密网站"
  [3389]="RDP-Windows远程桌面"
  [9200]="Elasticsearch-搜索"
)

# 3) 表头
printf "\n=== 轻触 %s ===\n" "$HOST"
printf "%-7s %-7s %-25s %s\n" "端口" "服务说明" "状态"

# 4) 顺序探测（单线程，0.3 s 超时，不乱序）
for PORT in $(printf '%s\n' "${!MAP[@]}" | sort -n); do
  if timeout 0.3 bash -c ">/dev/tcp/$HOST/$PORT" 2>/dev/null; then
    printf "%-7d %-25s %s\n" "$PORT" "${MAP[$PORT]}" "✅ 开放"
  else
    printf "%-7d %-25s %s\n" "$PORT" "${MAP[$PORT]}" "❌ 关闭"
  fi
done

# 5) 结束
printf "=== 扫描完成 ===\n\n"
