terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
  # profile 제거 - 환경변수 사용

  default_tags {
    tags = {
      Project     = "seunggil-aws-practice"
      Environment = "practice"
      Owner       = "seunggil"
    }
  }
}