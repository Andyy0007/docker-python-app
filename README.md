# Dockerized Flask Application

A simple Flask REST API containerized using Docker.

## Tech Stack

- Python 3.12
- Flask
- Docker

## Endpoints

### Home

GET /

```
Hello Docker! 🚀
```

### Health

GET /health

```json
{
  "status": "UP"
}
```

### About

GET /about

```
This app is created by Anadi.
```

## Build Image

```bash
docker build -t flask-app .
```

## Run Container

```bash
docker run -p 5000:5000 flask-app
```

Open

```
http://localhost:5000
```