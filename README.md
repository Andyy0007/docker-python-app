# Dockerized Flask Application with Kubernetes, CI/CD & Monitoring

A production-style Python Flask REST API demonstrating **containerization, Kubernetes orchestration, PostgreSQL integration, CI/CD automation, configuration management, health checks, and application observability using AppDynamics**.

The project started as a simple Dockerized Flask application and was progressively extended into a Kubernetes-based application stack with automated CI/CD.

---

## Architecture

```text
                         GitHub
                            |
                            | git push
                            v
                    GitHub Actions
                            |
                 +----------+----------+
                 |                     |
                CI                    CD
                 |                     |
          Python validation       Kubernetes
                 |                     |
          Docker image build       +---+---+
                 |                 |       |
          Docker image push      Flask   PostgreSQL
                 |                 |       |
                 +---------------->|       |
                                   |       |
                            AppDynamics    |
                           Python Agent    |
                                   |       |
                                   +---+---+
                                       |
                              Application Observability
```

---

## Tech Stack

### Application

* Python 3.12
* Flask
* PostgreSQL
* REST API

### Containerization

* Docker
* Docker Hub

### Kubernetes

* Kubernetes
* Docker Desktop Kubernetes
* Deployment
* Service
* ConfigMap
* Secret
* Readiness Probe
* Liveness Probe
* Rolling Updates
* ReplicaSets

### CI/CD

* GitHub Actions
* Automated Python validation
* Docker image build
* Docker image push
* Kubernetes deployment automation

### Observability

* AppDynamics Python Agent
* Application performance monitoring
* Application health monitoring
* Request/transaction monitoring
* Error and exception monitoring
* PostgreSQL interaction monitoring

---

# Application Endpoints

## Home

```http
GET /
```

Response:

```text
Hello Docker! 🚀
```

---

## Health

```http
GET /health
```

Response:

```json
{
  "status": "UP"
}
```

---

## Readiness

```http
GET /ready
```

Used by Kubernetes to determine whether the Flask application is ready to receive traffic.

---

## About

```http
GET /about
```

Response:

```text
This app is created by Anadi.
```

---

# Docker

## Build Image

```bash
docker build -t flask-app .
```

## Run Container

```bash
docker run -p 5000:5000 flask-app
```

Application:

```text
http://localhost:5000
```

---

# Docker Hub

The application image is published to Docker Hub.

Repository:

```text
anadi07/flaskapp
```

Images are tagged using Git commit SHA values for CI/CD deployments.

Example:

```text
anadi07/flaskapp:<commit-sha>
```

Using commit SHA tags allows each deployment to reference a specific version of the application instead of relying only on the `latest` tag.

---

# Kubernetes Architecture

The application is deployed to Kubernetes using the following resources:

```text
Kubernetes Cluster
│
├── Flask Deployment
│   └── 2 Flask Pods
│
├── Flask Service
│   └── NodePort 30007
│
├── PostgreSQL Deployment
│   └── 1 PostgreSQL Pod
│
├── PostgreSQL Service
│   └── ClusterIP
│
├── ConfigMap
│   └── Application configuration
│
└── Secret
    └── Database credentials
```

---

# Kubernetes Resources

## Flask Deployment

File:

```text
deployment.yaml
```

The Flask application runs with:

```text
Replicas: 2
Container Port: 5000
```

The two replicas provide basic application availability and allow Kubernetes to perform rolling updates.

---

## PostgreSQL Deployment

File:

```text
postgres-deployment.yaml
```

PostgreSQL runs inside the Kubernetes cluster and is exposed internally through a ClusterIP service.

```text
Flask Pod
    |
    | DB connection
    v
postgres-service
    |
    v
PostgreSQL Pod
```

> Note: PostgreSQL is currently deployed as a Kubernetes Deployment for learning purposes. A production database workload would generally require a StatefulSet and persistent storage.

---

## Services

### Flask Service

File:

```text
service.yaml
```

Type:

```text
NodePort
```

Port:

```text
5000
```

NodePort:

```text
30007
```

### PostgreSQL Service

File:

```text
postgres-service.yaml
```

Type:

```text
ClusterIP
```

Port:

```text
5432
```

The PostgreSQL service is internal to the Kubernetes cluster.

---

# ConfigMap

File:

```text
configmap.yaml
```

The ConfigMap stores non-sensitive application configuration such as:

```text
DB_HOST
DB_NAME
```

ConfigMaps allow configuration to be separated from the container image.

---

# Secret

File:

```text
secret.yaml
```

Database credentials are stored using a Kubernetes Secret rather than directly embedding credentials into the PostgreSQL deployment configuration.

Example keys:

```text
DB_USER
DB_PASSWORD
```

> For a real production environment, Kubernetes Secrets should be combined with stronger secret-management and encryption practices.

---

# Health Checks

The Flask application exposes:

```text
/health
/ready
```

Kubernetes uses the readiness endpoint to determine whether the application is ready to receive traffic.

Example:

```yaml
readinessProbe:
  httpGet:
    path: /ready
    port: 5000
```

This prevents Kubernetes from routing traffic to a Flask pod that is not ready.

PostgreSQL uses `pg_isready` for container health checks.

---

# Rolling Updates

The Flask application uses a Kubernetes Deployment with the default rolling update strategy.

When a new image is deployed, Kubernetes gradually replaces the old pods with new pods.

Example:

```text
Old Version
    |
    +---- Flask Pod
    |
    +---- Flask Pod
    |
    v
Rolling Update
    |
    +---- New Flask Pod
    +---- Old Flask Pod
    |
    v
New Version
    |
    +---- New Flask Pod
    +---- New Flask Pod
```

