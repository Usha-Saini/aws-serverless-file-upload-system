# AWS Production Ready Serverless File Upload System

## Overview

This project is an upgraded serverless backend system built using AWS services. It allows users to securely upload files using an API. Files are authenticated using JWT tokens, validated, stored in Amazon S3, processed asynchronously using AWS Lambda and Amazon SQS, and metadata is stored in DynamoDB.

This upgraded version focuses on security, scalability, reliability, and monitoring.

---

## Services Used

API Gateway  
AWS Lambda  
Amazon S3  
DynamoDB  
Amazon SQS  
Dead Letter Queue (DLQ)  
Amazon Cognito  
CloudWatch  
AWS SAM  

---

## Architecture Diagram

Architecture

---

## Working Flow

User sends a POST request using API Gateway with JWT token  
API Gateway validates token using Cognito  
Rate limiting is applied on API requests  
API Gateway triggers Upload Lambda  
Lambda validates file type and size  
Lambda uploads file to S3  
Lambda stores metadata in DynamoDB  
Lambda sends message to SQS queue  
Processor Lambda reads message from SQS  
File is processed asynchronously  
If processing fails, message goes to DLQ after retries  
Logs and metrics are stored in CloudWatch  

---

## Environment Variables

Environment Variables

BUCKET_NAME: my-file-upload-bucket-system  
TABLE_NAME: FileMetadatafix  
QUEUE_URL: file-processing-queue  
MAX_FILE_SIZE: 5242880  
USER_POOL_ID: ap-south-1_xxxxx  

---

## API Testing (Postman)

POST Request URL: https://your-api-url.amazonaws.com/prod/upload

Headers:

Authorization: Bearer JWT_TOKEN

Security

IAM role is configured with least privilege access:

S3: PutObject
DynamoDB: PutItem / UpdateItem
SQS: SendMessage / ReceiveMessage
CloudWatch: Logs Write Access
JWT Authentication Enabled
API Rate Limiting Enabled
Monitoring & Reliability

CloudWatch Alarms configured for:

Lambda Errors
API Failures
Queue Backlog
DLQ Messages

SQS Retry mechanism improves fault tolerance.
Infrastructure as Code

Deployment is managed using AWS SAM.
Conclusion

This project demonstrates a production-ready, secure, and scalable serverless architecture using AWS. It includes authentication, asynchronous processing, retry handling, monitoring, and Infrastructure as Code for real-world deployments.
