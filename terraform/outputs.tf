output "ec2_public_ip" {
  value = aws_instance.telecomm_ec2.public_ip
}