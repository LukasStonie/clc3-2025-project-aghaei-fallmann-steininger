# CLC3 Proposal
## Building a Monitor Dashboard for Real-Time Data Visualization

### Team Members 🧑🏻‍💻
- Fatemeh Aghaei (s2410595019)
- Lukas Fallmann (s2410595004)
- Lukas Steininger (s2410595016)

### Project Overview
#### Objective 🎯

> - What is the high level goal of your project?
> - What will you newly build and develop? What does already exist?
> - How does the high level architecture look like? Provide an architecture diagram.
> - How does it relate to cloud computing? What cloud technologies will you use?

##### High Level Goal
Implement a real-time monitoring dashboard for a fictional ticket platform that visualizes network traffic and sales data and produces alerts if problems arise. Monitoring and alerting will be implemented using Prometheus and Grafana.
Stress testing using the Python Locust library will be performed to show the functionality of the monitoring dashboard under high load.

The metrics that are observed are the number of requests, request duration, number of failed requests, CPU usage, and memory usage.
Alerts will be configured to notify the team via email (or Discord) if the number of failed requests exceeds a certain threshold or if the request duration exceeds a certain limit.

In the end, we will have a fully functional monitoring dashboard that can be used to monitor the performance of the ticket platform in real-time and alert the team in case of any issues.
In the presentation, we will demonstrate the functionality of the monitoring dashboard under high load using stress testing.

##### Newly built
Using the Python FastAPI library, multiple API-endpoints will be implemented to create concerts and buy tickets.
To simulate ticket purchases as close to reality as possible, a certain percentage of requests will be denied randomly to simulate failed transactions. 
Requests will take varying amounts of time to process. 
An additional bottleneck will be introduced by adding database to store concerts and ticket purchases.

##### High level architecture
The python FastAPI is executed in a containerized environment. 
A different container running Prometheus will be used to scrape metrics from the FastAPI application and store them. 
A third container running Grafana will be connected to Prometheus to visualize the metrics in a dashboard.
All three containers are deployed in the cloud using kubernetes.
The database that the FastAPI application connects to is also hosted in the cloud.

![architecture.png](/docs/data/architecture.png)
##### Cloud computing relation
Observability and monitoring are crucial aspects of cloud computing, and this project aims to demonstrate how to effectively monitor and visualize application performance.

##### Milestones 🪨

> - Break down the project into milestones, including team internal deadlines.

| **Milestone** 	  | **Description**                                       	                                    | **Deadline** 	 |
|------------------|--------------------------------------------------------------------------------------------|----------------|
| 1             	  | Acceptance of the Proposal                            	                                    | 22.12.2025   	 |
| 2             	  | Implementation of the backend code (FAST-API)                   	                          | 31.12.2025   	 |
| 3             	  | Integration of database                  	                                                 | 9.1.2026     	 |
| 4             	  | Instrumentation of Prometheus and Grafana including alerts and notifications             	 | 16.1.2026    	 |
| 5             	  | Definition of final dashboard metrics and stress test 	                                    | 23.1.2026    	 |
| 6             	  | Documentation (Reproducibility, ...)                  	                                    | 28.1.2026    	 |
| 7                | Final presentation                                                                         | 2.2.2026       |

#### Distribution of Work 🗄️

> - Show us who will work on what parts

FA ... Fatemeh Aghaei\
LF ... Lukas Fallmann\
LS ... Lukas Steininger

| **Work Package** | **Work Package Name** | **Person** | **Key Activities / Description**                                                                                                            | **Deliverables** | **Milestone** | **Deadline** |
|:-----------------| :---|:-----------|:--------------------------------------------------------------------------------------------------------------------------------------------| :--- | :--- | :--- |
| **1**            | **Project Initiation & Planning**|   FA,LF,LS         | • Requirement analysis & scoping<br>• Tech stack selection<br>• Proposal drafting                                                           | Approved Project Proposal | 1 | 22.12.2025 |
| **2**            | **Core Backend Development**|        LS    | • Repo & CI/CD setup<br>• API Endpoint implementation<br>• Business logic (using local DB)                                                  | Functional Backend (Local) | 2 | 31.12.2025 |
| **3**            | **Cloud Infra & Persistence**|        LF    | • Provision Cloud Database<br>• Schema migration & data seeding<br>• Connect backend to Cloud Host                                          | Cloud-Integrated Backend | 3 | 09.01.2026 |
| **4**            | **Observability Setup**|     FA    | • Code instrumentation (Metrics)<br>• Prometheus scraping config<br>• Grafana setup & data source<br>• Definition of Alerts & Notifications | Live Grafana Dashboard | 4 | 16.01.2026 |
| **5**            | **Testing, Validation & Tuning**|     FA       | • Define critical metrics<br>• Execute Stress/Load tests<br>• Finalize dashboard views                                                      | Stress Test Report & Final Dashboard | 5 | 23.01.2026 |
| **6**            | **Documentation & Delivery**|    FA,LF,LS        | • Write technical docs (Reproducibility)<br>• Create presentation slides<br>• Final Pitch                                                   | Technical Docs & Slide Deck | 6, 7 | 02.02.2026 |
