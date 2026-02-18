# AI-Driven Serverless Resume Parsing and Job Matching System on AWS

## Overview

The AI-Driven Serverless Resume Parsing and Job Matching System on AWS is a cloud-native, serverless application designed to automate the resume screening and job matching process.

Recruiters often spend significant time manually reviewing resumes and mapping candidates to job roles. This system automates that workflow using AWS serverless services, document AI, and intelligent matching logic.

The entire infrastructure is defined using AWS SAM (Infrastructure as Code), making the solution scalable, reproducible, and production-ready.

---

## What This Project Solves

This system automates:

- Resume uploads through REST APIs  
- Text extraction from resumes using AI  
- Parsing candidate skills and experience  
- Matching candidates to job descriptions  
- Providing analytics via dashboard APIs  

It reduces manual effort and introduces a scalable, event-driven recruitment workflow.

---

## Architecture Overview

This project follows a serverless and event-driven architecture where services are loosely coupled and scale automatically.

### End-to-End Flow
Client → API Gateway → Upload Lambda → Amazon S3
S3 Event → Amazon SQS → Textract Worker Lambda
Processed Text → NLP Parser → Amazon DynamoDB
Dashboard API → Fetch structured data
Job Matcher → Skill Similarity → Ranked Results


### Architectural Decisions

- Fully serverless design  
- Asynchronous processing using SQS  
- Decoupled services for reliability  
- Stateless Lambda functions  
- Infrastructure managed using AWS SAM  
- Cost-efficient, pay-per-use model  

---

## AWS Services Used

### AWS Lambda
Implements backend microservices:
- Upload Resume
- Textract Worker
- NLP Parser
- Job Matcher
- Dashboard API  

Each Lambda function is independent and scalable.

### Amazon API Gateway
- Exposes REST endpoints  
- Routes HTTP requests to Lambda functions  

### Amazon S3
- Stores uploaded resumes  
- Triggers downstream processing events  

### Amazon SQS
- Decouples resume upload from processing  
- Ensures reliable asynchronous execution  

### Amazon DynamoDB
- Stores structured candidate profiles  
- Stores job descriptions  
- Provides low-latency NoSQL queries  

### Amazon Textract
- Extracts text from resume documents  
- Enables automated document processing  

### AWS SAM
- Defines infrastructure as code  
- Enables version-controlled deployments  
- Allows one-command build and deploy  

---

## Project Structure
AI-Driven-Serverless-Resume-Parsing-and-Job-Matching-System-on-AWS/
│
├── template.yaml # Infrastructure as Code
│
├── functions/
│ ├── upload_resume/ # API → S3 → SQS
│ ├── textract_worker/ # SQS → Textract
│ ├── nlp_parser/ # Resume parsing logic
│ ├── job_matcher/ # Matching algorithm
│ └── dashboard/ # Analytics API
│
├── requirements.txt
└── README.md


---

## Lambda Functions Explained

### Upload Resume
- Triggered by API Gateway  
- Uploads resume file to S3  
- Sends message to SQS for processing  

### Textract Worker
- Triggered by SQS  
- Calls Amazon Textract  
- Extracts text from resume files  

### NLP Parser
- Triggered after text extraction  
- Cleans and processes extracted content  
- Identifies:
  - Skills  
  - Experience  
  - Education  
- Stores structured data in DynamoDB  

### Job Matcher
- Retrieves candidate data  
- Compares with job descriptions  
- Applies similarity scoring logic  
- Returns ranked job matches  

### Dashboard API
- Fetches processed data  
- Provides analytics endpoints  

---

## Matching Logic

The matching mechanism includes:

- Skill extraction from resumes  
- Text normalization  
- Similarity scoring (skill overlap or weighted matching)  
- Ranking of best-fit jobs  

Future enhancements may include:

- TF-IDF vectorization  
- Embedding-based similarity  
- Machine learning ranking models  

---

## Security Considerations

This project follows secure cloud development practices:

- IAM roles with least privilege access  
- No hardcoded credentials  
- Infrastructure defined via AWS SAM  
- Decoupled services using SQS  
- Secure S3 configuration  

---

## Deployment Instructions

### Prerequisites

- AWS CLI configured  
- AWS SAM CLI installed  
- Python 3.10+  
- AWS account with required permissions  

---

### Build the Application

```bash
sam build

Skills Demonstrated
Through this project, the following technical skills were demonstrated:
•	Serverless architecture design
•	Event-driven system development
•	Multi-service AWS integration
•	AI-based document processing
•	Infrastructure as Code using AWS SAM
•	Secure cloud-native development
•	Scalable backend engineering

Author
Santhosh Kumar
Master’s Student – Computer Science And Engineering 
Focus Area: Cloud Computing and Machine Learning

