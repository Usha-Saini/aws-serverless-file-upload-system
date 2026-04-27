# AWS Production-Ready Serverless File Processing System

## 🚀 Overview
This repository contains a high-availability, asynchronous backend system built with **AWS Serverless Application Model (SAM)**. It addresses the core pillars of the AWS Well-Architected Framework: Security, Reliability, and Performance Efficiency.

The system migrates a basic file-upload utility into a robust pipeline featuring **JWT Authentication**, **Queue-based Decoupling**, and **Automated Metadata Persistence**.

---

## 🏗️ Architecture
The system follows a non-blocking, asynchronous pattern to ensure the API remains responsive even during high traffic bursts.



### **The Workflow:**
1.  **Authentication:** Users authenticate via **Amazon Cognito** to obtain a JWT IdToken.
2.  **Traffic Control:** **API Gateway** enforces Rate Limiting (Throttling) and validates the JWT.
3.  **Validation & Ingestion:** The `Uploader Lambda` validates file constraints (type/size) and pushes a message to **Amazon SQS**.
4.  **Async Processing:** The `Processor Lambda` consumes messages from the queue to handle heavy tasks without slowing down the user.
5.  **Persistence:** Metadata (File name, size, user, timestamp) is committed to **Amazon DynamoDB**.
6.  **Fault Tolerance:** Failed executions are routed to a **Dead Letter Queue (DLQ)** for inspection and retry logic.

---

## 🛠️ Tech Stack & Services
* **Infrastructure as Code:** AWS SAM (CloudFormation)
* **Identity Provider:** Amazon Cognito (JWT)
* **Compute:** AWS Lambda (Python 3.9+)
* **Messaging:** Amazon SQS (with Redrive Policy/DLQ)
* **Database:** Amazon DynamoDB (NoSQL)
* **Storage:** Amazon S3
* **Observability:** Amazon CloudWatch (Logs & Alarms)

---

## 🔐 Security & Governance
* **Authentication:** Integrated JWT verification. Only users with a valid Cognito session can interact with the API.
* **Authorization:** IAM roles follow the **Principle of Least Privilege**, granting only the specific permissions needed for S3, SQS, and DynamoDB.
* **Throttling:** API Gateway is configured with rate limits to protect against DDoS and resource exhaustion.

---

## 📊 Monitoring & Reliability
* **Logging:** Centralized execution logs in **CloudWatch Logs** for end-to-end traceability.
* **Alerting:** CloudWatch Alarms configured for **Lambda Errors** and **SQS Backlog** depth.
* **Retry Policy:** SQS is configured with a visibility timeout and a max receive count before moving messages to the **DLQ**.

---

## 🚀 Deployment
This project is fully managed via **AWS SAM**.

```bash
# Build the application
sam build

# Deploy to AWS
sam deploy --guided
```

---

## 📂 Project Structure
```text
.
├── src/
│   ├── uploader.py       # Validates & pushes to SQS
│   └── processor.py      # Processes queue & updates DynamoDB
├── template.yaml         # SAM Infrastructure Template (MANDATORY)
├── docs/                 # Evidence of deployment & JWT decoding
└── postman/              # Exported Postman Collection
```
