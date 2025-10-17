variable "briansclark_zone_id" {
  type        = string
  description = "Hosted Zone ID for briansclark.net"
}

# Directly reference the variable
resource "aws_route53_record" "xclone_a" {
  zone_id = var.briansclark_zone_id
  name    = "xclone.briansclark.net"
  type    = "A"
  ttl     = 300
  records = [aws_instance.app.public_ip]
}

