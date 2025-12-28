from flask import Flask
import os
import socket

app = Flask(__name__)

@app.route('/')
def hello():
    hostname = socket.gethostname()
    return f'''
    <html>
    <head>
        <title>Docker Python Demo</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            }}
            .container {{
                text-align: center;
                padding: 40px;
                background: rgba(255,255,255,0.1);
                border-radius: 20px;
                backdrop-filter: blur(10px);
            }}
            h1 {{ font-size: 3em; margin-bottom: 10px; }}
            .emoji {{ font-size: 4em; }}
            .info {{ margin-top: 20px; opacity: 0.8; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="emoji">🐳</div>
            <h1>Hello from Docker!</h1>
            <p>This Python app is running inside a container.</p>
            <div class="info">
                <p>Container Hostname: <strong>{hostname}</strong></p>
                <p>Python Flask App v1.0</p>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/health')
def health():
    return {'status': 'healthy', 'hostname': socket.gethostname()}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

