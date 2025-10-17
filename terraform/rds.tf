resource "random_password" "db_password" {
  length           = 16
  special          = true
  override_special = "!#$%^&*()-_=+[]{}<>:?" # ✅ excludes '/', '@', and '"'
}

resource "aws_db_subnet_group" "rds_subnets" {
  name       = "xclone-rds-subnet-group"
  subnet_ids = data.aws_subnets.default.ids
}

resource "aws_db_instance" "postgres" {
  identifier              = "xclone-db"
  engine                  = "postgres"
  engine_version          = "15.14"
  instance_class          = "db.t3.micro" # change for production
  allocated_storage       = 20
  storage_type            = "gp3"
  username                = "xclone"
  password                = random_password.db_password.result
  db_name                 = "xclone"
  db_subnet_group_name    = aws_db_subnet_group.rds_subnets.name
  vpc_security_group_ids  = [aws_security_group.rds.id]
  skip_final_snapshot     = true
  publicly_accessible     = false
  backup_retention_period = 7
  multi_az                = false
  deletion_protection     = false
  tags                    = { Name = "xclone-postgres" }
}
