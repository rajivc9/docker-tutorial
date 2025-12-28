# Demo 4: Multi-Container Setup with Docker Compose 🎼

Learn to orchestrate multiple containers with Docker Compose.

## What is Docker Compose?

Docker Compose is a tool for defining and running **multi-container** Docker applications using a YAML file.

```
┌─────────────────────────────────────────────────────────────────┐
│                    WITHOUT DOCKER COMPOSE                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  $ docker network create mynet                                   │
│  $ docker run -d --name db --network mynet postgres              │
│  $ docker run -d --name redis --network mynet redis              │
│  $ docker run -d --name web --network mynet -p 5000:5000 myapp   │
│                                                                  │
│  Managing multiple containers manually is tedious! 😫            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    WITH DOCKER COMPOSE                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  $ docker compose up -d                                          │
│                                                                  │
│  One command to rule them all! 🎉                                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Project Overview

We'll build a **Task Manager** application with:
- **Frontend**: Flask web app
- **Backend**: Redis for data storage

```
┌─────────────────────────────────────────────────────────────────┐
│                     ARCHITECTURE                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   Browser ──► localhost:5000                                     │
│                    │                                             │
│   ┌────────────────▼────────────────┐                           │
│   │         Web Container           │                           │
│   │       (Flask Python App)        │                           │
│   │          Port 5000              │                           │
│   └────────────────┬────────────────┘                           │
│                    │                                             │
│                    │ Internal Network                            │
│                    │                                             │
│   ┌────────────────▼────────────────┐                           │
│   │        Redis Container          │                           │
│   │       (Data Storage)            │                           │
│   │          Port 6379              │                           │
│   └─────────────────────────────────┘                           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Project Structure

```
04-docker-compose/
├── docker-compose.yml    # Compose configuration
├── web/
│   ├── app.py            # Flask application
│   ├── requirements.txt  # Python dependencies
│   ├── Dockerfile        # Web app image
│   └── templates/
│       └── index.html    # HTML template
└── README.md
```

## Step 1: Understand docker-compose.yml

```yaml
version: '3.8'

services:
  # Web application service
  web:
    build: ./web                    # Build from Dockerfile in ./web
    ports:
      - "5000:5000"                 # Map port 5000
    environment:
      - REDIS_HOST=redis            # Environment variable
      - FLASK_ENV=development
    depends_on:
      - redis                       # Start redis first
    volumes:
      - ./web:/app                  # Mount for live reload
    restart: unless-stopped

  # Redis database service
  redis:
    image: redis:7-alpine           # Use official Redis image
    volumes:
      - redis_data:/data            # Persist data
    restart: unless-stopped

# Named volumes
volumes:
  redis_data:
```

### Key Concepts:

| Concept | Description |
|---------|-------------|
| `services` | Define containers to run |
| `build` | Build image from Dockerfile |
| `image` | Use existing image |
| `ports` | Port mapping |
| `environment` | Environment variables |
| `depends_on` | Service dependencies |
| `volumes` | Data persistence |
| `restart` | Restart policy |

## Step 2: Run the Application

```bash
# Navigate to demo directory
cd demos/04-docker-compose

# Start all services
docker compose up -d

# View running services
docker compose ps

# View logs
docker compose logs

# Follow logs for specific service
docker compose logs -f web
```

## Step 3: Access the Application

Open browser: http://localhost:5000

You'll see a task manager where you can:
- Add new tasks
- Mark tasks as complete
- Delete tasks

## Step 4: Explore the Setup

```bash
# List all containers
docker compose ps

# Execute command in web container
docker compose exec web bash

# Check Redis data
docker compose exec redis redis-cli
> KEYS *
> LRANGE tasks 0 -1
> exit

# View network
docker network ls
docker network inspect 04-docker-compose_default
```

## Step 5: Scaling Services

```bash
# Scale web service to 3 instances
# (Note: Would need load balancer for production)
docker compose up -d --scale web=3

# This won't work with fixed port mapping
# For scaling, use dynamic ports or a reverse proxy
```

## Step 6: Common Commands

```bash
# Start services
docker compose up -d

# Stop services
docker compose stop

# Stop and remove containers, networks
docker compose down

# Stop, remove containers, networks, AND volumes
docker compose down -v

# Rebuild images
docker compose build

# Rebuild and start
docker compose up -d --build

# View service logs
docker compose logs [service_name]

# Execute command in service
docker compose exec [service_name] [command]

# List running services
docker compose ps
```

## Step 7: Development Workflow

### Live Reload with Volumes

The `volumes` mount enables live code changes:

```yaml
volumes:
  - ./web:/app    # Changes to ./web reflect immediately
```

Try editing `web/app.py` and refresh the browser!

### Environment-Specific Configs

```bash
# Development
docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d

# Production
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

## Step 8: Cleanup

```bash
# Stop and remove everything
docker compose down

# Also remove volumes (data)
docker compose down -v

# Remove built images too
docker compose down --rmi all
```

## Key Takeaways

1. **Docker Compose** simplifies multi-container management
2. **Services** communicate via container names (DNS)
3. **depends_on** controls startup order
4. **Volumes** persist data beyond container lifecycle
5. **Environment variables** configure services
6. Single `docker compose up` starts everything!

## docker-compose.yml Reference

```yaml
version: '3.8'

services:
  service_name:
    # Image options (choose one)
    image: nginx:latest              # Use existing image
    build: ./path                    # Build from Dockerfile
    build:                           # Advanced build
      context: ./path
      dockerfile: Dockerfile.dev
      args:
        - BUILD_ARG=value
    
    # Container settings
    container_name: my-container     # Custom name
    hostname: myhost                 # Container hostname
    restart: unless-stopped          # Restart policy
    
    # Networking
    ports:
      - "8080:80"                    # host:container
    expose:
      - "3000"                       # Internal only
    networks:
      - frontend
      - backend
    
    # Environment
    environment:
      - KEY=value
    env_file:
      - .env
    
    # Storage
    volumes:
      - ./host/path:/container/path  # Bind mount
      - named_volume:/data           # Named volume
    
    # Dependencies
    depends_on:
      - db
      - redis
    
    # Resources (optional)
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M

volumes:
  named_volume:

networks:
  frontend:
  backend:
```

---

## Exercise

1. Add a PostgreSQL database service
2. Configure the web app to use PostgreSQL
3. Add a health check to the web service
4. Create a `.env` file for configuration

---

🎉 **Congratulations!** You've completed the Docker tutorial!

## What's Next?

- Learn Docker Swarm for clustering
- Explore Kubernetes for advanced orchestration
- Set up CI/CD pipelines with Docker
- Study container security best practices

