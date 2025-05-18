variable "aws_region" {
  description = "AWS region to deploy resources"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Name of the project"
  type        = string
  default     = "euaiact-qa"
}

variable "environment" {
  description = "Environment (e.g., dev, staging, prod)"
  type        = string
  default     = "dev"
}

# Database variables
variable "db_name" {
  description = "Name for the main database"
  type        = string
  default     = "euaiact"
}

variable "db_user" {
  description = "Username for the main database"
  type        = string
  default     = "postgres"
}

variable "db_password" {
  description = "Password for the main database"
  type        = string
  sensitive   = true
}

variable "logs_db_name" {
  description = "Name for the logs database"
  type        = string
  default     = "logs"
}

variable "logs_db_user" {
  description = "Username for the logs database"
  type        = string
  default     = "postgres"
}

variable "logs_db_password" {
  description = "Password for the logs database"
  type        = string
  sensitive   = true
}