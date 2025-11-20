#!/bin/bash
# Termux环境下Python库检查和安装脚本
# 用于检查和安装Word文档处理相关的Python库

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查命令是否存在
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# 检查Python包是否安装
check_python_package() {
    local package=$1
    python -c "import ${package}" 2>/dev/null
    return $?
}

# 安装Termux包
install_termux_package() {
    local package=$1
    log_info "安装Termux包: $package"
    if pkg install "$package" -y; then
        log_success "Termux包 $package 安装成功"
        return 0
    else
        log_error "Termux包 $package 安装失败"
        return 1
    fi
}

# 安装Python包
install_python_package() {
    local package=$1
    local display_name=${2:-$package}
    
    log_info "安装Python包: $display_name"
    
    # 首先尝试普通安装
    if pip install "$package" --quiet; then
        log_success "Python包 $display_name 安装成功"
        return 0
    else
        log_warning "普通安装失败，尝试使用--user参数安装"
        # 尝试用户模式安装
        if pip install --user "$package" --quiet; then
            log_success "Python包 $display_name 用户模式安装成功"
            return 0
        else
            log_error "Python包 $display_name 安装失败"
            return 1
        fi
    fi
}

# 主函数
main() {
    echo "========================================"
    echo "  Termux Python库检查和安装脚本"
    echo "  用于Word文档处理相关库"
    echo "========================================"
    echo

    # 1. 更新Termux包管理器
    log_info "更新Termux包管理器..."
    if pkg update -y && pkg upgrade -y; then
        log_success "Termux包管理器更新成功"
    else
        log_error "Termux包管理器更新失败"
        exit 1
    fi
    echo

    # 2. 检查并安装基础系统依赖
    log_info "检查系统依赖..."
    system_packages=("python" "python-pip" "libxml2" "libxslt" "zlib" "clang")
    
    for pkg in "${system_packages[@]}"; do
        if ! pkg list-installed | grep -q "^$pkg/"; then
            log_warning "$pkg 未安装，正在安装..."
            install_termux_package "$pkg" || exit 1
        else
            log_success "$pkg 已安装"
        fi
    done
    echo

    # 3. 检查Python环境
    log_info "检查Python环境..."
    if command_exists python; then
        python_version=$(python --version 2>&1)
        log_success "Python已安装: $python_version"
    else
        log_error "Python未安装"
        exit 1
    fi

    if command_exists pip; then
        pip_version=$(pip --version)
        log_success "pip已安装: $pip_version"
    else
        log_error "pip未安装"
        exit 1
    fi
    echo

    # 4. 更新pip
    log_info "更新pip到最新版本..."
    if pip install --upgrade pip --quiet; then
        log_success "pip更新成功"
    else
        log_warning "pip更新失败，继续使用当前版本"
    fi
    echo

    # 5. 检查并安装Python库
    log_info "检查Python库..."
    
    # 定义需要安装的库
    declare -A python_packages=(
        ["lxml"]="lxml"
        ["python-docx"]="python-docx"
        ["docxcompose"]="docxcompose"
    )
    
    for import_name in "${!python_packages[@]}"; do
        package_name="${python_packages[$import_name]}"
        
        if check_python_package "$import_name"; then
            log_success "$package_name 已安装"
        else
            log_warning "$package_name 未安装，正在安装..."
            install_python_package "$package_name" "$package_name" || exit 1
        fi
    done
    echo

    # 6. 验证安装
    log_info "验证安装..."
    python3 -c "
import sys
try:
    import os
    import re
    from docx import Document
    from docxcompose.composer import Composer
    from docx.shared import Pt
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement
    print('✅ 所有库导入成功！')
    print('✅ Word文档处理环境配置完成')
except ImportError as e:
    print(f'❌ 导入失败: {e}')
    sys.exit(1)
"
    
    if [ $? -eq 0 ]; then
        echo
        log_success "所有库安装验证成功！"
        echo
        echo "========================================"
        echo "  安装完成！现在可以使用Word处理功能了"
        echo "========================================"
    else
        log_error "验证失败，请检查错误信息"
        exit 1
    fi
}

# 运行主函数
main "$@"
