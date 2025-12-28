# Demo 1: Hello World - Your First Container 🎉

This demo introduces you to running your first Docker container.

## Step 1: Verify Docker Installation

```bash
docker --version
```

Expected output:
```
Docker version 24.x.x, build xxxxxxx
```

## Step 2: Run Hello World

```bash
docker run hello-world
```

### What happens behind the scenes:

```
┌─────────────────────────────────────────────────────────────────┐
│  1. Docker client contacts Docker daemon                        │
│  2. Daemon checks if 'hello-world' image exists locally         │
│  3. If not found, pulls from Docker Hub                         │
│  4. Daemon creates container from image                         │
│  5. Container runs and outputs message                          │
│  6. Container exits                                             │
└─────────────────────────────────────────────────────────────────┘
```

## Step 3: Explore What Happened

```bash
# See the downloaded image
docker images

# See all containers (including stopped)
docker ps -a
```

## Step 4: Run an Interactive Container

Let's run Ubuntu and interact with it:

```bash
# Run Ubuntu container interactively
docker run -it ubuntu bash
```

Inside the container:
```bash
# Check OS
cat /etc/os-release

# Create a file
echo "Hello from container!" > /tmp/hello.txt
cat /tmp/hello.txt

# Check running processes
ps aux

# Exit the container
exit
```

## Step 5: Understanding Container Lifecycle

```bash
# Run a container with a name
docker run -it --name my-ubuntu ubuntu bash

# Exit with Ctrl+D or type 'exit'

# See stopped container
docker ps -a

# Start the container again
docker start -i my-ubuntu

# Remove the container
docker rm my-ubuntu
```

## Key Takeaways

1. `docker run` creates and starts a container
2. `-it` flags enable interactive terminal
3. Containers are isolated from host system
4. Changes inside container are lost when removed (unless using volumes)
5. Use `docker ps -a` to see all containers

## Exercise

Try running these containers:

```bash
# Run Alpine Linux (very lightweight)
docker run -it alpine sh

# Run a specific Ubuntu version
docker run -it ubuntu:20.04 bash

# Run and automatically remove after exit
docker run -it --rm ubuntu bash
```

---

Next: [Demo 2 - Running a Web Server](../02-nginx-webserver/README.md)

