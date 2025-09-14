#!/bin/bash
set -euo pipefail

# Set Airflow UID
export AIRFLOW_UID=5001

# Create necessary folders and set permissions
for d in logs dags plugins config; do
  mkdir -p "$d"
  sudo chown -R $AIRFLOW_UID:0 "$d"
done

# Log in with the VM's managed identity
az login --identity --output none

# Get Key Vault name from environment variable
KEYVAULT_NAME="${KEYVAULT_NAME:?Environment variable KEYVAULT_NAME not set}"

# Get DOMAIN_NAME from environment variable
DOMAIN_NAME="${DOMAIN_NAME:?Environment variable DOMAIN_NAME not set}"
export DOMAIN_NAME

# Fetch secrets from Key Vault
FERNET_KEY=$(az keyvault secret show --vault-name "$KEYVAULT_NAME" --name fernet-key --query value -o tsv)
# SQL_CONN=$(az keyvault secret show --vault-name "$KEYVAULT_NAME" --name sql-conn --query value -o tsv)
AAD_TENANT_ID=$(az keyvault secret show --vault-name "$KEYVAULT_NAME" --name aad-tenant-id --query value -o tsv)
AAD_CLIENT_ID=$(az keyvault secret show --vault-name "$KEYVAULT_NAME" --name aad-client-id --query value -o tsv)
AAD_CLIENT_SECRET=$(az keyvault secret show --vault-name "$KEYVAULT_NAME" --name aad-client-secret --query value -o tsv)


# Write to temporary .env
cat > .env <<EOF
AIRFLOW_UID=$AIRFLOW_UID
DOMAIN_NAME=$DOMAIN_NAME
FERNET_KEY=$FERNET_KEY
AAD_TENANT_ID=$AAD_TENANT_ID
AAD_CLIENT_ID=$AAD_CLIENT_ID
AAD_CLIENT_SECRET=$AAD_CLIENT_SECRET
EOF

# Start Airflow with Docker Compose
sudo docker compose up -d

# Permanently remove .env
shred -u .env

# Show running containers
sudo docker ps