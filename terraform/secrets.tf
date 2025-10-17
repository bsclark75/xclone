data "aws_secretsmanager_secret" "xclone" {
  name = "xclone/credentials"
}

resource "aws_secretsmanager_secret_version" "xclone_values" {
  secret_id = data.aws_secretsmanager_secret.xclone.id

  secret_string = jsonencode({
    FLASK_ENV         = "production"
    SECRET_KEY        = aws_db_instance.postgres.password
    MAIL_SERVER       = var.mail_server
    MAIL_PORT         = var.mail_port
    MAIL_USE_TLS      = var.mail_use_tls
    MAIL_USERNAME     = var.mail_username
    MAIL_PASSWORD     = var.mail_password
    POSTGRES_USER     = aws_db_instance.postgres.username
    POSTGRES_PASSWORD = aws_db_instance.postgres.password
    POSTGRES_DB       = aws_db_instance.postgres.db_name
    POSTGRES_HOST     = aws_db_instance.postgres.address
  })
}

output "xclone_secret_version_id" {
  value = aws_secretsmanager_secret_version.xclone_values.id
}

