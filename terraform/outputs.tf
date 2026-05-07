output "deployment_metadata_file" {
  value       = local_file.deployment_manifest.filename
  description = "Path to generated metadata file"
}
