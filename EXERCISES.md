# 🏋️ Docker Exercises

Practice exercises to reinforce your Docker knowledge.

---

## Exercise 1: Basic Container Operations

### Task
1. Pull the `alpine` image
2. Run an Alpine container interactively
3. Inside the container, create a file `/tmp/hello.txt` with content "Hello Docker!"
4. Exit the container
5. Start the same container again and verify the file exists
6. Create a new Alpine container and verify the file does NOT exist (containers are isolated)

### Commands to try
```bash
docker pull alpine
docker run -it --name my-alpine alpine sh
# Inside: echo "Hello Docker!" > /tmp/hello.txt
# Inside: cat /tmp/hello.txt
# Inside: exit
docker start -i my-alpine
# Inside: cat /tmp/hello.txt
# Inside: exit
docker run -it --rm alpine sh
# Inside: cat /tmp/hello.txt  # Should fail!
```

### Learning Point
Each container has its own filesystem. Data is lost when the container is removed unless you use volumes.

---

## Exercise 2: Port Mapping

### Task
1. Run three Nginx containers on ports 8081, 8082, and 8083
2. Verify all three are accessible via browser or curl
3. Check which containers are running
4. Stop only the container on port 8082
5. Clean up all containers

### Expected Commands
```bash
docker run -d -p 8081:80 --name nginx1 nginx
docker run -d -p 8082:80 --name nginx2 nginx
docker run -d -p 8083:80 --name nginx3 nginx

curl http://localhost:8081
curl http://localhost:8082
curl http://localhost:8083

docker ps
docker stop nginx2
docker ps

docker stop nginx1 nginx3
docker rm nginx1 nginx2 nginx3
```

---

## Exercise 3: Volume Persistence

### Task
1. Create a named volume called `mydata`
2. Run an Alpine container with this volume mounted at `/data`
3. Create a file in `/data` inside the container
4. Exit and remove the container
5. Run a NEW container with the same volume
6. Verify the file still exists!

### Expected Commands
```bash
docker volume create mydata
docker run -it --name test1 -v mydata:/data alpine sh
# Inside: echo "Persistent data!" > /data/test.txt
# Inside: exit

docker rm test1

docker run -it --rm -v mydata:/data alpine sh
# Inside: cat /data/test.txt  # Should show "Persistent data!"
# Inside: exit

docker volume rm mydata
```

---

## Exercise 4: Build Your Own Image

### Task
Create a Docker image for a simple Python script that prints system information.

1. Create a directory `exercise4`
2. Create `info.py`:
```python
import platform
import os

print("=" * 50)
print("🐳 Docker Container System Info")
print("=" * 50)
print(f"Hostname: {platform.node()}")
print(f"OS: {platform.system()} {platform.release()}")
print(f"Python: {platform.python_version()}")
print(f"Architecture: {platform.machine()}")
print(f"User: {os.getenv('USER', 'unknown')}")
print("=" * 50)
```

3. Create a `Dockerfile`:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY info.py .
CMD ["python", "info.py"]
```

4. Build the image with tag `sysinfo:v1`
5. Run the container

### Expected Commands
```bash
mkdir exercise4 && cd exercise4
# Create info.py and Dockerfile as above
docker build -t sysinfo:v1 .
docker run --rm sysinfo:v1
```

---

## Exercise 5: Environment Variables

### Task
Modify the sysinfo image to accept a custom greeting via environment variable.

1. Update `info.py`:
```python
import platform
import os

greeting = os.getenv('GREETING', 'Hello')
name = os.getenv('NAME', 'Docker User')

print(f"{greeting}, {name}!")
print(f"Running on: {platform.node()}")
```

2. Rebuild as `sysinfo:v2`
3. Run with custom environment variables

### Expected Commands
```bash
docker build -t sysinfo:v2 .
docker run --rm sysinfo:v2
docker run --rm -e GREETING="Welcome" -e NAME="DevOps Engineer" sysinfo:v2
```

---

## Exercise 6: Multi-Container Networking

### Task
Set up two containers that can communicate with each other.

1. Create a custom network called `mynetwork`
2. Run a Redis container on this network
3. Run an Alpine container on the same network
4. From Alpine, ping the Redis container by name
5. From Alpine, connect to Redis using `redis-cli`

### Expected Commands
```bash
docker network create mynetwork

