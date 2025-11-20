#!/data/data/com.termux/files/usr/bin/bash
# Termux猜数字游戏
# 作者：根据你的需求定制
# L.说明 ，后续可自行拓展。猜老师，猜对跳转网址。自己刷题，100道等

echo "🎯 欢迎来到Termux猜数字游戏！"
echo "================================"

# 生成1-100之间的随机数
target=$(( RANDOM % 100 + 1 ))
attempts=0
max_attempts=10

echo "我已经想了一个1到100之间的神秘数字。"
echo "你有 $max_attempts 次机会猜中它！"
echo ""

while [ $attempts -lt $max_attempts ]; do
    remaining=$((max_attempts - attempts))
    echo "📊 你还剩 $remaining 次机会"
    read -p "请输入你猜的数字（1-100）: " guess
    
    # 检查输入是否为数字
    if ! [[ "$guess" =~ ^[0-9]+$ ]]; then
        echo "❌ 请输入有效的数字！"
        continue
    fi
    
    guess=$((guess))
    attempts=$((attempts + 1))
    
    if [ $guess -eq $target ]; then
        echo "🎉 恭喜你！猜对了！"
        echo "✅ 你用了 $attempts 次猜中了数字 $target"
        break
    elif [ $guess -lt $target ]; then
        echo "📈 太小了！往大点猜。"
    else
        echo "📉 太大了！往小点猜。"
    fi
    
    # 给出提示
    difference=$((guess - target))
    if [ ${difference#-} -le 5 ]; then
        echo "🔥 非常接近了！"
    elif [ ${difference#-} -le 15 ]; then
        echo "💡 有点接近了！"
    fi
    echo ""
done

if [ $attempts -eq $max_attempts ] && [ $guess -ne $target ]; then
    echo "💀 游戏结束！数字是 $target"
    echo "💡 下次运气会更好！"
fi

echo ""
echo "感谢游玩！"
