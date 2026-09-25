# SmartCloud ETL Architecture

## End-to-End Data Flow

CSV File
   ↓
Amazon S3 - Raw Data
   ↓
S3 ObjectCreated Event
   ↓
AWS Lambda
   ↓
Data Validation & Transformation
   ↓
 ┌─────────────────────┬─────────────────────┐
 ↓                     ↓                     ↓
Processed Data      Invalid Data          Metadata
S3/processed/       S3/invalid/           S3/metadata/
   ↓
Amazon Athena
   ↓
SQL Analysis / Metrics
   ↓
Dashboard / Reporting

## AWS Services Used

- Amazon S3: Cloud storage and data lake
- AWS Lambda: Serverless ETL processing
- IAM: Secure access control
- Amazon CloudWatch: Logs and monitoring
- Amazon Athena: SQL-based data analysis
- Terraform: Infrastructure as Code

## ETL Process

1. User uploads a CSV file into the `raw/` folder.
2. Amazon S3 generates an ObjectCreated event.
3. The event automatically triggers AWS Lambda.
4. Lambda reads and validates the input data.
5. Missing, invalid and duplicate records are identified.
6. Valid records are standardized and stored in `processed/`.
7. Invalid records and their reasons are stored in `invalid/`.
8. Processing metadata is stored in `metadata/`.
9. CloudWatch records execution logs.
10. Athena queries the processed and invalid data for reporting.

## Scalability

The current prototype uses AWS Lambda for event-driven processing of smaller files.

For large-scale datasets, the architecture can be extended with distributed processing services such as AWS Glue or Amazon EMR, with data partitioning in Amazon S3.

## Security

The S3 bucket is private with Block Public Access enabled.

Access is controlled through IAM permissions instead of public access.
