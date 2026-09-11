import os
import time
from flask import Flask, jsonify
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)
REQUEST_COUNT = Counter('flask_http_requests_total','Total HTTP requests',['method','endpoint','status'])
REQUEST_LATENCY = Histogram('flask_http_request_duration_seconds','HTTP request latency',['method','endpoint'])

@app.before_request
def before_request():
    from flask import g
    g.start_time = time.time()

@app.after_request
def after_request(response):
    from flask import request, g
    elapsed = time.time() - getattr(g, 'start_time', time.time())
    REQUEST_COUNT.labels(request.method, request.path, response.status_code).inc()
    REQUEST_LATENCY.labels(request.method, request.path).observe(elapsed)
    return response

@app.get('/')
def home():
    return jsonify(application='devops-flask-app', version=os.getenv('APP_VERSION','1.0.0'), environment=os.getenv('ENVIRONMENT','local'), message='DevOps pipeline is working')

@app.get('/health')
def health(): return jsonify(status='UP'), 200

@app.get('/ready')
def ready(): return jsonify(status='READY'), 200

@app.get('/metrics')
def metrics(): return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == '__main__': app.run(host='0.0.0.0', port=int(os.getenv('PORT','5000')))