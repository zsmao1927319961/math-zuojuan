# -*- coding: utf-8 -*-
# 本地验证服务器：所有响应带 no-store，杜绝浏览器 HTTP 缓存干扰验证
# 用法：python3.13 tools/serve.py [端口]   （默认 8642，在仓库根目录下起服务）
import os, sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8642
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

class H(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()
    def log_message(self, *a):
        pass

print('serving %s @ http://127.0.0.1:%d (no-store)' % (ROOT, PORT))
ThreadingHTTPServer(('127.0.0.1', PORT), H).serve_forever()
