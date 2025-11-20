# 备份 .bashrc
cp ~/.bashrc ~/.bashrc.bak

# 1. 在 .bashrc 末尾追加（没有就加，有了就不重复）
grep -qxF 'source $PREFIX/2025/func.sh' ~/.bashrc || echo 'source $PREFIX/2025/func.sh' >> ~/.bashrc

# 2. 生成/更新函数文件
mkdir -p $PREFIX/2025
cat > $PREFIX/2025/func.sh <<'EOF'
#!/data/data/com.termux/files/usr/bin/bash

# se 函数：切换到目录并运行 server.py
se(){
  read -erp "请输入目录: " dir
  [[ -d $dir ]] || { echo "目录不存在: $dir"; return 1; }
  cd "$dir" || return
  [[ -f server.py ]] && python server.py || echo "未找到 server.py"
}

# py 函数：运行指定的Python文件
py(){
  read -erp "请输入Python文件路径: " pyfile
  [[ -f "$pyfile" ]] || { echo "文件不存在: $pyfile"; return 1; }
  python "$pyfile"
}
EOF

# 3. 赋权 & 立即生效
chmod +x $PREFIX/2025/func.sh
source ~/.bashrc





二    下面是常用bashrc配置
~ $ cat ~/.bashrc
# 最优先：Gradle 7.6（必须放在最前面）
export PATH=$HOME/gradle-7.6/bin:$PATH
# Android SDK
export ANDROID_HOME=$HOME/android-sdk
export PATH=$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/platform-tools:$PATH
# 你的原有配置保持不变
$PREFIX/2025/start
$PREFIX/2025/leetcode.sh
alias s='source ~/.bashrc'
source $PREFIX/2025/func.sh
~ $