docker run -d --name myredis --network mynetwork redis:alpine

docker run -it --rm --network mynetwork alpine sh
# Inside: ping myredis -c 3
# Inside: apk add redis
# Inside: redis-cli -h myredis ping
# Inside: exit

docker stop myredis
docker rm myredis
docker network rm mynetwork
```

---

## Exercise 7: Docker Compose

### Task
Create a simple guestbook application with Docker Compose.

1. Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  web:
    image: nginx:alpine
    ports:
      - "8080:80"
    volumes:
      - ./html:/usr/share/nginx/html:ro
    depends_on:
      - api

  api:
    image: python:3.11-slim
    working_dir: /app
    volumes:
      - ./api:/app
    command: python -m http.server 8000
    expose:
      - "8000"
```

2. Create `html/index.html`:
```html
<!DOCTYPE html>
<html>
<head><title>Guestbook</title></head>
<body>
    <h1>Welcome to the Guestbook!</h1>
    <p>This is served by Nginx in a Docker container.</p>
</body>
</html>
```

3. Create `api/` directory (can be empty for now)

4. Start with `docker compose up -d`
5. Access http://localhost:8080
6. View logs with `docker compose logs`
7. Clean up with `docker compose down`

---

## Exercise 8: Dockerfile Best Practices

### Task
Optimize this Dockerfile:

**Before (inefficient):**
```dockerfile
FROM ubuntu:latest
RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
COPY . /app
WORKDIR /app
RUN pip3 install flask
RUN pip3 install redis
CMD python3 app.py
```

**After (optimized):**
```dockerfile
# Use specific, slim base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy only requirements first (layer caching)
COPY requirements.txt .

# Install dependencies in single layer, clean cache
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Don't run as root
RUN useradd -m appuser
USER appuser

# Document the port
EXPOSE 5000

# Use exec form for CMD
CMD ["python", "app.py"]
```

### Learning Points
- Use specific image tags (not `latest`)
- Use slim/alpine base images
- Combine RUN commands to reduce layers
- Copy dependencies before code for caching
- Clean up in the same layer
- Don't run as root
- Use exec form for CMD

---

## Exercise 9: Debugging Containers

### Task
Practice debugging a failing container.

1. Create a container that exits immediately:
```bash
docker run -d --name failing alpine echo "I will exit"
```

2. Check why it stopped:
```bash
docker ps -a
docker logs failing
docker inspect failing | grep -A 5 "State"
```

3. Run a container that keeps running:
```bash
docker run -d --name running alpine sleep infinity
docker exec -it running sh
```

4. Debug a container that won't start:
```bash
docker run -d --name broken alpine nonexistent-command
docker logs broken
```

---

## Exercise 10: Complete Application

### Final Challenge
Build a complete voting application with:
- Frontend (Nginx serving static files)
- Backend API (Python Flask)
- Database (Redis)
- All connected via Docker Compose

**Requirements:**
1. Users can vote for "Cats" or "Dogs"
2. Votes are stored in Redis
3. Results are displayed on the page
4. Use proper networking between services
5. Data persists across restarts (use volumes)

**Hints:**
- Frontend sends votes to backend API
- Backend stores votes in Redis
- Use `depends_on` for service ordering
- Mount volumes for Redis persistence

---

## 🎯 Self-Assessment Checklist

After completing these exercises, you should be able to:

- [ ] Pull and run Docker images
- [ ] Understand container lifecycle (create, start, stop, remove)
- [ ] Map ports between host and container
- [ ] Use volumes for data persistence
- [ ] Build custom images with Dockerfile
- [ ] Use environment variables
- [ ] Create and use Docker networks
- [ ] Write docker-compose.yml files
- [ ] Debug container issues
- [ ] Follow Dockerfile best practices

---

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Hub](https://hub.docker.com/)
- [Play with Docker](https://labs.play-with-docker.com/) - Free online Docker playground
- [Docker Samples](https://github.com/docker/awesome-compose)

Happy Learning! 🐳

