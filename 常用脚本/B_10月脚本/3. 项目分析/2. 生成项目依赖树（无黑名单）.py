#!/usr/bin/env bash # 指定用 bash 解释器      Mr.L bah脚本 ，.py只是为了阅读
#!/usr/bin/env bash # 指定用 bash 解释器
# ===================== 配置区 =====================
PROJECT_ROOT="/storage/emulated/0/Download/OnePlus Share/GITHUB 开源项目/3. ESP32-小智/副本/xiaozhi-esp32-main" # 项目根目录
IDF_ROOT="/storage/emulated/0/Download/OnePlus Share/ESP-IDF源码/esp-idf-v5.5.1" # ESP-IDF 根目录
ENTRY_FILE="main/main.cc" # 入口源文件
OUT_SUBDIR="项目分析报告" # 输出子目录
# =================================================
set -euo pipefail # 开启严格模式：遇错退出、未定义变量报错、管道失败即失败

main(){ # 主函数
    local ENTRY_FULL="${PROJECT_ROOT}/${ENTRY_FILE}" # 拼接入口文件完整路径
    local OUT_FULL="${PROJECT_ROOT}/${OUT_SUBDIR}/$(basename "${ENTRY_FILE}")-层级依赖树.txt" # 输出文件完整路径
    mkdir -p "$(dirname "${OUT_FULL}")" # 若输出目录不存在则递归创建

    echo "⏳ 正在扫描头文件，请稍等..." # 打印提示
    declare -A HDR_MAP # 声明关联数组，用于存储头文件映射
    while IFS= read -r -d '' h; do # 以 null 为分隔符读取所有 .h 文件
        HDR_MAP["$(basename "$h")"]+="$h"$'\n' # 以文件名为键，完整路径为值，允许多路径
    done < <(find "${PROJECT_ROOT}" "${IDF_ROOT}" -type f -iname '*.h' -print0) # 在项目根和 IDF 根下查找所有头文件

    extract(){ # 定义提取头文件名的函数
        grep -oE '^\s*#\s*include\s+["<][^">]+[">]' "$1" 2>/dev/null | # 匹配 #include 行
        sed -E 's/^[^"<]*["<]//; s/[">].*$//' | # 去掉前后缀，保留文件名
        xargs -n1 basename 2>/dev/null || true # 取 basename，忽略错误
    }

    declare -A SEEN_INC        # 仅用于“已打印”去重
    declare -A STACK           # 用于循环依赖检测
    local ROOT_IDX=1 # 根序号从 1 开始

    # DFS 递归
    walk(){ # 递归遍历依赖
        local prefix=$1 inc=$2 lvl=$3 # 参数：前缀、当前头文件、层级
        [[ -n "${STACK[$inc]:-}" ]] && { printf "%*s%s: %s  [Circular Dependency!]\n" $((lvl*2)) "" "${prefix}" "${inc}"; return; } # 检测到循环依赖
        [[ -n "${SEEN_INC[${inc}]:-}" ]] && return   # 已打印过就不再展开
        SEEN_INC["${inc}"]=1 # 标记已打印
        STACK["${inc}"]=1 # 入栈，用于循环检测

        local found= # 是否找到标志
        local cand # 候选路径
        while IFS= read -r cand; do # 读取该头文件所有可能路径
            [[ -f "$cand" ]] || continue # 文件不存在则跳过
            local sub_counter=1 sub_inc # 子序号与头文件
            for sub_inc in $(extract "$cand"); do # 提取该头文件包含的子头文件
                local new_prefix="${prefix}.${sub_counter}" # 构造新前缀
                printf "%*s%s: %s\n" $((lvl*2)) "" "${new_prefix}" "${sub_inc}" # 打印子节点
                walk "${new_prefix}" "${sub_inc}" $((lvl+1)) # 递归
                ((sub_counter++)) # 序号自增
            done
            found=1 # 找到至少一个有效路径
            break # 只取第一个有效路径
        done < <(printf '%s' "${HDR_MAP[$inc]:-}") # 从映射中读取路径列表

        [[ $found ]] || printf "%*s%s: %s  [Not Found]\n" $((lvl*2)) "" "${prefix}" "${inc}" # 未找到文件
        unset STACK["${inc}"]    # 回溯出栈
    }

    { # 开始重定向到输出文件
        printf "=== 层级依赖树（无黑名单，已检测循环依赖） ===\n" # 标题
        printf "0: %s\n" "$(basename "${ENTRY_FILE}")" # 打印入口文件名
        local inc # 临时变量
        for inc in $(extract "${ENTRY_FULL}"); do # 提取入口文件直接包含的头文件
            printf "%d: %s\n" "${ROOT_IDX}" "${inc}" # 打印第一层
            walk "${ROOT_IDX}" "${inc}" 1 # 递归展开
            ((ROOT_IDX++)) # 根序号自增
        done
    } > "${OUT_FULL}" # 全部写入文件

    echo "✅ 新格式层级依赖树已写入：${OUT_FULL}" # 完成提示
}

main "$@" # 传入所有参数并执行主函数
