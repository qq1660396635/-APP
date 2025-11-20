需求，手机启动服务器。并且可以在网站中链接这个服务器

一  代码部分
python3 -x <<'EOF'
# -*- coding: utf-8 -*-
from http.server import HTTPServer, BaseHTTPRequestHandler as RH

class H(RH):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write('<html><meta charset=utf-8><body><h1>你好世界</h1></body></html>'.encode('utf-8'))

HTTPServer(('', 8080), H).serve_forever()
EOF


二 访问网站
http://127.0.0.1:8080


三  简单优化，可双向通信
python3 -x <<'EOF'
# -*- coding: utf-8 -*-
import json
import socket
import subprocess
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
import threading

# 全局消息队列和锁
message_queue = []
queue_lock = threading.Lock()

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """支持多线程的HTTP服务器"""

class RequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
    
    def do_GET(self):
        if self.path == '/':
            self._set_headers()
            self.wfile.write(self._create_html().encode('utf-8'))
        elif self.path == '/messages':
            self._handle_messages()
        elif self.path == '/ip':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            # 获取热点IP地址
            hotspot_ip = self.get_hotspot_ip()
            self.wfile.write(json.dumps({"ip": hotspot_ip}).encode('utf-8'))
        else:
            self.send_error(404)
    
    def do_POST(self):
        if self.path == '/send':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            self._process_message(post_data)
            self._set_headers()
            self.wfile.write(b'Message received')
        else:
            self.send_error(404)
    
    def get_hotspot_ip(self):
        """获取手机热点IP地址"""
        try:
            # 尝试获取wlan0接口的IP（热点接口）
            result = subprocess.run(['ip', 'addr', 'show', 'wlan0'], capture_output=True, text=True)
            if result.returncode == 0:
                # 查找IPv4地址
                import re
                ip_match = re.search(r'inet (\d+\.\d+\.\d+\.\d+)/', result.stdout)
                if ip_match:
                    return ip_match.group(1)
            
            # 如果wlan0没有IP，尝试其他方法
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            try:
                s.connect(("8.8.8.8", 80))
                return s.getsockname()[0]
            finally:
                s.close()
        except:
            return "无法获取IP"
    
    def _process_message(self, data):
        try:
            message = json.loads(data.decode('utf-8'))['message']
            with queue_lock:
                message_queue.append(message)
            print(f"\n\033[1;35m收到消息: \033[1;36m{message}\033[0m")
        except:
            print("\n\033[1;31m无效消息格式\033[0m")
    
    def _handle_messages(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        with queue_lock:
            response = json.dumps({"messages": message_queue.copy()})
            message_queue.clear()
        self.wfile.write(response.encode('utf-8'))
    
    def _create_html(self):
        return f"""
        <!DOCTYPE html>
        <html lang="zh-CN">
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>Termux 通信中心</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
                    color: white;
                    margin: 0;
                    padding: 20px;
                    min-height: 100vh;
                }}
                .container {{
                    max-width: 800px;
                    margin: 0 auto;
                    background: rgba(255, 255, 255, 0.1);
                    backdrop-filter: blur(10px);
                    border-radius: 20px;
                    padding: 30px;
                    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
                }}
                h1 {{
                    text-align: center;
                    font-size: 2.5rem;
                    margin-bottom: 30px;
                    text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
                }}
                .message-box {{
                    background: rgba(255, 255, 255, 0.15);
                    border-radius: 15px;
                    padding: 20px;
                    margin-bottom: 25px;
                    max-height: 300px;
                    overflow-y: auto;
                }}
                .message {{
                    background: rgba(255, 255, 255, 0.2);
                    border-radius: 10px;
                    padding: 12px 15px;
                    margin-bottom: 10px;
                    animation: fadeIn 0.5s;
                }}
                @keyframes fadeIn {{
                    from {{ opacity: 0; transform: translateY(10px); }}
                    to {{ opacity: 1; transform: translateY(0); }}
                }}
                .input-group {{
                    display: flex;
                    gap: 10px;
                }}
                input {{
                    flex: 1;
                    padding: 15px;
                    border: none;
                    border-radius: 50px;
                    background: rgba(255, 255, 255, 0.2);
                    color: white;
                    font-size: 1rem;
                    outline: none;
                }}
                input::placeholder {{ color: rgba(255, 255, 255, 0.7); }}
                button {{
                    background: #ff2e63;
                    color: white;
                    border: none;
                    border-radius: 50px;
                    padding: 0 30px;
                    font-size: 1rem;
                    font-weight: bold;
                    cursor: pointer;
                    transition: all 0.3s;
                }}
                button:hover {{
                    background: #ff5c8d;
                    transform: translateY(-2px);
                    box-shadow: 0 5px 15px rgba(255, 46, 99, 0.4);
                }}
                .status {{
                    text-align: center;
                    margin-top: 20px;
                    font-size: 0.9rem;
                    opacity: 0.8;
                }}
                .ip-info {{
                    background: rgba(0, 0, 0, 0.2);
                    border-radius: 10px;
                    padding: 10px;
                    margin-top: 20px;
                    text-align: center;
                    font-size: 0.9rem;
                }}
                .copy-btn {{
                    background: #4CAF50;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    padding: 5px 10px;
                    margin-left: 10px;
                    cursor: pointer;
                    font-size: 0.8rem;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>✨ Termux 通信中心 ✨</h1>
                
                <div class="message-box" id="messageBox">
                    <div class="message">📢 已连接到Termux服务器！</div>
                </div>
                
                <div class="input-group">
                    <input type="text" id="messageInput" placeholder="输入消息发送到Termux终端...">
                    <button onclick="sendMessage()">发送</button>
                </div>
                
                <div class="status">
                    <p>连接状态: <span id="status">🟢 在线</span></p>
                </div>
                
                <div class="ip-info">
                    <p>其他设备访问地址: <span id="ipAddress">正在获取...</span>
                    <button class="copy-btn" onclick="copyIP()">复制</button></p>
                </div>
            </div>

            <script>
                const messageBox = document.getElementById('messageBox');
                const messageInput = document.getElementById('messageInput');
                const statusElem = document.getElementById('status');
                const ipAddressElem = document.getElementById('ipAddress');
                
                // 添加新消息到消息框
                function addMessage(text) {{
                    const msgDiv = document.createElement('div');
                    msgDiv.className = 'message';
                    msgDiv.textContent = text;
                    messageBox.prepend(msgDiv);
                    messageBox.scrollTop = 0;
                }}
                
                // 发送消息到服务器
                function sendMessage() {{
                    const message = messageInput.value.trim();
                    if (message) {{
                        fetch('/send', {{
                            method: 'POST',
                            headers: {{ 'Content-Type': 'application/json' }},
                            body: JSON.stringify({{ message }})
                        }});
                        addMessage(`📤 你: ${{message}}`);
                        messageInput.value = '';
                    }}
                }}
                
                // 按Enter发送消息
                messageInput.addEventListener('keypress', (e) => {{
                    if (e.key === 'Enter') sendMessage();
                }});
                
                // 轮询获取新消息
                async function fetchMessages() {{
                    try {{
                        const response = await fetch('/messages');
                        const data = await response.json();
                        data.messages.forEach(msg => addMessage(`📥 Termux: ${{msg}}`));
                        statusElem.innerHTML = '🟢 在线';
                    }} catch (error) {{
                        statusElem.innerHTML = '🔴 离线 - 尝试重新连接...';
                    }}
                    setTimeout(fetchMessages, 2000);
                }}
                
                // 获取服务器IP地址
                async function getServerIP() {{
                    try {{
                        const response = await fetch('/ip');
                        const data = await response.json();
                        ipAddressElem.textContent = `http://${{data.ip}}:8080`;
                    }} catch (error) {{
                        ipAddressElem.textContent = '无法获取IP地址';
                    }}
                }}
                
                // 复制IP地址到剪贴板
                function copyIP() {{
                    const text = ipAddressElem.textContent;
                    navigator.clipboard.writeText(text)
                        .then(() => alert('地址已复制到剪贴板'))
                        .catch(err => console.error('复制失败:', err));
                }}
                
                // 初始化
                fetchMessages();
                getServerIP();
            </script>
        </body>
        </html>
        """

if __name__ == '__main__':
    host = '0.0.0.0'  # 绑定到所有网络接口
    port = 8080
    
    # 获取热点IP地址
    def get_hotspot_ip():
        """获取手机热点IP地址"""
        try:
            # 尝试获取wlan0接口的IP（热点接口）
            result = subprocess.run(['ip', 'addr', 'show', 'wlan0'], capture_output=True, text=True)
            if result.returncode == 0:
                # 查找IPv4地址
                import re
                ip_match = re.search(r'inet (\d+\.\d+\.\d+\.\d+)/', result.stdout)
                if ip_match:
                    return ip_match.group(1)
            
            # 如果wlan0没有IP，尝试其他方法
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            try:
                s.connect(("8.8.8.8", 80))
                return s.getsockname()[0]
            finally:
                s.close()
        except:
            return "无法获取IP"
    
    hotspot_ip = get_hotspot_ip()

    print("\033[1;32m启动Termux通信服务器...\033[0m")
    print(f"\033[1;33m本机访问: \033[1;34mhttp://localhost:{port}\033[0m")
    print(f"\033[1;33m热点IP: \033[1;34mhttp://{hotspot_ip}:{port}\033[0m")
    print("\033[1;33m等待网页连接...\033[0m")
    
    server = ThreadedHTTPServer((host, port), RequestHandler)
    server.serve_forever()
EOF
