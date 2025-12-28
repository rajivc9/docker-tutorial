# 🐳 Docker Cheat Sheet

Quick reference for common Docker commands.

---

## 📦 Images

```bash
# List all images
docker images
docker image ls

# Pull image from registry
docker pull nginx
docker pull nginx:1.25-alpine    # Specific version

# Build image from Dockerfile
docker build -t myapp:v1 .
docker build -t myapp:v1 -f Dockerfile.dev .   # Custom Dockerfile

# Tag an image
docker tag myapp:v1 myrepo/myapp:v1

# Push to registry
docker push myrepo/myapp:v1

# Remove image
docker rmi nginx
docker rmi -f nginx              # Force remove

# Remove unused images
docker image prune
docker image prune -a            # Remove all unused

# Inspect image
docker inspect nginx
docker history nginx             # Show layers
```

---

## 🚢 Containers

```bash
# Run container
docker run nginx
docker run -d nginx                              # Detached (background)
docker run -it ubuntu bash                       # Interactive terminal
docker run --rm nginx                            # Remove after exit
docker run --name my-nginx nginx                 # Custom name
docker run -p 8080:80 nginx                      # Port mapping
docker run -e MY_VAR=value nginx                 # Environment variable
docker run -v /host/path:/container/path nginx   # Volume mount
docker run --network mynet nginx                 # Specific network

# List containers
docker ps                        # Running only
docker ps -a                     # All containers
docker ps -q                     # Only IDs

# Container lifecycle
docker start my-nginx
docker stop my-nginx
docker restart my-nginx
docker pause my-nginx
docker unpause my-nginx

# Remove container
docker rm my-nginx
docker rm -f my-nginx            # Force remove running

# Container logs
docker logs my-nginx
docker logs -f my-nginx          # Follow logs
docker logs --tail 100 my-nginx  # Last 100 lines

# Execute in container
docker exec -it my-nginx bash
docker exec my-nginx ls /etc

# Copy files
docker cp file.txt my-nginx:/app/
docker cp my-nginx:/app/file.txt ./

# Inspect container
docker inspect my-nginx
docker stats                     # Live resource usage
docker top my-nginx              # Running processes
```

---

## 💾 Volumes

```bash
# Create volume
docker volume create mydata

# List volumes
docker volume ls

# Inspect volume
docker volume inspect mydata

# Remove volume
docker volume rm mydata

# Remove unused volumes
docker volume prune

# Mount volume to container
docker run -v mydata:/app/data nginx

# Bind mount (host directory)
docker run -v /host/path:/container/path nginx
docker run -v $(pwd):/app nginx                  # Current directory

# Read-only mount
docker run -v /host/path:/container/path:ro nginx
```

---

## 🌐 Networks

```bash
# List networks
docker network ls

# Create network
docker network create mynet
docker network create --driver bridge mynet

# Connect container to network
docker network connect mynet my-nginx

# Disconnect from network
docker network disconnect mynet my-nginx

# Inspect network
docker network inspect mynet

# Remove network
docker network rm mynet

# Run container on network
docker run --network mynet nginx
```

---

## 🎼 Docker Compose

```bash
# Start services
docker compose up
docker compose up -d             # Detached
docker compose up --build        # Rebuild images

# Stop services
docker compose stop

# Stop and remove
docker compose down
docker compose down -v           # Also remove volumes
docker compose down --rmi all    # Also remove images

# View status
docker compose ps
docker compose logs
docker compose logs -f web       # Follow specific service

# Execute in service
docker compose exec web bash

# Scale service
docker compose up -d --scale web=3

# Build images
docker compose build

# Pull images
docker compose pull
```

---

## 🧹 Cleanup

```bash
# Remove stopped containers
docker container prune

# Remove unused images
docker image prune
docker image prune -a            # All unused images

# Remove unused volumes
docker volume prune

# Remove unused networks
docker network prune

# Remove everything unused
docker system prune
docker system prune -a           # Including unused images
docker system prune --volumes    # Including volumes

# Disk usage
docker system df
```

---

## 📝 Dockerfile Reference

```dockerfile
# Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV APP_ENV=production
ENV PORT=8080

# Install system packages
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy files
COPY requirements.txt .
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create non-root user
RUN useradd -m appuser
USER appuser

# Expose port (documentation)
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s \
  CMD curl -f http://localhost:8080/health || exit 1

# Default command
CMD ["python", "app.py"]

# Or use ENTRYPOINT for fixed executable
ENTRYPOINT ["python"]
CMD ["app.py"]
```

---

## 🔧 docker-compose.yml Reference

```yaml
version: '3.8'

services:
  web:
    build: ./web
    # OR
    image: nginx:latest
    
    container_name: my-web
    hostname: web-server
    
    ports:
      - "8080:80"
    
    environment:
      - NODE_ENV=production
    env_file:
      - .env
    
    volumes:
      - ./app:/app
      - data_volume:/data
    
    networks:
      - frontend
      - backend
    
    depends_on:
      - db
      - redis
    
    restart: unless-stopped
    
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost"]
      interval: 30s
      timeout: 10s
      retries: 3

  db:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: secret
    volumes:
      - db_data:/var/lib/postgresql/data

volumes:
  data_volume:
  db_data:

networks:
  frontend:
  backend:
```

---

## 🚀 Common Patterns

### Development Setup
```bash
# Live reload with volume mount
docker run -d -p 3000:3000 -v $(pwd):/app myapp
```

### Database with Persistence
```bash
docker run -d \
  --name postgres \
  -e POSTGRES_PASSWORD=secret \
  -v pgdata:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:15
```

### Multi-stage Build
```dockerfile
# Build stage
FROM node:18 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
```

---

## 📊 Useful Flags Summary

| Flag | Description |
|------|-------------|
| `-d` | Detached mode (background) |
| `-it` | Interactive terminal |
| `-p host:container` | Port mapping |
| `-v host:container` | Volume mount |
| `-e KEY=value` | Environment variable |
| `--name` | Container name |
| `--rm` | Remove after exit |
| `--network` | Connect to network |
| `-f` | Force / specify file |

---

Happy Dockering! 🐳

