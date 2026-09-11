# DevOps Production Project — Flask + PostgreSQL on AWS EKS

End-to-end DevOps portfolio project covering GitHub, Docker, Terraform, Ansible, AWS EC2, Amazon EKS, Helm, Prometheus/Grafana, GitHub Actions, Jenkins and Linux operations.

Architecture: Developer → GitHub → CI/CD → Docker Hub → AWS EKS → Helm → Flask → Prometheus → Grafana.

Terraform provisions VPC/EKS; Ansible configures EC2; Helm deploys Kubernetes workloads; Prometheus scrapes `/metrics`.

Local: `docker compose up --build`

EKS: `aws eks update-kubeconfig --region ap-south-1 --name devops-eks` then `helm upgrade --install flask-app ./helm/flask-app --namespace flask-app --create-namespace --set image.repository=anadi07/flaskapp --set image.tag=latest`.

For production, use GitHub OIDC, AWS Secrets Manager, image digests, private networking, remote Terraform state and security scanning.