The rollout can be monitored using:

```bash
kubectl rollout status deployment/flask-app
```

---

# CI/CD Pipeline

GitHub Actions is used to automate the CI/CD process.

Workflow file:

```text
.github/workflows/deploy.yml
```

## CI Stage

The pipeline performs:

```text
Git Push
   |
   v
Checkout Code
   |
   v
Setup Python
   |
   v
Install Dependencies
   |
   v
Python Syntax Check
   |
   v
Docker Login
   |
   v
Docker Build
   |
   v
Docker Push
```

Python syntax validation is performed using:

```bash
python -m py_compile app.py
```

---

# Docker Image Build

The CI pipeline builds the application image using:

```bash
docker build -t anadi07/flaskapp:${{ github.sha }} .
```

The image is then pushed to Docker Hub:

```bash
docker push anadi07/flaskapp:${{ github.sha }}
```

The GitHub commit SHA is used as the image tag.

This provides traceability between:

```text
Git Commit
     |
     v
Docker Image
     |
     v
Kubernetes Deployment
```

---

# CD Stage

The deployment stage is responsible for deploying the application to Kubernetes.

The pipeline performs operations such as:

```bash
kubectl apply -f secret.yaml
kubectl apply -f configmap.yaml
kubectl apply -f postgres-deployment.yaml
kubectl apply -f postgres-service.yaml
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```

The deployment is then verified using:

```bash
kubectl rollout status deployment/flask-app
```

A successful deployment produces:

```text
deployment "flask-app" successfully rolled out
```

---

# Kubernetes Commands

Check all pods:

```bash
kubectl get pods
```

Check deployments:

```bash
kubectl get deployments
```

Check services:

```bash
kubectl get svc
```

Check ReplicaSets:

```bash
kubectl get rs
```

Describe Flask deployment:

```bash
kubectl describe deployment flask-app
```

Check rollout:

```bash
kubectl rollout status deployment flask-app
```

Check deployment image:

```bash
kubectl get deployment flask-app -o=jsonpath="{.spec.template.spec.containers[0].image}"
```

View Flask logs:

```bash
kubectl logs deployment/flask-app
```

---

# AppDynamics Observability

The Flask application has been instrumented using the **AppDynamics Python Agent**.

The agent provides application-level observability in addition to Kubernetes-level monitoring.

```text
Kubernetes
│
├── Pod status
├── Pod restarts
├── Readiness
├── Resource usage
└── Deployment status
        |
        v
Flask Application
        |
        v
AppDynamics Python Agent
        |
        ├── Requests
        ├── Transactions
        ├── Response time
        ├── Errors
        └── Database calls
```

This allows application problems to be investigated beyond simply checking whether a Kubernetes pod is running.

For example:

```text
Kubernetes:
Pod = Running

but

AppDynamics:
Application response time = High
Database call = Slow
```

This demonstrates the difference between **infrastructure health** and **application performance**.

---

# Troubleshooting Examples

The project can be used to practice common Kubernetes failure scenarios.

### Check pod status

```bash
kubectl get pods
```

### Check pod details

```bash
kubectl describe pod <pod-name>
```

### Check application logs

```bash
kubectl logs <pod-name>
```

### Check deployment events

```bash
kubectl describe deployment flask-app
```

### Check service configuration

```bash
kubectl describe service flask-service
```

### Check rollout

```bash
kubectl rollout status deployment/flask-app
```

Common scenarios to investigate include:

* `CrashLoopBackOff`
* `ImagePullBackOff`
* `ErrImagePull`
* failed readiness probe
* failed database connection
* incorrect ConfigMap
* incorrect Secret
* failed rolling update

---

# Project Learning Objectives

This project demonstrates practical knowledge of:

* Python Flask application development
* Docker containerization
* Docker image management
* PostgreSQL integration
* Kubernetes Deployments
* Kubernetes Services
* ReplicaSets
* ConfigMaps
* Secrets
* Readiness and liveness checks
* Rolling deployments
* GitHub Actions
* CI/CD concepts
* Docker Hub
* Kubernetes troubleshooting
* Application observability
* AppDynamics Python Agent

---

# Future Improvements

The following improvements can be added as the project evolves:

* [ ] Ingress and Ingress Controller
* [ ] StatefulSet for PostgreSQL
* [ ] PersistentVolume and PersistentVolumeClaim
* [ ] StorageClass
* [ ] Resource requests and limits
* [ ] Horizontal Pod Autoscaler
* [ ] Helm chart
* [ ] NetworkPolicy
* [ ] RBAC
* [ ] PodDisruptionBudget
* [ ] DaemonSet for node-level monitoring
* [ ] Advanced Kubernetes scheduling
* [ ] Automated rollback
* [ ] Improved secret management
* [ ] Prometheus and Grafana integration
* [ ] Production Kubernetes deployment

---

# Project Status

Current implementation:

```text
Python Flask             ✅
Docker                   ✅
Docker Hub               ✅
PostgreSQL               ✅
Kubernetes               ✅
Deployment               ✅
Services                 ✅
ConfigMap                ✅
Secret                   ✅
Readiness Probe          ✅
Liveness Probe           ✅
Rolling Update            ✅
GitHub Actions CI        ✅
GitHub Actions CD        ✅
AppDynamics Python Agent ✅
```

The project is being developed incrementally to demonstrate practical **DevOps, Kubernetes, CI/CD, and observability skills**.
