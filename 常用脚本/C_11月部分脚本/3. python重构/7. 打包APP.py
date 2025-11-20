#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 一体化 Cordova 构建工具（凉安V 定制版） - Python版

import os
import sys
import shutil
import random
import subprocess
import glob
from datetime import datetime

# --- 全局配置 ---
# 使用 os.path.expanduser 正确处理家目录路径
OUT_DIR = "/storage/emulated/0/Download"
PROJ_DIR = os.path.join(os.path.expanduser("~"), "2026")

def run_command(command, check=True, capture_output=False):
    """运行外部命令的辅助函数"""
    print(f"🔧 执行命令: {command}")
    try:
        # 使用 shell=True 是为了方便处理像 cordova, pkill 这样的复合命令
        # 在此脚本中，命令来源是可信的，风险可控
        result = subprocess.run(
            command,
            shell=True,
            check=check,
            capture_output=capture_output,
            text=True
        )
        if capture_output:
            return result.stdout.strip()
        return result
    except subprocess.CalledProcessError as e:
        print(f"❌ 命令执行失败: {command}")
        print(f"   错误信息: {e.stderr.strip() if e.stderr else '未知'}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"❌ 命令未找到: {command.split()[0]}")
        sys.exit(1)

# --- 任务一：打包网页为APK ---
def build_apk():
    """打包网页为APK"""
    print("\n=== 打包模式 ===")
    # 1. 获取用户输入 (模式、路径、版本号)
    print("1) 打包单个 HTML 文件")
    print("2) 打包整个目录（含 index.html）")
    mode = input("请选择 (1/2): ")
    if mode not in ("1", "2"):
        print("❌ 无效选择")
        return

    src_path = input("请输入路径（文件或目录）: ").strip()
    if not os.path.exists(src_path):
        print("❌ 路径不存在")
        return

    app_title = ask_app_name()

    # 2. 检查并安装依赖
    check_deps()

    # 3. 创建并配置Cordova项目
    if os.path.exists(PROJ_DIR):
        print(f"🧹 清理旧项目目录: {PROJ_DIR}")
        shutil.rmtree(PROJ_DIR)
    
    # Cordova 项目ID使用时间戳确保唯一性
    app_id = f"com.example.auto.v{int(datetime.now().timestamp())}"
    run_command(f"cordova create {PROJ_DIR} {app_id} '{app_title}'")
    
    original_cwd = os.getcwd()
    os.chdir(PROJ_DIR)
    print(f"📍 切换到项目目录: {os.getcwd()}")

    try:
        # 4. 复制源文件到www目录
        print("📋 复制源文件...")
        www_dir = "www"
        shutil.rmtree(www_dir, ignore_errors=True)
        os.makedirs(www_dir)

        if mode == "1":
            shutil.copy2(src_path, os.path.join(www_dir, "index.html"))
        else:
            # dirs_exist_ok=True 允许复制到已存在的目录
            shutil.copytree(src_path, www_dir, dirs_exist_ok=True)

        # 5. 添加Cordova插件和平台
        print("🔌 添加 InAppBrowser 插件...")
        run_command("cordova plugin add cordova-plugin-inappbrowser")
        print("🤖 添加 Android 平台...")
        run_command("cordova platform add android@12.0.1 --no-fetch")

        # 6. 配置Gradle以使用Termux的aapt2
        print("⚙️ 配置 Gradle...")
        gradle_props_path = os.path.join("platforms", "android", "gradle.properties")
        aapt2_termux_path = "/data/data/com.termux/files/usr/bin/aapt2"
        
        with open(gradle_props_path, "a") as f:
            f.write(f"\nandroid.aapt2FromMavenOverride={aapt2_termux_path}\n")
            f.write("android.enableAapt2Daemon=false\n")

        # 7. 清理构建缓存和旧文件
        print("🧹 清理构建缓存...")
        gradle_cache = os.path.expanduser("~/.gradle/caches/transforms-3")
        if os.path.exists(gradle_cache):
            for item in glob.glob(os.path.join(gradle_cache, "*aapt2*")):
                if os.path.isdir(item):
                    shutil.rmtree(item)
                else:
                    os.remove(item)
        
        shutil.rmtree("platforms/android/build", ignore_errors=True)
        shutil.rmtree("platforms/android/app/build", ignore_errors=True)
        shutil.rmtree("platforms/android/app/src/main/assets/www", ignore_errors=True)
        shutil.rmtree(os.path.expanduser("~/.npm/_cacache"), ignore_errors=True)
        shutil.rmtree(os.path.expanduser("~/.cordova/npm_cache"), ignore_errors=True)
        
        # 确保目标assets目录存在
        assets_www_dir = "platforms/android/app/src/main/assets/www"
        os.makedirs(assets_www_dir, exist_ok=True)
        shutil.copytree("www", assets_www_dir, dirs_exist_ok=True)
        
        # 杀死可能残留的gradle进程
        run_command("pkill -f gradle", check=False)

        # 8. 执行Cordova构建
        print("🏗️ 开始构建...")
        run_command("cordova build android")

        # 9. 复制最终APK到输出目录
        print("📦 复制APK...")
        os.makedirs(OUT_DIR, exist_ok=True)
        apk_src_path = "platforms/android/app/build/outputs/apk/debug/app-debug.apk"
        apk_dest_path = os.path.join(OUT_DIR, "凉安V1r.apk")
        shutil.copy2(apk_src_path, apk_dest_path)
        print(f"✅ 构建完成 → {apk_dest_path}")

    finally:
        # 确保无论如何都切换回原目录
        os.chdir(original_cwd)

# --- 任务二：修复并重新构建APK ---
def rebuild_apk():
    """修复并重新构建APK"""
    print("\n=== 修复重建模式 ===")
    # 1. 检查项目目录是否存在
    if not os.path.isdir(PROJ_DIR):
        print("❌ 项目目录不存在，请先运行打包")
        return

    # 2. 检查依赖
    check_deps()

    original_cwd = os.getcwd()
    os.chdir(PROJ_DIR)
    print(f"📍 切换到项目目录: {os.getcwd()}")

    try:
        # 3. 重新配置Gradle
        print("⚙️ 重新配置 Gradle...")
        gradle_props_path = "platforms/android/gradle.properties"
        aapt2_termux_path = "/data/data/com.termux/files/usr/bin/aapt2"
        
        with open(gradle_props_path, "w") as f: # 使用 'w' 覆盖写入，确保配置干净
            f.write(f"android.aapt2FromMavenOverride={aapt2_termux_path}\n")
            f.write("android.enableAapt2Daemon=false\n")

        # 4. 清理构建缓存和旧文件 (与build_apk中的逻辑相同)
        print("🧹 清理构建缓存...")
        gradle_cache = os.path.expanduser("~/.gradle/caches/transforms-3")
        if os.path.exists(gradle_cache):
            for item in glob.glob(os.path.join(gradle_cache, "*aapt2*")):
                if os.path.isdir(item):
                    shutil.rmtree(item)
                else:
                    os.remove(item)

        shutil.rmtree("platforms/android/build", ignore_errors=True)
        shutil.rmtree("platforms/android/app/build", ignore_errors=True)
        shutil.rmtree("platforms/android/app/src/main/assets/www", ignore_errors=True)
        shutil.rmtree(os.path.expanduser("~/.npm/_cacache"), ignore_errors=True)
        shutil.rmtree(os.path.expanduser("~/.cordova/npm_cache"), ignore_errors=True)
        
        assets_www_dir = "platforms/android/app/src/main/assets/www"
        os.makedirs(assets_www_dir, exist_ok=True)
        shutil.copytree("www", assets_www_dir, dirs_exist_ok=True)

        run_command("pkill -f gradle", check=False)

        # 5. 执行Cordova构建
        print("🏗️ 开始重新构建...")
        run_command("cordova build android")

        # 6. 复制最终APK到输出目录
        print("📦 复制APK...")
        os.makedirs(OUT_DIR, exist_ok=True)
        apk_src_path = "platforms/android/app/build/outputs/apk/debug/app-debug.apk"
        apk_dest_path = os.path.join(OUT_DIR, "MyBookmarks.apk")
        shutil.copy2(apk_src_path, apk_dest_path)
        print(f"✅ 修复重建完成 → {apk_dest_path}")

    finally:
        os.chdir(original_cwd)

# --- 任务三：复制最新APK ---
def copy_latest_apk():
    """复制最新APK"""
    print("\n=== 复制最新 APK ===")
    # 1. 检查项目目录是否存在
    if not os.path.isdir(PROJ_DIR):
        print("❌ 项目目录不存在")
        return

    original_cwd = os.getcwd()
    os.chdir(PROJ_DIR)
    print(f"📍 切换到项目目录: {os.getcwd()}")

    try:
        # 2. 查找项目中所有APK文件
        apk_list = glob.glob("./*.apk", recursive=True)
        if not apk_list:
            print("❌ 未找到 APK")
            return

        # 3. 确定最新的APK文件
        # 使用 max() 和 os.path.getmtime 找到最新修改的文件
        latest_apk_path = max(apk_list, key=os.path.getmtime)
        print(f"🔍 找到最新APK: {latest_apk_path}")

        # 4. 生成新的随机文件名
        new_name = rand_apk_name()

        # 5. 复制并重命名APK到输出目录
        os.makedirs(OUT_DIR, exist_ok=True)
        dest_path = os.path.join(OUT_DIR, new_name)
        shutil.copy2(latest_apk_path, dest_path)
        print(f"✅ 已复制 → {dest_path}")

    finally:
        os.chdir(original_cwd)

# --- 辅助函数 ---
def check_deps():
    """检查并安装必要的依赖"""
    print("🔍 检查依赖...")
    if not shutil.which("node"):
        print("❌ 请先 pkg install nodejs")
        sys.exit(1)

    # 检查 aapt2 是否已安装
    try:
        run_command("pkg list-installed aapt2", capture_output=True)
    except SystemExit:
        print("📦 aapt2 未安装，正在安装...")
        run_command("pkg install aapt2 -y")

    if not shutil.which("cordova"):
        print("📦 Cordova 未安装，正在全局安装...")
        run_command("npm i -g cordova")
    
    print("✅ 所有依赖检查通过。")

def ask_app_name():
    """询问版本号并生成应用名称"""
    ver = input("请输入今天版本号（如 11.2a）: ")
    if not ver:
        print("❌ 版本号不能为空")
        sys.exit(1)
    return f"凉安V{ver}"

def rand_apk_name():
    """生成带4位随机数的APK文件名"""
    num = random.randint(0, 9999)
    return f"凉安V{num:04d}.apk"

# --- 主程序入口 ---
if __name__ == "__main__":
    # 1. 显示主菜单
    print("=== Cordova 构建工具（凉安V 版）===")
    print("1) 打包网页为 APK（应用名=凉安V+版本号）")
    print("2) 修复并重新构建")
    print("3) 复制最新 APK（文件名=凉安V+4位随机）")
    
    # 2. 获取用户选择
    choice = input("请输入选择 (1/2/3): ")

    # 3. 根据选择调用对应函数
    if choice == "1":
        build_apk()
    elif choice == "2":
        rebuild_apk()
    elif choice == "3":
        copy_latest_apk()
    else:
        print("❌ 无效选择")

