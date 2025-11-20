一  需求分析
1. 需求：视频转PDF工具，我们家下载的91学习视频「1991年数学视频」，转PDF

2. 功能：将视频文件每隔10秒提取一帧图片，合并生成PDF文档

3. 执行流程：
   1. ffmpeg按时间间隔提取视频帧为JPG图片
   2. ImageMagick将图片序列合并为PDF文件
   3. 清理临时文件并输出结果
   
二   代码 
 #!/data/data/com.termux/files/usr/bin/bash
# 设置路径
INPUT_VIDEO="/storage/emulated/0/Download/OnePlus Share/GITHUB 开源项目/项目01/脚本/2025-ouikk-4.mp4"
OUTPUT_DIR="$(dirname "$INPUT_VIDEO")/temp_frames"
PDF_OUTPUT="${INPUT_VIDEO%.mp4}.pdf"

echo "开始处理视频: $INPUT_VIDEO"
echo "输出目录: $OUTPUT_DIR"
echo "PDF输出: $PDF_OUTPUT"

# 创建临时目录
mkdir -p "$OUTPUT_DIR"
cd "$(dirname "$INPUT_VIDEO")"

# 提取帧（每10秒一帧）
echo "正在提取视频帧..."
ffmpeg -v error -i "$INPUT_VIDEO" -vf "fps=1/10" -q:v 2 "temp_frames/frame_%04d.jpg"

# 检查提取结果
FRAME_COUNT=$(ls "$OUTPUT_DIR"/*.jpg 2>/dev/null | wc -l)
if [ $FRAME_COUNT -eq 0 ]; then
    echo "❌ 错误：未提取到任何帧！"
    echo "可能原因："
    echo "1. 输入视频路径不正确"
    echo "2. ffmpeg未正确安装"
    echo "3. 视频格式不支持"
    exit 1
else
    echo "✅ 成功提取 $FRAME_COUNT 帧图像"
fi

# 合并为PDF
echo "正在合并帧为PDF..."
cd "temp_frames"
mapfile -t FRAMES < <(ls *.jpg 2>/dev/null | sort)
magick "${FRAMES[@]}" "$PDF_OUTPUT"

# 清理
cd ..
rm -rf "temp_frames"

echo "✅ PDF合并完成: $PDF_OUTPUT"
echo "✅ 文件大小: $(du -h "$PDF_OUTPUT" | cut -f1)"
