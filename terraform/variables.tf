variable "project_name" {
  description = "Project name for generated metadata"
  type        = string
  default     = "secure-notes-api"
}

variable "environment" {
  description = "Environment label"
  type        = string
  default     = "dev"
}

variable "owner" {
  description = "Owner identifier"
  type        = string
  default     = "junior-devsecops"
}
