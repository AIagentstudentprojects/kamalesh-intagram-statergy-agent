import json, os, urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from .prompt import SYSTEM_PROMPT, SCHEMA, build_user_prompt, fallback_strategy

ROOT = Path(__file__).resolve().parent.parent

def load_env():
    env = ROOT / '.env'
    if env.exists():
        for line in env.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ.setdefault(key.strip(), value.strip())

def validate(data):
    required = ['brand', 'niche', 'audience', 'offer', 'goal']
    if not isinstance(data, dict): raise ValueError('Request body must be a JSON object.')
    for key in required:
        if not str(data.get(key, '')).strip(): raise ValueError(f'Missing required field: {key}.')
    return {k: str(v).strip() for k, v in data.items()}

def ai_strategy(data):
    key = os.getenv('OPENAI_API_KEY')
    if not key: return None
    base = os.getenv('OPENAI_API_BASE', 'https://api.openai.com/v1').rstrip('/')
    payload = {'model': os.getenv('MODEL', 'gpt-5-mini'), 'messages': [{'role': 'system', 'content': SYSTEM_PROMPT}, {'role': 'user', 'content': build_user_prompt(data)}], 'response_format': {'type': 'json_schema', 'json_schema': {'name': 'instagram_strategy', 'strict': True, 'schema': SCHEMA}}, 'max_completion_tokens': 6000}
    req = urllib.request.Request(base + '/chat/completions', data=json.dumps(payload).encode(), headers={'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json'}, method='POST')
    with urllib.request.urlopen(req, timeout=90) as response:
        body = json.loads(response.read())
    content = body['choices'][0]['message']['content']
    return json.loads(content)

class Handler(BaseHTTPRequestHandler):
    def send_json(self, status, value):
        raw = json.dumps(value, ensure_ascii=False).encode()
        self.send_response(status); self.send_header('Content-Type', 'application/json; charset=utf-8'); self.send_header('Content-Length', str(len(raw))); self.end_headers(); self.wfile.write(raw)
    def do_GET(self):
        if self.path == '/api/health': return self.send_json(200, {'ok': True, 'ai_configured': bool(os.getenv('OPENAI_API_KEY'))})
        if self.path in ('/', '/index.html'):
            raw = (ROOT / 'public' / 'index.html').read_bytes(); self.send_response(200); self.send_header('Content-Type', 'text/html; charset=utf-8'); self.send_header('Content-Length', str(len(raw))); self.end_headers(); self.wfile.write(raw); return
        self.send_error(404)
    def do_POST(self):
        if self.path != '/api/strategy': return self.send_error(404)
        try:
            length = int(self.headers.get('Content-Length', '0')); data = validate(json.loads(self.rfile.read(length)))
            try:
                strategy = ai_strategy(data); source = 'ai' if strategy else 'fallback'
            except Exception as exc:
                strategy, source = fallback_strategy(data), 'fallback'
                print(f'AI provider unavailable; using fallback: {exc}')
            self.send_json(200, {'strategy': strategy, 'source': source, 'model': os.getenv('MODEL', 'gpt-5-mini')})
        except ValueError as exc: self.send_json(400, {'error': str(exc)})
        except Exception as exc: self.send_json(500, {'error': 'Unexpected server error.', 'detail': str(exc)})
    def log_message(self, format, *args): print(format % args)

def main():
    load_env(); port = int(os.getenv('PORT', '8000')); print(f'Instagram Strategy Agent running at http://localhost:{port}')
    ThreadingHTTPServer(('0.0.0.0', port), Handler).serve_forever()

if __name__ == '__main__': main()
