variable "ami_id" {
  description = "Ubuntu 22.04 AMI for ap-south-1"
  type        = string
  default     = "ami-0f5ee92e2d63afc18"
}

variable "instance_type" {
  description = "EC2 instance type (Free Tier)"
  type        = string
  default     = "t3.micro"
}

variable "key_name" {
  description = "EC2 Key Pair name"
  type        = string
  default     = "medicapskey1"
}