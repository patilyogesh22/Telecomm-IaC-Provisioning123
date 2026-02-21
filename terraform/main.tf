provider "aws" {
  region = "ap-south-1"
}

resource "aws_instance" "telecomm_ec2" {
  ami           = "ami-0f5ee92e2d63afc18" # Ubuntu 22.04 (check region)
  instance_type = "t3.micro"
  key_name      = "medicapskey1"

  user_data = <<-EOF
    #!/bin/bash
    apt update -y
    apt install docker.io -y
    systemctl start docker
    systemctl enable docker

    curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
    install minikube-linux-amd64 /usr/local/bin/minikube

    curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
    install kubectl /usr/local/bin/kubectl
  EOF

  tags = {
    Name = "Telecomm-IaC-EC2"
  }
}