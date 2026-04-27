from flask import Flask, jsonify, render_template_string
from datetime import datetime
import os

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flask в Docker</title>
    <style>
        body { font-family: system-ui, sans-serif; background: #f0f2f5; color: #333; 
               display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .card { background: #fff; padding: 2rem; border-radius: 16px; box-shadow: 0 8px 24px rgba(0,0,0,0.1); 
                text-align: center; max-width: 450px; width: 100%; }
        h1 { margin-top: 0; color: #2c3e50; }
        .time { font-size: 2rem; font-weight: bold; color: #3498db; margin: 1rem 0; }
        .btn { display: inline-block; padding: 10px 20px; background: #3498db; color: #fff; 
               text-decoration: none; border-radius: 8px; margin-top: 1rem; }
        .btn:hover { background: #2980b9; }
    </style>
</head>
<body>
    <div class="card">
        <h1> Python Web App</h1>
        <p>Приложение работает внутри Docker-контейнера</p>
        <div class="time" id="clock">{{ time }}</div>
        <a class="btn" href="/api/status">Проверить API</a>
    </div>
    <script>
        setInterval(async () => {
            const res = await fetch('/api/time');
            const data = await res.json();
            document.getElementById('clock').textContent = data.time;
        }, 1000);
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, time=datetime.now().strftime("%H:%M:%S"))

@app.route('/api/status')
def api_status():
    return jsonify({
        "status": "ok",
        "version": "1.0.0",
        "env": os.environ.get("APP_ENV", "production"),
        "python": os.sys.version.split()[0]
    })

@app.route('/api/time')
def api_time():
    return jsonify({"time": datetime.now().strftime("%H:%M:%S")})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
