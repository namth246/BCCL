import json
import sys

sys.stdout.reconfigure(encoding="utf-8")
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse
from market_data import fetch_market_week
class Handler(SimpleHTTPRequestHandler):
 def __init__(self,*a,**k): super().__init__(*a,directory=Path(__file__).parent,**k)
 def do_GET(self):
  p=urlparse(self.path)
  if p.path!='/api/market-week': return super().do_GET()
  q=parse_qs(p.query); start,end=q.get('start',[''])[0],q.get('end',[''])[0]
  if len(start)!=10 or len(end)!=10:return self.reply(400,{'error':'Khoảng ngày không hợp lệ.'})
  try:return self.reply(200,fetch_market_week(start,end))
  except Exception as e:return self.reply(502,{'error':str(e)})
 def reply(self,status,payload):
  body=json.dumps(payload,ensure_ascii=False).encode('utf-8');self.send_response(status);self.send_header('Content-Type','application/json; charset=utf-8');self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body)
def create_server(port=8000): return ThreadingHTTPServer(('127.0.0.1',port),Handler)
if __name__=='__main__':
 server=create_server();print(f'Mở http://127.0.0.1:{server.server_port}');server.serve_forever()
