# Demo 3: Building a Custom Python App 🐍

Learn to create your own Docker image with a Python application.

## Project Structure

```
03-python-app/
├── app.py              # Python application
├── requirements.txt    # Python dependencies
├── Dockerfile          # Build instructions
└── .dockerignore       # Files to exclude
```

## Step 1: Understand the Application

We have a simple Flask web application that displays a greeting.

### app.py
```python
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
```

## Step 2: Understand the Dockerfile

```dockerfile
# Dockerfile explained line by line

# 1. Base Image - Start with official Python image
FROM python:3.11-slim

# 2. Set working directory inside container
WORKDIR /app

# 3. Copy requirements first (for better caching)
COPY requirements.txt .

# 4. Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy application code
COPY app.py .

# 6. Expose port (documentation)
EXPOSE 5000

# 7. Command to run the application
CMD ["python", "app.py"]
```

### Layer Caching Visualization:

```
┌─────────────────────────────────────────────────────────────┐
│ Build #1 (First time - all layers built)                    │
├─────────────────────────────────────────────────────────────┤
│ Layer 1: FROM python:3.11-slim          [BUILT]             │
│ Layer 2: WORKDIR /app                   [BUILT]             │
│ Layer 3: COPY requirements.txt          [BUILT]             │
│ Layer 4: RUN pip install                [BUILT] ← Slow      │
│ Layer 5: COPY app.py                    [BUILT]             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Build #2 (Only app.py changed)                              │
├─────────────────────────────────────────────────────────────┤
│ Layer 1: FROM python:3.11-slim          [CACHED] ✓          │
│ Layer 2: WORKDIR /app                   [CACHED] ✓          │
│ Layer 3: COPY requirements.txt          [CACHED] ✓          │
│ Layer 4: RUN pip install                [CACHED] ✓ Fast!    │
│ Layer 5: COPY app.py                    [BUILT]  ← Only this│
└─────────────────────────────────────────────────────────────┘
```

## Step 3: Build the Image

```bash
# Navigate to demo directory
cd demos/03-python-app

# Build the image
docker build -t my-python-app:v1 .

# The -t flag tags the image with a name:version
```

### Understanding build output:
```
Step 1/7 : FROM python:3.11-slim
 ---> abc123def456
Step 2/7 : WORKDIR /app
 ---> Running in xyz789...
...
Successfully built abc123def456
Successfully tagged my-python-app:v1
```

## Step 4: Run the Container

```bash
# Run the container
docker run -d -p 5000:5000 --name python-demo my-python-app:v1

# Check it's running
docker ps

# View logs
docker logs python-demo
```

Access in browser: http://localhost:5000

## Step 5: Verify Health Endpoint

```bash
curl http://localhost:5000/health
```

Expected output:
```json
{"hostname":"abc123def456","status":"healthy"}
```

## Step 6: Update and Rebuild

Let's modify the app and rebuild:

```bash
# Edit app.py - change the greeting
# Then rebuild with a new tag
docker build -t my-python-app:v2 .

# Stop old container
docker stop python-demo
docker rm python-demo

# Run new version
docker run -d -p 5000:5000 --name python-demo my-python-app:v2
```

## Step 7: View Image Layers

```bash
# See image history
docker history my-python-app:v1

# Inspect image details
docker inspect my-python-app:v1
```

## Step 8: Push to Docker Hub (Optional)

```bash
# Login to Docker Hub
docker login

# Tag image for Docker Hub
docker tag my-python-app:v1 yourusername/my-python-app:v1

# Push to registry
docker push yourusername/my-python-app:v1
```

## Step 9: Cleanup

```bash
# Stop and remove container
docker stop python-demo
docker rm python-demo

# Remove images
docker rmi my-python-app:v1 my-python-app:v2
```

## Key Takeaways

1. **Dockerfile** defines how to build an image
2. **Layer caching** speeds up rebuilds
3. Copy dependencies before code for better caching
4. Use **slim** base images when possible
5. **Tag images** with versions (not just `latest`)
6. **EXPOSE** is documentation; use `-p` for actual port mapping

## Dockerfile Instructions Reference

| Instruction | Purpose |
|-------------|---------|
| `FROM` | Base image |
| `WORKDIR` | Set working directory |
| `COPY` | Copy files from host |
| `ADD` | Copy + extract archives + URLs |
| `RUN` | Execute commands (build time) |
| `ENV` | Set environment variables |
| `EXPOSE` | Document which ports to expose |
| `CMD` | Default command (runtime) |
| `ENTRYPOINT` | Main executable |

---

Next: [Demo 4 - Multi-container with Docker Compose](../04-docker-compose/README.md)

