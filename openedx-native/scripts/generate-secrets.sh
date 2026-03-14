#!/bin/bash
# Generate secrets for Open edX Native Docker Compose setup
# This script generates strong random secrets for all required environment variables

set -e

echo "==================================="
echo "Open edX Secrets Generator"
echo "==================================="
echo ""

# Function to generate a random password
generate_password() {
    openssl rand -base64 32 | tr -d "=+/" | cut -c1-32
}

# Function to generate Django secret key
generate_django_secret() {
    python3 -c "import random, string; print(''.join(random.SystemRandom().choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(50)))"
}

echo "Generating secrets..."
echo ""

# MySQL
MYSQL_ROOT_PASSWORD=$(generate_password)
MYSQL_PASSWORD=$(generate_password)

# MongoDB
MONGO_PASSWORD=$(generate_password)

# Redis
REDIS_PASSWORD=$(generate_password)

# Meilisearch
MEILI_MASTER_KEY=$(generate_password)

# Django
SECRET_KEY=$(generate_django_secret)

# Display generated secrets
echo "==================================="
echo "Generated Secrets"
echo "==================================="
echo ""
echo "MYSQL_ROOT_PASSWORD=$MYSQL_ROOT_PASSWORD"
echo "MYSQL_PASSWORD=$MYSQL_PASSWORD"
echo "MONGO_PASSWORD=$MONGO_PASSWORD"
echo "REDIS_PASSWORD=$REDIS_PASSWORD"
echo "MEILI_MASTER_KEY=$MEILI_MASTER_KEY"
echo "SECRET_KEY=$SECRET_KEY"
echo ""
echo "==================================="
echo "IMPORTANT: Copy these values to your .env file"
echo "==================================="
echo ""
echo "To create .env file automatically, run:"
echo "  ./scripts/generate-secrets.sh > .env.secrets"
echo "  cat .env.example .env.secrets > .env"
echo "  rm .env.secrets"
echo ""
