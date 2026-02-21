output "ec2_public_ip" {
  description = "Temporary EC2 public IP"
  value       = aws_instance.telecomm_ec2.public_ip
}

output "elastic_ip" {
  description = "Static Elastic IP (use for domain)"
  value       = aws_eip.telecomm_eip.public_ip
}