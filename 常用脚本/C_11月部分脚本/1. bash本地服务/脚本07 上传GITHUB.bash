#!/bin/bash

# =========================================================
# 错误处理和调试配置
# =========================================================

# 开启 e 选项：遇到非零退出状态（即致命错误）时立即退出脚本
set -e
# 开启 u 选项：使用未定义的变量时视为错误
set -u
# 开启 o pipefail 选项：管道中任何命令失败，整个管道即失败
set -o pipefail

# 错误处理函数：在任何命令失败时被调用
error_handler() {
    local exit_code="$?"
    local line_num="$1"

    if [ "$exit_code" -ne 0 ]; then
        echo -e "\n🛑 **致命错误 (FATAL ERROR)**"
        echo "-------------------------------------"
        echo "错误代码 (Exit Code): **$exit_code**"
        echo "错误行号 (Error Line): **$line_num**"
        echo "最后执行的命令 (Last Command): **$BASH_COMMAND**"
        echo "-------------------------------------"
        echo "请根据错误行号，检查上方命令的输出，确定问题所在（例如权限、网络或文件路径）"
    fi
    exit "$exit_code"
}

# 设置 trap：当发生 ERR (错误) 信号时，调用 error_handler 函数
trap 'error_handler $LINENO' ERR

# =========================================================
# 配置区（自己改）
# =========================================================
USER="qq1660396635"
REPO="-APP"
# 确保这个路径是正确的，并且在 Termux 中可以访问
SRC_DIR="/storage/emulated/0/Download/OnePlus Share/03 - 个人测试/常用工具转安卓" 

# =========================================================
# 业务区
# =========================================================

echo "--- 脚本开始执行 ---"

# 切换到源目录。如果目录不存在，脚本会在这里失败并报错。
echo "正在切换目录到: $SRC_DIR"
cd "$SRC_DIR"

# 接收 GitHub Token
read -rp "粘贴 GitHub Token 后回车: " TOKEN
echo

# 1. 初始化 Git 仓库 (如果需要)
[ ! -d .git ] && git init -q
echo "Git 仓库状态检查完成。"

# 2. 允许非标准目录（Termux 环境中可能需要）
# 2>/dev/null || true 确保即使失败也不会中断脚本
git config --global --add safe.directory "$SRC_DIR" 2>/dev/null || true
echo "Git safe directory 配置完成。"

# 3. 配置远程仓库 URL (使用 TOKEN 进行身份验证)
REMOTE_URL="https://${USER}:${TOKEN}@github.com/${USER}/${REPO}.git"
echo "正在配置远程仓库 URL..."
# 尝试设置 URL，如果不存在则添加。如果失败，可能是权限问题。
git remote set-url origin "$REMOTE_URL" 2>/dev/null || \
  git remote add origin "$REMOTE_URL"

# 4. 拉取远程更新
echo "正在尝试拉取远程更新..."
# 尝试拉取 main 或 master 分支的最新代码，以解决合并冲突。
git pull origin main || git pull origin master || echo "警告：未能拉取远程代码，可能是新仓库。"

# 5. 添加并提交文件
echo "正在添加并提交文件..."
git add .
git commit -qm "update $(date +%m%d-%H%M)"

# 6. 推送到临时分支（关键修改：移除 --force）
# 使用秒级时间戳分支名，绕开 ruleset
TMP_BRANCH="tmp-$(date +%s)"
echo "正在推送到临时分支: $TMP_BRANCH (非强制推送)"

# 这一行是您之前失败的地方。如果再次失败，错误捕获将打印行号。
git push origin HEAD:"$TMP_BRANCH"

# 清除错误捕获，因为我们已经成功退出
trap - ERR

echo ===== 上传完成 =====
echo "去 GitHub 页面合并 $TMP_BRANCH 到 main 即可"
