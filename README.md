# Microservices Monitoring Solution

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Monitoring and Management](#monitoring-and-management)
  - [Deployment strategy](#deployment-strategy)
- [Contributing](#contributing)

## Overview

This project is a microservices monitoring solution designed to ensure the smooth operation, uptime, security, and performance of a set of microservices within a SaaS platform. It consists of several components, each serving a specific purpose:

- **PondPulse**: A stateless application that generates increnemted application version and exposes metadata for the microservices. the scheme is built as the following
  ```bash
  {
  "Frog1": {
    "state": "slow",
    "version": 20 ## will change on each get request
  }
  ```
- **FlyTrap**: A service that detects performance and security issues in the microservices and communicates with PondPulse to modify their state to ['insecure', 'slow', 'healthy'].

- **DBRibbit**: A component that periodically polls PondPulse and persists faulty versions to a MongoDB database.

- **MongoDB & Mongo express**: MongoDB which is a cloud native `Nosql` `DocumentDB` `Database`, and `Mongo Express` which is an interactive lightweight Web-Based Administrative Tool to effectively manage MongoDB Databases.


## Architecture
![Screenshot](images/Architecture.png)


## Getting Started

### Prerequisites

Before you begin, ensure you have met the following requirements:

- A Kubernetes cluster set up (for deploying with Helm)
-  `kubectl` [installed](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
- Helm [installed](https://helm.sh/docs/intro/install/) (for deploying with Helm)
- Git [Installed](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

### Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/your-username/microservices-monitoring.git
   cd microservices-monitoring

2. **Running the Microservices**

   ```bash
   helm install frog-chart ./deploy

### Monitoring and Management
- PondPulse: Access PondPulse's CRUD REST APIs to retrieve information about the microservices. For example:
```bash
curl http://node-ip:30001/microservices
```

- FlyTrap: FlyTrap automatically detects performance and security issues and communicates with PondPulse to modify the state of the microservices. You can check the logs of the pod running flytrap to see if it detected any issue with one of the microservices - the interval for checking for errors is 60 seconds.
```bash
kubectl logs -f -l app flytrap
```

- BRibbit: DBRibbit polls PondPulse periodically and persists faulty versions to a MongoDB database. You can check the logs of the pod running dbribbit to see if it updated some document in the DB.
```bash
kubectl logs -f -l app=dbribbit
```

- MongoDB & Mongo express: To insure data persistency - I chose MongoDB which is a cloud native `Nosql` `DocumentDB` `Database`, and i paired it with an instance of `Mongo Express` which is an interactive lightweight Web-Based Administrative Tool to effectively manage MongoDB Databases.

  
### Deployment Strategy
For the deployment - I decided to implement the `Helm` subchart strategy in which you can manage and deploy multiple dependent charts within a single `helm chart` - where you can deploy them as a single unit.
```bash
.
├── charts
│   ├── microservices
│   │   ├── Chart.yaml
│   │   ├── templates
│   │   │   ├── dbribbit-deployment.yaml
│   │   │   ├── flytrap-deployment.yaml
│   │   │   ├── pondpulse-deployment.yaml
│   │   │   └── pondpulse-service.yaml
│   │   └── values.yaml
│   └── mongo-app
│       ├── Chart.yaml
│       ├── templates
│       │   ├── 01-mongoDB-secret.yaml
│       │   ├── 02-mongoDB-deployment.yaml
│       │   ├── 03-mongoDB-service.yaml
│       │   ├── 04-mongoDB-configmap.yaml
│       │   ├── 05-mongo-exp-deployment.yaml
│       │   └── 06-mongo-exp-service.yaml
│       └── values.yaml
├── Chart.yaml
├── template.yaml
└── values.yaml
```

### Notes
* Considering the fact that there is time between the creation of resources and when Microservices are up and running (due to the time is takes to pull the container images), I have decided to implement an `InitContainer` for both `flytrap` and `DBribbit` microservices. The reason for that is because they are dependent on the `pondpulse` microservice, and its better for them to run only when `pondpulse` is up and running.
That way, the application starts to run right away when all pods are fully available.
 
### Contributing
Contributions are welcome! If you'd like to contribute to this project, please fork the repository and create a pull request.

Source code is located under the src directory and each microservice has its own Dockerfile respectively
