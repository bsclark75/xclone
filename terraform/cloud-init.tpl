#!/bin/bash
set -euxo pipefail

# --- Variables populated by Terraform ---
REPO_URL="${repo_url}"
REPO_BRANCH="${repo_branch}"
SECRET_ARN="${secret_arn}"
DOMAIN="${domain}"
EMAIL="${email}"
AWS_REGION="${aws_region}"

# --- Paths ---
APP_DIR="/opt/xclone"
ENV_JSON="$APP_DIR/.env.json"
ENV_FILE="$APP_DIR/.env"

# --- Update system and install dependencies ---
apt-get update -y
DEBIAN_FRONTEND=noninteractive apt-get install -y \
  git python3-venv python3-pip nginx jq awscli snapd postgresql-client

# --- Install and enable SSM Agent ---
if systemctl list-unit-files | grep -q 'amazon-ssm-agent'; then
  systemctl enable --now amazon-ssm-agent || \
  systemctl enable --now snap.amazon-ssm-agent.amazon-ssm-agent.service || true
else
  systemctl enable --now snapd.socket
  snap install amazon-ssm-agent --classic
  sleep 5
  systemctl enable --now snap.amazon-ssm-agent.amazon-ssm-agent.service || true
fi

# --- Install Certbot for SSL ---
snap install core; snap refresh core
snap install --classic certbot || true
ln -sf /snap/bin/certbot /usr/bin/certbot || true

# --- Clone application repository ---
if [ ! -d "$APP_DIR/.git" ]; then
  git clone --branch "$REPO_BRANCH" "$REPO_URL" "$APP_DIR"
else
  cd "$APP_DIR" && git fetch && git checkout "$REPO_BRANCH" && git pull
fi

# --- Configure firewall ---
ufw --force reset
ufw allow OpenSSH
ufw allow 'Nginx Full'
ufw --force enable || true

# --- Fetch secrets from AWS Secrets Manager ---
for i in {1..5}; do
  echo "Attempt $i: Fetching secrets..."
  aws secretsmanager get-secret-value \
    --secret-id "$SECRET_ARN" \
    --region "$AWS_REGION" \
    --query SecretString \
    --output text > "$ENV_JSON" 2>/dev/null

  if jq -e . "$ENV_JSON" >/dev/null 2>&1; then
    echo "✅ Secrets fetched successfully."
    break
  fi

  echo "⚠️ Secrets not ready, retrying in 5s..."
  sleep 5
done

if ! jq -e . "$ENV_JSON" >/dev/null 2>&1; then
  echo "❌ Failed to fetch AWS secrets after retries."
  exit 1
fi

# --- Generate .env from secrets JSON ---
echo "🧩 Generating .env file..."
jq -r '
  . as $env |
  "FLASK_ENV=production",
  "DATABASE_URL=\"postgresql://\($env.POSTGRES_USER):\($env.POSTGRES_PASSWORD)@\($env.POSTGRES_HOST):\($env.POSTGRES_PORT // 5432)/\($env.POSTGRES_DB)\"",
  "POSTGRES_USER=\($env.POSTGRES_USER)",
  "POSTGRES_PASSWORD=\"\($env.POSTGRES_PASSWORD)\"",
  "POSTGRES_DB=\($env.POSTGRES_DB)",
  "POSTGRES_HOST=\($env.POSTGRES_HOST)",
  "POSTGRES_PORT=\($env.POSTGRES_PORT // 5432)",
  "MAIL_SERVER=\($env.MAIL_SERVER)",
  "MAIL_PORT=\($env.MAIL_PORT)",
  "MAIL_USE_TLS=\($env.MAIL_USE_TLS)",
  "MAIL_USERNAME=\($env.MAIL_USERNAME)",
  "MAIL_PASSWORD=\($env.MAIL_PASSWORD)"
' "$ENV_JSON" > "$ENV_FILE"

chmod 600 "$ENV_FILE"
set -a; . "$ENV_FILE"; set +a

# --- Python virtual environment ---
cd "$APP_DIR"
python3 -m venv venv
. venv/bin/activate
pip install --upgrade pip
[ -f requirements.txt ] && pip install -r requirements.txt

# --- Create Gunicorn service ---
cat >/etc/systemd/system/gunicorn.service <<'EOF'
[Unit]
Description=Gunicorn instance to serve Flask app
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/opt/xclone
EnvironmentFile=/opt/xclone/.env
ExecStart=/opt/xclone/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:8000 "app:create_app()"
Restart=always

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable --now gunicorn

# --- Configure Nginx (HTTP) ---
mkdir -p /var/www/certbot
cat >/etc/nginx/sites-available/xclone <<EOF
server {
  listen 80;
  server_name $DOMAIN;

  root /var/www/certbot;
  location /.well-known/acme-challenge/ {
    try_files \$uri =404;
  }

  location / {
    proxy_pass http://127.0.0.1:8000;
    proxy_set_header Host \$host;
    proxy_set_header X-Real-IP \$remote_addr;
    proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto \$scheme;
  }
}
EOF

ln -sf /etc/nginx/sites-available/xclone /etc/nginx/sites-enabled/xclone
rm -f /etc/nginx/sites-enabled/default
nginx -t && systemctl restart nginx

# --- Obtain SSL certificate ---
certbot certonly --nginx -d "$DOMAIN" -m "$EMAIL" --agree-tos --non-interactive

# --- Configure Nginx (HTTPS) ---
cat >/etc/nginx/sites-available/xclone <<EOF
server {
    listen 80;
    server_name $DOMAIN;
    return 301 https://\$host\$request_uri;
}

server {
    listen 443 ssl;
    server_name $DOMAIN;

    ssl_certificate /etc/letsencrypt/live/$DOMAIN/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/$DOMAIN/privkey.pem;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;

    root /var/www/certbot;
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    access_log /var/log/nginx/xclone_access.log;
    error_log /var/log/nginx/xclone_error.log;
}
EOF

systemctl reload nginx

# Apply database migrations and setup admin user
echo "📦 Applying database migrations and initializing admin user..."
cd /opt/xclone
source venv/bin/activate
flask db upgrade
python setup_admin.py


# --- Complete ---
touch /tmp/cloud-init-done
echo "✅ Cloud-init completed successfully at $(date)"
