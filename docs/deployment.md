# Documention for Deployment
This document provides an overview of the deployment process for our application. It covers the necessary steps, tools, and best practices to ensure a smooth and successful deployment.

## Continuous Integration
Once the code is pushed to the main branch of the repository, a Continuous Integration (CI) pipeline is triggered. 
This pipeline includes the following steps:
1. Code Checkout: Retrieves the latest repository content.

2. Version Tagging: Generates a SHORT_SHA (first 7 characters of the commit hash) to provide unique versioning for every build.

3. Docker Setup: Initializes Buildx for extended build capabilities (like multi-platform support).

4. Authentication: Securely logs into Docker Hub using GitHub Secrets (DOCKER_USERNAME and DOCKER_PASSWORD).

5. Build & Optimization: Builds the image using the runtime target of the Dockerfile to keep the final image size small.

6. Push: Uploads the resulting image to Docker Hub with two tags:
- :latest (for the most recent stable version)
- :${SHORT_SHA} (for specific version tracking and rollbacks).

## Continous Deleivery
Open the project in the devcontainer (if not already done), so that all requried dependencies are available.

### Login to Azure
```bash
az login
```
The browser opens up at the first time so you can log into you Microsoft account. After that, press enter in the console.

### Change the subscription (if necessarry)
If the resource group is not yours, and you have only been given access to it, you need to change the subscription. For that execute the following commands:

```bash
az account list --output table
```

```bash
az account set --subscription <SUBSCRIPTION-ID>
```

### Connect to the cluster
Connect to the cluster by providing the resource group name and the cluster name
```bash
az aks get-credentials --resource-group TicketSystemResourceGroup --name TicketWatcher-Cluster
```

### Deletion of config map
If you already deployed the containers before and you just made changes, you need to clear the config maps.

```bash
kubectl delete configmap prometheus-config

kubectl delete configmap grafana-provisioning

kubectl delete configmap grafana-dashboards
```

### Creation of config maps
Once the old config maps are cleared, or in case this is your first time starting, you need to create config maps for the three pods that we want to start:
```bash
# 1. Upload Prometheus Config
kubectl create configmap prometheus-config \
  --from-file=./clc3_project/prometheus/prometheus.yml

# 2. Upload Grafana Provisioning (Datasources)
kubectl create configmap grafana-provisioning \
  --from-file=alerting-rules=./clc3_project/grafana/provisioning/alerting/alert-rules.yml \
  --from-file=contact-points=./clc3_project/grafana/provisioning/alerting/contact-points.yml \
  --from-file=policies=./clc3_project/grafana/provisioning/alerting/policies.yml \
  --from-file=dashboard-provider=./clc3_project/grafana/provisioning/dashboards/dashboard.yml \
  --from-file=prometheus-ds=./clc3_project/grafana/provisioning/datasources/prometheus.yml

# 3. create the Dashboards ConfigMap
kubectl create configmap grafana-dashboards \
  --from-file=app-monitoring.json=./clc3_project/grafana/dashboards/app-monitoring.json
```

### Restarting the pods
Now the pods can be restarted. Since there is no continous deployment, you need to change the tag of the image before restarting. For that locate the `image` section in the web app deployment of the [ticket_app.yml](../ticket_app.yml) and change it to the tag that the github action produced. 

Once you have done this, you need to apply these changes:

```bash
kubectl apply -f ticket_app.yml
```

```bash
kubectl create secret generic db-credentials \
  --from-literal=db-url="postgresql://myadmin:MyComplexPassword123!@db:5432/postgres"
```

```bash
kubectl create secret generic grafana-secrets \
  --from-literal=discord-webhook="https://discord.com/api/webhooks/your-id/your-token"
```

After applying, you can restart the rollouts

```bash
kubectl rollout restart deployment prometheus

kubectl rollout restart deployment grafana

kubectl rollout restart deployment ticket-web
```
### Checking progress
You can check the progress of the rollout by getting all pods. A short status will be depicted.

```bash
kubectl get pods
```

If you want to check out the logs of a specific pod (if, for instance something failed), you can look at them via this command

```bash
kubectl logs -f <POD__NAME> 
```

And if you want to dig even deeper into a pod, you can connect to it interactively:

```bash
kubectl exec -it <POD_NAME> -- bash
```

### Information on the public IP

Since we want to monitor the dashboard, do stress testing with API, ... we need the public facing IPs of the grafana and ticket-web pods. We can get that information the following way:

```bash
kubectl get svc ticket-web
kubectl get svc grafana
```

### Starting and Stopping

```bash
az aks start --name TicketWatcher-Cluster --resource-group TicketSystemResourceGroup
```

```bash
az aks stop --name TicketWatcher-Cluster --resource-group TicketSystemResourceGroup
```



