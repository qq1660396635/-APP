需求，还在担心视频被百度网盘迅雷封杀吗？

脚本01  加密91视频 ，全部MP4转TXT
#!/data/data/com.termux/files/usr/bin/bash
cd "/storage/emulated/0/Download/OnePlus Share/GITHUB 开源项目/项目01/脚本/02 不可描述/A" || exit 1
find . -type f -iname '*.mp4' -exec sh -c 'mv "$1" "${1%.mp4}.txt"' _ {} \;



脚本02  解密91视频，全部TXT转MP4
#!/data/data/com.termux/files/usr/bin/bash
cd "/storage/emulated/0/Download/OnePlus Share/GITHUB 开源项目/项目01/脚本/02 不可描述/A" || exit 1
find . -type f -iname '*.txt' -exec sh -c 'mv "$1" "${1%.txt}.mp4"' _ {} \;
