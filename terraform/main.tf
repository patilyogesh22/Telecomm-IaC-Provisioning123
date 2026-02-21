resource "aws_instance" "telecomm_ec2" {
  ami           = var.ami_id
  instance_type = var.instance_type
  key_name      = var.key_name

  user_data = <<-EOF
    #!/bin/bash
    apt update -y
    apt install docker.io -y
    systemctl start docker
    systemctl enable docker
    usermod -aG docker ubuntu
  EOF

  tags = {
    Name = "Telecomm-IaC-EC2"
  }
}

resource "aws_eip" "telecomm_eip" {
  instance = aws_instance.telecomm_ec2.id
  domain   = "vpc"

  tags = {
    Name = "Telecomm-IaC-EIP"
  }
}