# SmartCloud-ETL

## Cloud Data Lake and Automated ETL Pipeline using AWS

SmartCloud ETL is an event-driven cloud data pipeline that automatically ingests, validates, transforms, and organizes CSV data using AWS services.

## Problem Statement

Organizations receive data from multiple sources in different formats. Raw data may contain missing values, invalid values, and duplicate records.

Manual data cleaning is time-consuming and error-prone.

Our solution automates this process using a cloud-based ETL pipeline.

## Objectives

- Store raw data securely in the cloud
- Automatically process newly uploaded CSV files
- Validate required fields and data types
- Detect missing, invalid, and duplicate records
- Standardize valid data
- Separate valid and invalid records
- Store processing metadata
- Monitor execution using CloudWatch
- Analyze data using Amazon Athena
- Manage infrastructure using Terraform

## Architecture

```text
CSV File
    |
    v
Amazon S3 - Raw Data
    |
    | ObjectCreated Event
    v
AWS Lambda
    |
    |-- Data Validation
    |-- Data Transformation
    |-- Duplicate Detection
    |
    +-------------+-------------+
    |                           |
    v                           v
Processed Data             Invalid Data
S3/processed/              S3/invalid/
    |                           |
    +-------------+-------------+
                  |
                  v
            Amazon Athena
                  |
                  v
            SQL Analysis
                  |
                  v
             Reporting

AWS Services Used

Service	                     |                Purpose
                             |  
Amazon S3                    |             	Raw, processed, invalid and metadata storage
AWS Lambda	                 |              Serverless ETL processing
IAM	                         |              Secure access control
Amazon CloudWatch	           |              Logs and monitoring
Amazon Athena	               |              SQL-based data analysis
Terraform	                   |              Infrastructure as Code
 

ETL Workflow

1. A CSV file is uploaded to the raw/ folder in Amazon S3.


2. S3 generates an ObjectCreated event.


3. The event automatically triggers AWS Lambda.


4. Lambda reads the CSV file.


5. Required fields and data types are validated.


6. Missing, invalid, and duplicate records are detected.


7. Valid records are standardized and stored in processed/.


8. Invalid records and their reasons are stored in invalid/.


9. Processing metadata is stored in metadata/.


10. CloudWatch stores execution logs.


11. Amazon Athena is used to query the processed and invalid data.



Data Validation

The pipeline checks:
Missing Name
Missing Age
Missing City
Missing Salary
Invalid Age
Invalid Salary
Duplicate records


Example

Neha  -> Missing Age
Vikas -> Invalid Salary
Rohit -> Duplicate Record

Sample Data

A sample CSV file is available at:

sample-data/sample.csv

The sample contains both valid and intentionally invalid records to demonstrate the validation process.

Scalability

The current prototype uses AWS Lambda for event-driven processing of smaller files.

For large-scale datasets, the architecture can be extended using distributed processing services such as AWS Glue or Amazon EMR, with partitioned data stored in Amazon S3.

Security

The S3 bucket is kept private.

Block Public Access is enabled.

Access is controlled using IAM.

No public bucket access is required.


Infrastructure as Code

Terraform configuration is provided in:

terraform/main.tf

Terraform allows the AWS infrastructure to be defined and managed using reusable configuration files.

Project Structure

SmartCloud-ETL/
|
|-- architecture/
|   `-- architecture.md
|
|-- lambda/
|   `-- lambda_function.py
|
|-- sample-data/
|   `-- sample.csv
|
|-- terraform/
|   `-- main.tf
|
`-- README.md

Expected Outcome

The pipeline automatically converts raw CSV data into analysis-ready data while separating invalid records and maintaining processing metadata.

Future Enhancements

AWS Glue for large-scale ETL

Amazon EMR for distributed processing

Advanced dashboard integration

Additional input formats such as JSON

Data quality monitoring and alerts


Project Information

Project: SmartCloud ETL

Problem Statement: PS-06 – Cloud Data Lake and Automated ETL Pipeline

Domain: Cloud Computing

Cloud Provider: Amazon Web Services (AWS)
