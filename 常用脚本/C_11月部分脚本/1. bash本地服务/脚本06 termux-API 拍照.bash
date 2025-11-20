# 1. 设置文件名并拍照
F=/sdcard/Download/photo_$(date +%Y%m%d_%H%M%S).jpg \
&& termux-camera-photo -c 0 "$F"          # 拍照保存

# 2. 扫描进系统相册。。   刷新图库
am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d "file://$F"

# 3. 打开刚拍的照片      调用图库查看
termux-open "$F"                       







1. termux-battery-status —— 读电量、健康度、温度、实时电流  
2. termux-sms-send —— 后台偷偷发短信（可带多条收件人）  
3. termux-sms-inbox —— 把收件箱全部导出来，json 格式  
4. termux-location —— 拿 GPS/网络定位，精度可调  
5. termux-vibrate —— 让手机震一下，可设毫秒数  
6. termux-volume —— 读/设媒体、铃声音量  
7. termux-brightness —— 直接改屏幕亮度（0-255）  
8. termux-torch —— 开关手电筒  
9. termux-wifi-connectioninfo —— 当前 Wi-Fi 名称、IP、网关、信号强度  
10. termux-wifi-enable true/false —— 秒开/关 Wi-Fi  
11. termux-cellinfo —— 附近基站信息全 dump  
12. termux-telephony-deviceinfo —— IMEI、运营商、网络类型  
13. termux-clipboard-get / set —— 读写剪贴板  
14. termux-contact-list —— 把通讯录一次性拉出来  
15. termux-call —— 直接拨号（只拨不出声，可秒挂）  
16. termux-notification —— 自定义通知栏图标、文字、按钮  
17. termux-notification-remove —— 撤销刚才的通知  
18. termux-toast —— 屏幕底部轻提示  
19. termux-dialog —— 弹出原生输入框、单选、多选、日期、时间  
20. termux-download —— 后台下载文件，可断点续传  
21. termux-sensor —— 列出所有传感器并实时输出数据（加速度、陀螺仪、磁场、气压…）  
22. termux-microphone-record —— 后台录音，可限时长、限大小  
23. termux-microphone-stop —— 停止录音并自动保存到 Download  
24. termux-tts-engines —— 列出系统语音引擎  
25. termux-tts-speak —— 文字转语音，可指定语言和语速  
26. termux-wake-lock / termux-wake-unlock —— 禁止/允许系统休眠  
27. termux-fingerprint —— 调指纹弹窗，返回成功/失败（可做多因素认证）  
28. termux-camera-info —— 列出前后摄像头分辨率、对焦模式等  
29. termux-camera-photo -c 1 —— 切换前摄自拍  
30. termux-media-player play / pause / stop —— 本地后台播放器  
31. termux-media-scan —— 手动把任意文件刷进媒体库  
32. termux-share —— 把文件/文字甩到系统分享面板  
33. termux-storage-get —— 调系统文件选择器，用户选完返回路径  
34. termux-bt-adapter-enable true/false —— 开关蓝牙（需 Android 12 以下或授权）  
35. termux-bt-device-list —— 列出已配对蓝牙设备  
36. termux-usb —— 列举 USB 设备（可配合 libusb 做更多事）  
37. termux-job-scheduler —— 注册系统级定时任务（省电调度）  
38. termux-url-opener —— 把任意链接甩给默认浏览器  
39. termux-open --chooser —— 强制弹出“用哪个 App 打开”的选择器  
40. termux-reset —— 一键清掉 Termux 所有数据（摸鱼后毁尸灭迹）