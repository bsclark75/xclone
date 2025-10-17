terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# ------------------------------------------------------------------------------
# 1️⃣ Bootstrap provider (no assume_role)
# Used only to discover the current AWS account ID dynamically.
# ------------------------------------------------------------------------------
provider "aws" {
  alias  = "bootstrap"
  region = var.aws_region
}

# ------------------------------------------------------------------------------
# 2️⃣ Get current AWS account ID from STS using bootstrap provider
# ------------------------------------------------------------------------------
data "aws_caller_identity" "bootstrap" {
  provider = aws.bootstrap
}

# ------------------------------------------------------------------------------
# 3️⃣ Main provider (assume role using dynamically discovered account ID)
# ------------------------------------------------------------------------------
provider "aws" {
  region = var.aws_region

  assume_role {
    role_arn     = "arn:aws:iam::${data.aws_caller_identity.bootstrap.account_id}:role/TerraformAdmin"
    session_name = "terraform"
  }
}
