说明
   1.  home下，新建2025放脚本  
   2.  安装之前，看有没有安装过


一    安卓相关安装步骤
# 0. Termux首次授权存储
termux-setup-storage
# 1. 更新软件源
pkg update -y && pkg upgrade -y
# 2. 安装基础工具链
pkg install -y wget unzip zip git openjdk-17 apksigner nodejs python
# 3. 创建Android SDK目录
mkdir -p $HOME/android-sdk/cmdline-tools
# 4. 进入SDK目录
cd $HOME/android-sdk/cmdline-tools
# 5. 下载命令行工具包
wget https://dl.google.com/android/repository/commandlinetools-linux-11076708_latest.zip
# 6. 解压并整理
unzip *.zip && mv cmdline-tools latest
# 7. 写入ANDROID_HOME
echo 'export ANDROID_HOME=$HOME/android-sdk' >> $HOME/.bashrc
# 8. 写入PATH
echo 'export PATH=$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/platform-tools:$PATH' >> $HOME/.bashrc
# 9. 重载环境变量
source $HOME/.bashrc
# 10. 安装SDK组件
sdkmanager "platform-tools" "platforms;android-33" "build-tools;33.0.2"
# 11. 回到HOME
cd $HOME
# 12. 下载Gradle 7.6
wget https://services.gradle.org/distributions/gradle-7.6-bin.zip
# 13. 解压Gradle
unzip gradle-7.6-bin.zip
# 14. 写入Gradle PATH
echo 'export PATH=$HOME/gradle-7.6/bin:$PATH' >> $HOME/.bashrc
# 15. 重载环境变量
source $HOME/.bashrc
# 16. 全局安装Cordova
npm i -g cordova
# 17. 验证Java版本
java -version
# 18. 验证Gradle版本
gradle --version
# 19. 验证SDK组件
sdkmanager --list | head
# 20. 创建Cordova项目
cordova create hello com.example.hello Hello
# 21. 进入项目目录
cd hello
# 22. 添加Android 12平台
cordova platform add android@12
# 23. 构建Debug APK
cordova build android



二   测试哪些安装   dpkg
for p in android-sdk-build-tools openjdk-17 aapt apksigner dx ecj; do
  dpkg -l | grep -q "^ii.*$p" \
    && echo "✅ $p: $(dpkg -l | awk -v pkg="$p" '$2==pkg {print $3}')" \
    || echo "❌ $p: 未安装"; done
    
 
 
 三   ecj安装
 # 1. 清掉空文件
rm -f $PREFIX/share/ecj.jar

# 2. 下载（Eclipse CDN，稳定）
wget https://www.eclipse.org/downloads/download.php?file=/eclipse/downloads/drops4/R-4.15-202003050155/ecj-4.15.jar \
  -O $PREFIX/share/ecj.jar

# 3. 确认大小（≈ 3.9 MB）
ls -lh $PREFIX/share/ecj.jar

# 4. 再测
ecj -version