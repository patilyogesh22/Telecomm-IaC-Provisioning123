provider "aws" {
  region = var.aws_region
}

resource "aws_security_group" "telecomm_sg" {
  ingress {
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "telecomm_ec2" {
  ami                    = var.ami_id
  instance_type          = "t3.micro"
  key_name               = var.key_name
  vpc_security_group_ids = [aws_security_group.telecomm_sg.id]

  user_data = <<-EOF
              #!/bin/bash
              apt update
              apt install docker.io git -y
              systemctl start docker
              systemctl enable docker

              git clone ${var.github_repo}
              cd telecomm-iac-project

              docker build -t telecomm-app .
              docker run -d -p 5000:5000 telecomm-app
              EOF

  tags = {
    Name = "Telecomm-IaC-EC2"
  }
}
