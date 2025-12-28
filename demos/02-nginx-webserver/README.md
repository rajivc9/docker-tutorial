# Demo 2: Running a Web Server (Nginx) 🌐

Learn to run a web server and understand port mapping.

## Step 1: Run Nginx Container

```bash
# Run Nginx in detached mode with port mapping
docker run -d -p 8080:80 --name my-nginx nginx
```

### Understanding the command:
- `-d` : Run in detached mode (background)
- `-p 8080:80` : Map host port 8080 to container port 80
- `--name my-nginx` : Give container a name
- `nginx` : Image name

### Port Mapping Visualization:

```
┌─────────────────────────────────────────────────────────────┐
│                      HOST MACHINE                           │
│                                                             │
│   Browser ──► localhost:8080                                │
│                    │                                        │
│                    ▼                                        │
│   ┌─────────────────────────────────────────────────────┐  │
│   │              DOCKER CONTAINER                        │  │
│   │                                                      │  │
│   │   Port 8080 (host) ──mapped to──► Port 80 (nginx)   │  │
│   │                                                      │  │
│   └─────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Step 2: Access the Web Server

Open your browser and go to:
```
http://localhost:8080
```

Or use curl:
```bash
curl http://localhost:8080
```

You should see the Nginx welcome page!

## Step 3: Explore Container

```bash
# Check running containers
docker ps

# View container logs
docker logs my-nginx

# Follow logs in real-time
docker logs -f my-nginx

# Execute commands inside container
docker exec -it my-nginx bash

# Inside container, explore:
ls /usr/share/nginx/html/
cat /etc/nginx/nginx.conf
exit
```

## Step 4: Serve Custom Content

### Method 1: Copy files into container

```bash
# Create a custom HTML file
echo '<h1>Hello from Docker!</h1>' > index.html

# Copy to container
docker cp index.html my-nginx:/usr/share/nginx/html/

# Refresh browser - you'll see your custom page!
```

### Method 2: Mount a volume (Recommended)

```bash
# Stop and remove existing container
docker stop my-nginx
docker rm my-nginx

# Create a directory with your website
mkdir -p ~/my-website
echo '<html>
<head><title>My Docker Site</title></head>
<body>
  <h1>🐳 Welcome to My Docker Website!</h1>
  <p>This is served from a mounted volume.</p>
</body>
</html>' > ~/my-website/index.html

# Run with volume mount
docker run -d \
  -p 8080:80 \
  --name my-nginx \
  -v ~/my-website:/usr/share/nginx/html:ro \
  nginx
```

The `:ro` flag makes the mount read-only for security.

## Step 5: Multiple Port Mappings

```bash
# Stop existing container
docker stop my-nginx
docker rm my-nginx

# Run multiple instances on different ports
docker run -d -p 8081:80 --name nginx-1 nginx
docker run -d -p 8082:80 --name nginx-2 nginx
docker run -d -p 8083:80 --name nginx-3 nginx

# Check all running
docker ps

# Access each:
# http://localhost:8081
# http://localhost:8082
# http://localhost:8083
```

## Step 6: Cleanup

```bash
# Stop all nginx containers
docker stop nginx-1 nginx-2 nginx-3

# Remove all stopped containers
docker container prune

# Or remove specific containers
docker rm nginx-1 nginx-2 nginx-3
```

## Key Takeaways

1. `-d` runs containers in background (detached mode)
2. `-p host:container` maps ports between host and container
3. `docker logs` shows container output
4. `docker exec` runs commands in running containers
5. Volumes (`-v`) mount host directories into containers
6. Multiple containers can run from same image on different ports

## Exercise

1. Run Nginx on port 9000
2. Create a custom HTML page and serve it
3. Check the access logs using `docker logs`

---

Next: [Demo 3 - Building a Custom Python App](../03-python-app/README.md)

