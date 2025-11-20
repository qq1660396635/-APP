“把 8~20 号例程文件夹里的 Core 子目录 tree 结果，连同对应文件夹名，一次性追加写进
/storage/emulated/0/Download/OnePlus\ Share/GITHUB\ 开源项目/项目01/野火小智文档/core_summary.txt”  

python3 -c "
# 引入 subprocess 用于在 Python 内调用外部命令（如 tree）
# 引入 pathlib 用于面向对象地操作文件系统路径
# 引入 re 用于正则表达式匹配目录名
import subprocess, pathlib, re

# 将根目录字符串封装为 Path 对象，后续可直接用 / 拼接子路径
root = pathlib.Path('/storage/emulated/0/Download/OnePlus Share/GITHUB 开源项目/项目01/野火小智文档')

# 拼接输出文件完整路径，等价于 os.path.join(root, 'core_summary.txt')
out  = root/'core_summary.txt'

# 以 UTF-8 编码、覆盖写模式打开文件；with 块结束时会自动 flush 并关闭文件
with out.open('w', encoding='utf-8') as f:
    # 循环生成 8 到 20（含）共 13 个实验编号
    for n in range(8, 21):
        # 为当前编号构造正则关键字：
        # 非 19 时精确匹配 "[n]"；19 时匹配 "[19" 前缀，从而覆盖 19-1 到 19-10
        key = fr'\[{n}\]' if n != 19 else r'\[19'

        # 按字典序遍历根目录下所有直接子项（文件或文件夹）
        for d in sorted(root.iterdir()):
            # 只处理目录，且目录名必须满足上面构造的正则
            if d.is_dir() and re.search(key, d.name):
                # 定位到该实验目录下的 Core 子目录
                core = d/'Core'
                # 只有 Core 目录真实存在时才写入标题并生成树状图
                if core.exists():
                    # 写入分隔行，方便阅读
                    f.write(f'\n======== {d.name} ========\n')
                    # 调用系统 tree 命令，把树状图直接重定向到文件；
                    # stderr 也合并到 stdout，保证报错信息不会出现在终端
                    subprocess.run(['tree', str(core)], stdout=f, stderr=subprocess.STDOUT)
                # 不 break，继续循环，确保同一编号（尤其是 19-x）全部被抓取
"
