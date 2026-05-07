terraform {
  required_version = ">= 1.5.0"
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.5"
    }
    null = {
      source  = "hashicorp/null"
      version = "~> 3.2"
    }
  }
}

provider "local" {}
provider "null" {}

resource "local_file" "deployment_manifest" {
  filename = "${path.module}/build/deployment-info.txt"
  content  = <<EOT
project=${var.project_name}
environment=${var.environment}
owner=${var.owner}
EOT
}

resource "null_resource" "security_gate_example" {
  triggers = {
    project = var.project_name
    env     = var.environment
  }

  provisioner "local-exec" {
    command = "echo Security gate check for ${var.project_name} in ${var.environment}"
  }
}
