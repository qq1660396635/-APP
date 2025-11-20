#   L.  已对代码进行优化，便于人类阅读，先看main
 
python3 -x <<'EOF'   #   Python转bash
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
M3U8视频下载脚本
87000固定，87100-87200随到随下
单线程+极简提示+跳过>500MB文件
"""

import os
import subprocess
import requests
from pathlib import Path

# ==================== 配置常量 ====================
BASE_URL = "https://你的视频地址🔗🔗🔗🔗🔗🔗/87000"
START_ID = 87100
END_ID = 87200
SAVE_ROOT = "/storage/emulated/0/Download/OnePlus Share/GITHUB 开源项目/项目01/脚本/02 不可描述"
USER_AGENT = "Mozilla/5.0 (Linux; Android 13; SM-G973F) AppleWebKit/537.36"
MAX_FILE_SIZE_MB = 500
REQUEST_TIMEOUT = 10
DOWNLOAD_TIMEOUT = 3600

HEADERS = {"User-Agent": USER_AGENT}


# ==================== 功能函数（按调用顺序排列） ====================
def check_m3u8_accessible(m3u8_url: str) -> bool:
    """
    检查M3U8文件是否可访问
    
    参数: m3u8_url - M3U8文件URL
    返回: 布尔值
    """
    try:
        response = requests.get(m3u8_url, headers=HEADERS, timeout=5)
        return response.text.startswith("#EXTM3U")
    except requests.RequestException:
        return False


def get_save_folder(video_id: int, start_id: int, save_root: str) -> Path:
    """
    获取视频保存文件夹路径
    
    参数: 
        video_id - 视频ID
        start_id - 起始ID  
        save_root - 保存根目录
    返回: 文件夹Path对象
    """
    # 每20个视频一个文件夹
    folder_start = start_id + ((video_id - start_id) // 20) * 20
    folder_name = f"{folder_start}-{folder_start + 19}"
    folder_path = Path(save_root) / folder_name
    folder_path.mkdir(parents=True, exist_ok=True)
    
    return folder_path


def get_video_size_mb(m3u8_url: str) -> int:
    """
    估算M3U8视频文件大小(MB)
    
    参数: m3u8_url - M3U8文件URL
    返回: 估算大小(MB)，失败返回0
    """
    try:
        # 1. 获取M3U8内容
        response = requests.get(m3u8_url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        lines = [line.strip() for line in response.text.splitlines() if line.strip()]
        
        # 2. 查找分片信息
        segment_line = next((line for line in lines if not line.startswith("#")), None)
        if not segment_line:
            return 0
        
        # 3. 构建分片URL
        base_url = m3u8_url.rsplit("/", 1)[0]
        segment_url = f"{base_url}/{segment_line}"
        
        # 4. 获取分片头部估算比特率
        segment_head = requests.get(
            segment_url, 
            headers={**HEADERS, "Range": "bytes=0-1023"}, 
            timeout=REQUEST_TIMEOUT
        ).content
        
        # 5. 使用ffprobe获取比特率
        bitrate_output = subprocess.check_output(
            ["ffprobe", "-v", "error", "-show_entries", "format=bit_rate", "-of", "csv=p=0", "-"],
            input=segment_head, 
            stderr=subprocess.DEVNULL,
        ).decode().strip()
        
        bitrate = int(bitrate_output) if bitrate_output.isdigit() else 1_000_000
        
        # 6. 计算总时长
        total_duration = 0.0
        for line in lines:
            if line.startswith("#EXTINF:"):
                total_duration += float(line.split(":")[1].split(",")[0])
        
        return int(bitrate * total_duration / 8 / 1024 / 1024) if total_duration > 0 else 0
        
    except Exception:
        return 0


def download_video(m3u8_url: str, output_file: Path, video_id: int) -> bool:
    """
    下载M3U8视频文件
    
    参数:
        m3u8_url - M3U8文件URL
        output_file - 输出文件路径  
        video_id - 视频ID
    返回: 布尔值
    """
    try:
        result = subprocess.run(
            [
                "ffmpeg", "-hide_banner", "-loglevel", "error", "-nostats", "-y",
                "-user_agent", USER_AGENT, "-i", m3u8_url, "-c", "copy", str(output_file)
            ],
            timeout=DOWNLOAD_TIMEOUT
        )
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print(f"[超时] {video_id}")
        return False
    except Exception as error:
        print(f"[错误] {video_id}: {error}")
        return False


def main():
    """主函数"""
    # 一、初始化
    Path(SAVE_ROOT).mkdir(parents=True, exist_ok=True)
    print(f"[开始] 下载范围 {START_ID}-{END_ID}")
    
    success_count, skip_count, fail_count = 0, 0, 0
    
    # 二、遍历视频ID
    for video_id in range(START_ID, END_ID + 1):
        m3u8_url = f"{BASE_URL}/{video_id}/index.m3u8"
        
        # 1. 检查可访问性
        if not check_m3u8_accessible(m3u8_url):
            print(f"[跳过] {video_id} 不可访问")
            skip_count += 1
            continue
        
        # 2. 获取保存路径
        save_folder = get_save_folder(video_id, START_ID, SAVE_ROOT)
        output_file = save_folder / f"{video_id}.mp4"
        
        # 3. 检查文件存在
        if output_file.exists():
            print(f"[存在] {video_id}.mp4")
            skip_count += 1
            continue
        
        # 4. 估算文件大小
        file_size = get_video_size_mb(m3u8_url)
        if file_size > MAX_FILE_SIZE_MB:
            print(f"[跳过] {video_id} 大小{file_size}MB>500MB")
            skip_count += 1
            continue
        
        # 5. 下载视频
        print(f"[下载] {video_id} 大小{file_size}MB")
        if download_video(m3u8_url, output_file, video_id):
            print(f"[完成] {video_id}.mp4")
            success_count += 1
        else:
            print(f"[失败] {video_id}.mp4")
            fail_count += 1
    
    # 三、输出总结
    print(f">>> 全部结束! 成功:{success_count}, 跳过:{skip_count}, 失败:{fail_count}")


if __name__ == "__main__":
    main()

EOF