# aws-serverless-crud-api
POC - Serverless CRUD API using API Gateway, Lambda, DynamoDB
# AWS Serverless CRUD API (POC 01)

This project is a **serverless CRUD API** built on AWS using:

- **API Gateway (REST API)**
- **AWS Lambda (Python)**
- **Amazon DynamoDB**
- **IAM Roles**
- **Postman Web** for testing

It demonstrates how to build a simple, scalable backend without managing servers.

---

## Architecture

**Flow:**

`Client (Postman) → API Gateway → Lambda → DynamoDB → back to client`

**Services used:**

- **API Gateway** – exposes REST endpoints
- **Lambda** – contains Python business logic
- **DynamoDB** – NoSQL database to store items
- **IAM** – grants Lambda access to DynamoDB & CloudWatch
- **CloudWatch** – used for debugging and logs

---

## Endpoints

Assuming base URL:
https://{api-id}.execute-api.{region}.amazonaws.com/Dev

