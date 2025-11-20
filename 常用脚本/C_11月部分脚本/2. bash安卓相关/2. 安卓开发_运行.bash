案例一  标准流程
# 1. 清空旧目录
cd ~ && rm -rf 2025
# 2. 创建 Cordova 空项目
cordova create 2025 com.example.games2025 HTML5Games
# 3. 复制游戏文件
cd 2025 && rm -rf www/* && cp -r "/storage/emulated/0/Download/OnePlus Share/03 - 个人测试/测试/测试"/* www/ && ls www
# 4. 锁定版本添加平台
cordova platform add android@12.0.1 --no-fetch
# 5. 强制使用系统 aapt2
echo "android.aapt2FromMavenOverride=$(which aapt2)" >> platforms/android/gradle.properties
# 6. 清理缓存并构建
rm -rf ~/.gradle/caches/transforms-3/*aapt2*
cordova build android --no-daemon


案例二  离线路由，页面跳转
1. 清空旧目录
   cd ~ && rm -rf 2025

2. 创建 Cordova 空项目
   cordova create 2025 com.example.testGame TestGame

3. 在 2025 下新建 testGame 目录并复制所有游戏文件（不含原 index.html）
   mkdir -p 2025/testGame
   cp "/storage/emulated/0/Download/OnePlus Share/03 - 个人测试/03 - 脚本测试/脚本网站B 合集 单页面"/[0-9]*.html 2025/testGame/

4. 新建离线路由首页
   cat > 2025/testGame/index.html <<'EOF'
   <!doctype html><meta charset="utf-8"><title>游戏中心</title>
   <style>body{font-family:sans-serif;text-align:center;margin-top:10%;background:#f2f2f2}
   h1{margin-bottom:20px}.games{display:grid;grid-template-columns:1fr 1fr;gap:10px;padding:0 20px}
   a{background:#fff;border:1px solid #ccc;border-radius:8px;padding:20px;text-decoration:none;color:#333;box-shadow:0 2px 4px rgba(0,0,0,.1)}
   a:hover{transform:scale(1.05);transition:.2s}</style>
   <h1>离线路由游戏中心</h1>
   <div class="games">
   <a href="01_消消乐.html">消消乐</a>
   <a href="02_推箱子.html">推箱子</a>
   <a href="03_俄罗斯方块.html">俄罗斯方块</a>
   <a href="04_打地鼠.html">打地鼠</a>
   <a href="05_点灯游戏.html">点灯游戏</a>
   <a href="06.飞机大战.html">飞机大战</a>
   <a href="07_跳一跳.html">跳一跳</a>
   <a href="08_星际逃生.html">星际逃生</a>
   <a href="09_切水果.html">切水果</a>
   <a href="10_塔防游戏.html">塔防游戏</a>
   <a href="11_打砖块max.html">打砖块</a>
   <a href="12_尼姆博弈.html">尼姆博弈</a>
   <a href="13_台球.html">台球</a>
   </div>
   EOF

5. 提上来覆盖 www
   cd 2025 && rm -rf www/* && cp testGame/* www/

6. 锁定版本添加平台
   cordova platform add android@12.0.1 --no-fetch

7. 强制系统 aapt2 + 清理缓存
   echo "android.aapt2FromMavenOverride=/data/data/com.termux/files/usr/bin/aapt2" >> platforms/android/gradle.properties
   rm -rf ~/.gradle/caches/transforms-3/*aapt2*

8. 构建
   cordova build android --no-daemon

9. 复制到手机（成功后执行）
   cp ~/2025/platforms/android/app/build/outputs/apk/debug/app-debug.apk \
      "/storage/emulated/0/Download/OnePlus Share/03 - 个人测试/"

