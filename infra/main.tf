terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}


provider "aws" {
  region = "us-east-2"
}



resource "aws_s3_bucket" "brdev_bucket" {
  bucket = "brdev-bucket"

  tags = {
    Name        = "brdev-dl"
    Environment = "Dev"
  }
}