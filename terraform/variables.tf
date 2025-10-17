variable "aws_region" {
  type    = string
  default = "us-east-2"
}

variable "key_name" {
  type = string
}

variable "allowed_ssh_cidr" {
  type    = string
  default = "73.52.11.216/32"
}

variable "instance_type" {
  type    = string
  default = "t3.small"
}

variable "repo_url" {
  type = string
}

variable "repo_branch" {
  type    = string
  default = "main"
}

variable "domain_name" {
  type = string
}

variable "email" {
  type = string
}

variable "mail_server" {
  description = "Mail server hostname"
  type        = string
}

variable "mail_port" {
  description = "Mail server port"
  type        = number
}

variable "mail_use_tls" {
  description = "Whether to use TLS for mail"
  type        = bool
}

variable "mail_username" {
  description = "Mail server username"
  type        = string
}

variable "mail_password" {
  description = "Mail server password"
  type        = string
  sensitive   = true
}

