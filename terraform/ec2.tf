# Get the latest Ubuntu 22.04 LTS (Jammy) AMI
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }
}

# Launch EC2 instance for the app
resource "aws_instance" "app" {
  ami                         = data.aws_ami.ubuntu.id
  instance_type               = var.instance_type
  subnet_id                   = data.aws_subnets.default.ids[0]
  vpc_security_group_ids      = [aws_security_group.app.id]
  key_name                    = var.key_name
  iam_instance_profile        = aws_iam_instance_profile.ec2_profile.name
  associate_public_ip_address = true
    depends_on = [
    aws_secretsmanager_secret_version.xclone_values ]

  root_block_device {
    volume_size = 40
    volume_type = "gp3"
  }

  # Render and inject cloud-init script
  user_data = templatefile("${path.module}/cloud-init.tpl", {
    repo_url    = var.repo_url
    repo_branch = var.repo_branch
    secret_arn  = data.aws_secretsmanager_secret.xclone.arn
    domain      = var.domain_name
    email       = var.email
    aws_region  = var.aws_region # <--- Added for dynamic region support
  })

  # Force recreation when user_data (cloud-init.tpl) changes
  user_data_replace_on_change = true

  tags = {
    Name = "xclone-app"
  }
}

# Outputs for convenience
output "app_public_ip" {
  value = aws_instance.app.public_ip
}

output "app_public_dns" {
  value = aws_instance.app.public_dns
}
