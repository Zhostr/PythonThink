import http.server
import socketserver
import time
import random
from datetime import datetime, timedelta, timezone
import threading  # 多线程支持

PORT = 8000
COOKIE_PORT = 8001
CACHE_PORT = 8002

# 父类，实现设置 Date 响应头的功能
class BaseHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
         # 移除默认添加的 Date 头
        for header in self._headers_buffer:
            if header.lower().startswith(b'date:'):
                self._headers_buffer.remove(header)
        # 获取当前 UTC 时间并格式化为 HTTP 日期格式
        current_utc_time = datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')
        # 设置 Date 响应头
        self.send_header('Date', current_utc_time)
        # 调用父类的 end_headers 方法完成响应头发送
        super().end_headers()

class ChunkedHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.send_header('Transfer-Encoding', 'chunked')
        self.end_headers()

        chunks = ["Hello", " ", "World", "!"]
        for chunk in chunks:
            # 计算块的长度并以十六进制表示
            chunk_length = hex(len(chunk.encode()))[2:]
            # 发送块长度
            self.wfile.write(f"{chunk_length}\r\n".encode())
            # 发送块内容
            self.wfile.write(chunk.encode())
            self.wfile.write(b"\r\n")
            time.sleep(1)  # 模拟延迟

        # 发送结束块
        self.wfile.write(b"0\r\n\r\n")

class CookieHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if 'Cookie' in self.headers:
            cookies = self.headers['Cookie']
            print(f"Received Cookies: {cookies}")
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"Cookies received and printed on server.\n")
        else:
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')

            # 设置自定义 Cookie 并添加属性
            expires = (datetime.utcnow() + timedelta(seconds=30)).strftime("%a, %d %b %Y %H:%M:%S GMT")
            self.send_header('Set-Cookie', 'username=testuser; Expires=' + expires + '; HttpOnly; Path=/; Secure; SameSite=Strict')
            self.send_header('Set-Cookie', 'userid=12345; Expires=' + expires + '; HttpOnly; Path=/; Secure; SameSite=Strict')
            self.send_header('Set-Cookie', 'sessionid=abcde12345; Expires=' + expires + '; HttpOnly; Path=/; Secure; SameSite=Strict')

            self.end_headers()
            self.wfile.write(b"No cookies found. Custom cookies sent to client.\n")

class CacheHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 生成随机数
        random_number = random.randint(1, 100)

        # 响应内容
        content = f"Hello, World! Random number: {random_number}".encode()

        # 设置响应头
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.send_header('Cache-Control', 'max-age=10')  # 设置缓存有效期
        self.send_header('Content-Length', str(len(content)))
        super().end_headers()

        # 发送响应内容
        self.wfile.write(content)

'''
socketserver.TCPServer 默认以阻塞模式运行，代码中先启动了端口 8000 的服务器，导致后续代码无法继续执行
with socketserver.TCPServer(("", PORT), ChunkedHandler) as httpd:
    print(f"Serving at port {PORT}")
    httpd.serve_forever()

# 启动第二个服务器（CookieHandler）
with socketserver.TCPServer(("", COOKIE_PORT), CookieHandler) as httpd:
    print(f"Serving at port {COOKIE_PORT}")
    httpd.serve_forever()
'''

# 定义服务器启动函数
def start_server(port, handler):
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Serving at port {port}")
        httpd.serve_forever()

# 创建并启动多个线程
threading.Thread(target=start_server, args=(PORT, ChunkedHandler)).start()
threading.Thread(target=start_server, args=(COOKIE_PORT, CookieHandler)).start()
threading.Thread(target=start_server, args=(CACHE_PORT, CacheHandler)).start()

# 主线程保持运行
while True:
    time.sleep(1)