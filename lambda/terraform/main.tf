terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

provider "aws" {
  region = "ap-south-1"
}

# Existing SmartCloud ETL S3 bucket
resource "aws_s3_bucket" "smartcloud_etl" {
  bucket = "smartcloud-etl-gaurav-2026-728035102805-ap-south-1-an"

  lifecycle {
    prevent_destroy = true
  }

  tags = {
    Project     = "SmartCloud-ETL"
    Environment = "Hackathon"
    ManagedBy   = "Terraform"
  }
}

# Keep the S3 bucket private
resource "aws_s3_bucket_public_access_block" "smartcloud_etl" {
  bucket = aws_s3_bucket.smartcloud_etl.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Enable bucket-owner ownership
resource "aws_s3_bucket_ownership_controls" "smartcloud_etl" {
  bucket = aws_s3_bucket.smartcloud_etl.id

  rule {
    object_ownership = "BucketOwnerEnforced"
  }
}

# Existing Lambda function
data "aws_lambda_function" "etl_processor" {
  function_name = "smartcloud-etl-processor"
}

# Existing IAM role used by Lambda
data "aws_iam_role" "lambda_role" {
  name = "smartcloud-etl-processor-role-gbutash9"
}

output "s3_bucket_name" {
  value = aws_s3_bucket.smartcloud_etl.bucket
}

output "lambda_function_name" {
  value = data.aws_lambda_function.etl_processor.function_name
}

output "lambda_role_arn" {
  value = data.aws_iam_role.lambda_role.arn
}
