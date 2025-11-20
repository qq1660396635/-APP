#!/bin/bash

# --- 配置区域 ---
# 每次请求之间的延迟时间（秒）
DELAY=2
# --- 配置结束 ---


# 定义API列表数组
# 格式: "类别|接口名称|接口地址"
APIS=(
    "聚合数据平台|手机号码归属地|https://www.juhe.cn/docs/api/id/11"
    "聚合数据平台|历史上的今天|https://www.juhe.cn/docs/api/id/63"
    "聚合数据平台|身份证查询|https://www.juhe.cn/docs/api/id/38"
    "聚合数据平台|邮编查询|https://www.juhe.cn/docs/api/id/66"
    "聚合数据平台|IP地址查询|https://www.juhe.cn/docs/api/id/1"
    "聚合数据平台|股票数据|https://www.juhe.cn/docs/api/id/21"
    "聚合数据平台|基金财务数据|https://www.juhe.cn/docs/api/id/28"
    "聚合数据平台|汇率查询|https://www.juhe.cn/docs/api/id/80"
    "聚合数据平台|星座运势|https://www.juhe.cn/docs/api/id/58"
    "聚合数据平台|笑话大全|https://www.juhe.cn/docs/api/id/95"
    "聚合数据平台|周公解梦|https://www.juhe.cn/docs/api/id/64"
    "聚合数据平台|电影票房|https://www.juhe.cn/docs/api/id/44"
    "聚合数据平台|语音识别|https://www.juhe.cn/docs/api/id/134"
    "聚合数据平台|成语词典|https://www.juhe.cn/docs/api/id/157"
    "聚合数据平台|问答机器人|https://www.juhe.cn/docs/api/id/112"
    "聚合数据平台|全国WIFI|https://www.juhe.cn/docs/api/id/18"
    "聚合数据平台|网站安全检测|https://www.juhe.cn/docs/api/id/19"
    "聚合数据平台|手机固话来电显示|https://www.juhe.cn/docs/api/id/72"
    "聚合数据平台|新闻头条|https://www.juhe.cn/docs/api/id/235"
    "聚合数据平台|万年历|https://www.juhe.cn/docs/api/id/177"
    "聚合数据平台|NBA赛事|https://www.juhe.cn/docs/api/id/92"
    "API Store平台|IP地址查询|http://apistore.baidu.com/apiworks/servicedetail/114.html"
    "API Store平台|身份证查询|http://apistore.baidu.com/apiworks/servicedetail/113.html"
    "API Store平台|手机号码归属地|http://apistore.baidu.com/apiworks/servicedetail/794.html"
    "API Store平台|频道新闻API_易源|http://apistore.baidu.com/apiworks/servicedetail/688.html"
    "API Store平台|微信热门精选|http://apistore.baidu.com/apiworks/servicedetail/632.html"
    "API Store平台|体育新闻|http://apistore.baidu.com/apiworks/servicedetail/711.html"
    "API Store平台|科技新闻|http://apistore.baidu.com/apiworks/servicedetail/1061.html"
    "API Store平台|国际新闻|http://apistore.baidu.com/apiworks/servicedetail/823.html"
    "API Store平台|美女图片|http://apistore.baidu.com/apiworks/servicedetail/720.html"
    "API Store平台|音乐搜索|http://apistore.baidu.com/apiworks/servicedetail/1020.html"
    "API Store平台|笑话大全|http://apistore.baidu.com/apiworks/servicedetail/864.html"
    "API Store平台|图灵机器人|http://apistore.baidu.com/apiworks/servicedetail/736.html"
    "API Store平台|语音合成|http://apistore.baidu.com/apiworks/servicedetail/867.html"
    "API Store平台|天气查询|http://apistore.baidu.com/apiworks/servicedetail/112.html"
    "API Store平台|中国和世界天气预报|http://apistore.baidu.com/apiworks/servicedetail/478.html"
    "API Store平台|去哪儿网火车票|http://apistore.baidu.com/apiworks/servicedetail/697.html"
    "API Store平台|去哪儿景点门票查询|http://apistore.baidu.com/apiworks/servicedetail/140.html"
    "API Store平台|天狗健康菜谱|http://apistore.baidu.com/apiworks/servicedetail/987.html"
    "API Store平台|天狗药品查询|http://apistore.baidu.com/apiworks/servicedetail/916.html"
    "API Store平台|天狗医院大全|http://apistore.baidu.com/apiworks/servicedetail/988.html"
    "API Store平台|pullword在线分词服务|http://apistore.baidu.com/apiworks/servicedetail/143.html"
    "API Store平台|汉字转拼音|http://apistore.baidu.com/apiworks/servicedetail/1124.html"
    "其他平台|淘宝开放平台|http://open.taobao.com/?spm=a219a.7395905.1.1.YdFDV6"
    "其他平台|图灵语音|http://www.tuling123.com/help/h_cent_andriodsdk.jhtml?nav=doc"
    "其他平台|融云IM|https://developer.rongcloud.cn/signin?returnUrl=%2Fapp%2Fappkey%2FPv4vYQwaxSZdfpLX5AI%3D"
    "其他平台|高德地图|http://lbs.amap.com/"
    "其他平台|蜻蜓|http://open.qingting.fm"
)

echo "=========================================="
echo "       API 接口连通性测试脚本"
echo "=========================================="
echo "开始测试... 每次请求间隔 ${DELAY} 秒。"
echo "------------------------------------------"

# 遍历数组中的每一个API
for api_info in "${APIS[@]}"; do
    # 使用 IFS (Internal Field Separator) 和 read 命令来分割字符串
    IFS='|' read -r category name url <<< "$api_info"

    echo -n "正在测试: $name ... "

    # 使用 curl 发送请求
    # -s: 静默模式，不显示进度和错误
    # -L: 跟随重定向
    # -o /dev/null: 将响应内容丢弃到黑洞
    # -w "%{http_code}": 在最后只输出HTTP状态码
    # --connect-timeout 10: 设置连接超时为10秒，防止卡死
    http_code=$(curl -s -L -o /dev/null -w "%{http_code}" --connect-timeout 10 "$url")

    # 判断状态码
    # 2xx 开头表示成功，3xx 开头表示重定向成功（因为用了-L，所以也算成功）
    if [[ "$http_code" =~ ^[23] ]]; then
        # \033[32m 是绿色，\033[0m 是恢复默认颜色
        echo -e "\033[32m✅ 成功 (状态码: $http_code)\033[0m"
        # 按照您的要求，如果成功了就在控制台打印详细信息
        echo -e "   ---> 类别: $category"
        echo -e "   ---> 地址: $url"
    else
        # \033[31m 是红色
        echo -e "\033[31m❌ 失败 (状态码: $http_code)\033[0m"
    fi

    echo "------------------------------------------"
    
    # 暂停指定秒数
    sleep $DELAY
done

echo "所有API测试完成。"
