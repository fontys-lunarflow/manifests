# Lunarflow manifests

This repository contains the Kubernetes manifests, with which the Lunarflow project can be installed.

### Inventory

| **Component** | **Type**   |
|---------------|------------|
| PostgreSQL    | Supporting |
| pgAdmin       | Supporting |
| RabbitMQ      | Supporting |
| Traefik       | Supporting |
| Content API   | Product    |
| Ticket API    | Product    |
| User API      | Product    |
| Frontend      | Product    |

**Supporting:** Not part of the Lunarflow project but needed for proper functioning.

**Product:** Component part of the Lunarflow project.

### Installation: 01-namespaces.yaml

- Execute `kubectl apply -f 01-namespaces.yaml`

### Installation: 02-lunarflow_config.yaml

- Edit the values to fit the production environment, especially the **lunarflow-config** and **lunarflow-secrets** sections.
- Execute `kubectl apply -f 02-lunarflow_config.yaml`

### Installation: 03-storage.yaml until 11-ingress.yaml

- Execute `kubectl apply -f FILE`

### Post installation

- Ensure the Kubernetes cluster has valid SSL certificates.
