# Building a Monitor Dashboard for Real-Time Data Visualization

## Team Members 🧑🏻‍💻
- Fatemeh Aghaei (s2410595019)
- Lukas Fallmann (s2410595004)
- Lukas Steininger (s2410595016)

## Project Overview
### Objective 🎯

> - What is the high level goal of your project?
> - What will you newly build and develop? What does already exist?
> - How does the high level architecture look like? Provide an architecture diagram.
> - How does it relate to cloud computing? What cloud technologies will you use?

#### High Level Goal
Implement a real-time monitoring dashboard that visualizes network traffic and sales data of a fictional ticket platform using Python FastApi, Grafana and Prometheus. Additional stress testing using the Python Locust library will be performed to show the functionality of the monitoring dashboard under high load.

#### Newly built
Multiple API-endpoints to create concerts and buy tickets, 
To simulate ticket purchases as close to reality as possible, a certain percentage of requests will be denied randomly to simulate failed transactions. and requests will take varying amounts of time to process. An additonal bottle neck will be provided by adding a database to store concerts and ticket purchases.

#### High level architecture
The python FastAPI will be deployed in the google cloud via a kubernetes cluster. Prometheus will be used to scrape metrics from the FastAPI application and store them. Grafana will be connected to Prometheus to visualize the metrics in a dashboard.

#### Cloud computing relation
The project will be deployed in the Google Cloud Platform (GCP) using a Kubernetes cluster. Additonally, managed services for Prometheus and Grafana will be used to simplify the setup and management of these tools. Observability and monitoring are crucial aspects of cloud computing, and this project aims to demonstrate how to effectively monitor and visualize application performance in a cloud environment.

### Milestones 🪨

> - Break down the project into milestones, including team internal deadlines.

### Distribution of Work 🗄️

> - Show us who will work on what parts
