output "vpc_id" {
  description = "VPC ID"
  value       = aws_vpc.main.id
}

output "vpc_cidr_block" {
  description = "VPC CIDR block"
  value       = aws_vpc.main.cidr_block
}

output "region" {
  description = "AWS region"
  value       = var.aws_region
}

output "internet_gateway_id" {
  description = "Internet Gateway ID"
  value       = aws_internet_gateway.main.id
}

output "public_subnet_id" {
  description = "Public subnet ID"
  value       = aws_subnet.public.id
}

output "private_subnet_ids" {
  description = "Private subnet IDs"
  value       = aws_subnet.private[*].id
}

output "nat_gateway_id" {
  description = "NAT Gateway ID"
  value       = aws_nat_gateway.main.id
}

output "ec2_instance_id" {
  description = "EC2 instance ID"
  value       = aws_instance.mysql_server.id
}

output "ec2_private_ip" {
  description = "EC2 private IP"
  value       = aws_instance.mysql_server.private_ip
}

output "security_group_id" {
  description = "Security group ID for EC2"
  value       = aws_security_group.ec2_mysql.id
}