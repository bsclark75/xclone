data "aws_iam_policy_document" "ec2_assume" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "ec2_role" {
  name               = "xclone-ec2-role"
  assume_role_policy = data.aws_iam_policy_document.ec2_assume.json
}

resource "aws_iam_instance_profile" "ec2_profile" {
  name = "xclone-ec2-profile"
  role = aws_iam_role.ec2_role.name
}

resource "aws_iam_role_policy_attachment" "ssm_attach" {
  role       = aws_iam_role.ec2_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}

data "aws_iam_policy_document" "secrets_policy" {
  statement {
    actions = [
      "secretsmanager:GetSecretValue",
      "secretsmanager:DescribeSecret"
    ]
    resources = [data.aws_secretsmanager_secret.xclone.arn]
  }
}

resource "aws_iam_policy" "secrets_read" {
  name   = "xclone-secrets-read"
  policy = data.aws_iam_policy_document.secrets_policy.json
}

resource "aws_iam_role_policy_attachment" "attach_secrets" {
  role       = aws_iam_role.ec2_role.name
  policy_arn = aws_iam_policy.secrets_read.arn
}
