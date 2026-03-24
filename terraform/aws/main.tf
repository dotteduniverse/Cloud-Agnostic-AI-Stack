provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "rag_bucket" {
  bucket = "my-rag-bucket-${random_id.bucket_suffix.hex}"
}

resource "random_id" "bucket_suffix" {
  byte_length = 4
}

output "bucket_name" {
  value = aws_s3_bucket.rag_bucket.bucket
}