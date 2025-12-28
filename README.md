# 🐳 Docker Tutorial for Beginners

A comprehensive hands-on guide to learning Docker on Ubuntu.

## 📚 Table of Contents

1. [What is Docker?](#what-is-docker)
2. [Installation](#installation)
3. [Core Concepts](#core-concepts)
4. [Basic Commands](#basic-commands)
5. [Hands-on Demos](#hands-on-demos)
6. [Best Practices](#best-practices)

---

## What is Docker?

Docker is a platform that enables you to **package, distribute, and run applications** in isolated environments called **containers**.

### Why Docker?

| Problem Without Docker | Solution With Docker |
|------------------------|----------------------|
| "Works on my machine" syndrome | Consistent environment everywhere |
| Complex dependency management | All dependencies packaged together |
| Resource-heavy VMs | Lightweight containers |
| Slow deployment | Fast startup times |

### Docker vs Virtual Machines

```
┌─────────────────────────────────────────────────────────────────┐
│                    VIRTUAL MACHINES                              │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────┐  ┌─────────┐  ┌─────────┐                         │
│  │  App A  │  │  App B  │  │  App C  │                         │
│  ├─────────┤  ├─────────┤  ├─────────┤                         │
│  │Guest OS │  │Guest OS │  │Guest OS │  ← Each VM has full OS  │
│  └─────────┘  └─────────┘  └─────────┘                         │
│  ┌─────────────────────────────────────┐                       │
│  │           Hypervisor                │                       │
│  └─────────────────────────────────────┘                       │
│  ┌─────────────────────────────────────┐                       │
│  │           Host OS                   │                       │
│  └─────────────────────────────────────┘                       │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                      CONTAINERS                                  │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────┐  ┌─────────┐  ┌─────────┐                         │
│  │  App A  │  │  App B  │  │  App C  │                         │
│  └─────────┘  └─────────┘  └─────────┘                         │
│  ┌─────────────────────────────────────┐                       │
│  │         Docker Engine               │  ← Shares Host OS     │
│  └─────────────────────────────────────┘                       │
│  ┌─────────────────────────────────────┐                       │
│  │           Host OS                   │                       │
│  └─────────────────────────────────────┘                       │
└─────────────────────────────────────────────────────────────────┘
```

---

## Installation

### Install Docker on Ubuntu

```bash
# 1. Update package index
sudo apt update

# 2. Install prerequisites
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common

# 3. Add Docker's official GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# 4. Add Docker repository
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 5. Install Docker Engine
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# 6. Add your user to docker group (avoid using sudo)
sudo usermod -aG docker $USER

# 7. Apply group changes (or logout/login)
newgrp docker

# 8. Verify installation
docker --version
docker run hello-world
```

---

## Core Concepts

### 1. Images 📦

An **image** is a read-only template containing instructions for creating a container. Think of it as a **blueprint** or **snapshot**.

```
┌────────────────────────────────────┐
│           Docker Image             │
├────────────────────────────────────┤
│  Layer 4: Application Code         │
│  Layer 3: Dependencies (npm, pip)  │
│  Layer 2: Runtime (Node, Python)   │
│  Layer 1: Base OS (Ubuntu, Alpine) │
└────────────────────────────────────┘
```

### 2. Containers 🚢

A **container** is a running instance of an image. It's isolated, lightweight, and contains everything needed to run the application.

```
Image  ──────►  Container (running)
               Container (running)
               Container (stopped)
```

### 3. Dockerfile 📝

A **Dockerfile** is a text file with instructions to build an image.

```dockerfile
FROM ubuntu:22.04          # Base image
RUN apt update             # Run commands
COPY . /app                # Copy files
WORKDIR /app               # Set working directory
CMD ["./start.sh"]         # Default command
```

### 4. Docker Registry 🏪

A **registry** stores Docker images. Docker Hub is the default public registry.

```
┌─────────────┐     push      ┌─────────────┐
│   Local     │ ────────────► │  Registry   │
│   Machine   │ ◄──────────── │ (Docker Hub)│
└─────────────┘     pull      └─────────────┘
```

### 5. Volumes 💾

**Volumes** persist data beyond container lifecycle.

```
┌─────────────────┐
│   Container     │
│  ┌───────────┐  │
│  │  /app/data│──┼──► Volume (persistent storage)
│  └───────────┘  │
└─────────────────┘
```

### 6. Networks 🌐

Docker **networks** enable containers to communicate with each other.

```
┌─────────────────────────────────────┐
│         Docker Network              │
│  ┌─────────┐      ┌─────────┐      │
│  │  Web    │ ◄──► │   DB    │      │
│  │Container│      │Container│      │
│  └─────────┘      └─────────┘      │
└─────────────────────────────────────┘
```

---

## Basic Commands

### Image Commands

```bash
# List images
docker images

# Pull an image from registry
docker pull nginx

# Build image from Dockerfile
docker build -t myapp:v1 .

# Remove an image
docker rmi nginx

# Remove unused images
docker image prune
```

### Container Commands

```bash
# Run a container
docker run nginx

# Run in detached mode (background)
docker run -d nginx

# Run with port mapping
docker run -d -p 8080:80 nginx

# Run with name
docker run -d --name my-nginx nginx

# Run interactively
docker run -it ubuntu bash

# List running containers
docker ps

# List all containers (including stopped)
docker ps -a

# Stop a container
docker stop my-nginx

# Start a stopped container
docker start my-nginx

# Remove a container
docker rm my-nginx

# Remove all stopped containers
docker container prune

# View container logs
docker logs my-nginx

# Execute command in running container
docker exec -it my-nginx bash
```

### Volume Commands

```bash
# Create a volume
docker volume create mydata

# List volumes
docker volume ls

# Run container with volume
docker run -d -v mydata:/app/data nginx

# Run with bind mount (host directory)
docker run -d -v /host/path:/container/path nginx

# Remove a volume
docker volume rm mydata
```

### Network Commands

```bash
# List networks
docker network ls

# Create a network
docker network create mynetwork

# Run container on specific network
docker run -d --network mynetwork nginx

# Connect container to network
docker network connect mynetwork my-container

# Inspect network
docker network inspect mynetwork
```

---

## Hands-on Demos

See the `demos/` folder for practical examples:

1. **Demo 1**: Hello World - Your first container
2. **Demo 2**: Running a Web Server (Nginx)
3. **Demo 3**: Building a Custom Python App
4. **Demo 4**: Multi-container setup with Docker Compose

---

## Best Practices

### Dockerfile Best Practices

1. **Use specific base image tags** (not `latest`)
   ```dockerfile
   # Good
   FROM python:3.11-slim
   
   # Avoid
   FROM python:latest
   ```

2. **Minimize layers** - Combine RUN commands
   ```dockerfile
   # Good
   RUN apt update && apt install -y curl git && rm -rf /var/lib/apt/lists/*
   
   # Avoid
   RUN apt update
   RUN apt install -y curl
   RUN apt install -y git
   ```

3. **Use .dockerignore** to exclude unnecessary files

4. **Don't run as root**
   ```dockerfile
   RUN useradd -m appuser
   USER appuser
   ```

5. **Use multi-stage builds** for smaller images

### Security Best Practices

- Keep images updated
- Scan images for vulnerabilities
- Use official base images
- Don't store secrets in images
- Use read-only containers when possible

---

## Quick Reference Cheat Sheet

```
┌────────────────────────────────────────────────────────────────┐
│                    DOCKER CHEAT SHEET                          │
├────────────────────────────────────────────────────────────────┤
│ IMAGES                          │ CONTAINERS                   │
│ docker images                   │ docker ps                    │
│ docker pull <image>             │ docker run <image>           │
│ docker build -t <name> .        │ docker stop <container>      │
│ docker rmi <image>              │ docker rm <container>        │
│                                 │ docker logs <container>      │
│                                 │ docker exec -it <c> bash     │
├────────────────────────────────────────────────────────────────┤
│ VOLUMES                         │ NETWORKS                     │
│ docker volume ls                │ docker network ls            │
│ docker volume create <name>     │ docker network create <name> │
│ -v <vol>:/path                  │ --network <name>             │
├────────────────────────────────────────────────────────────────┤
│ CLEANUP                                                        │
│ docker system prune -a          # Remove all unused resources  │
│ docker container prune          # Remove stopped containers    │
│ docker image prune              # Remove dangling images       │
└────────────────────────────────────────────────────────────────┘
```

---

## Next Steps

After completing this tutorial:
1. Learn Docker Compose for multi-container applications
2. Explore Docker Swarm or Kubernetes for orchestration
3. Set up CI/CD pipelines with Docker
4. Learn about container security best practices

Happy Dockering! 🐳

