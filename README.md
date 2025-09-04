# airflow-azure-starter

## Required .env file for Azure OAuth

You must create a `.env` file in the project root with the following variables for Azure authentication to work:

```ini
AIRFLOW_UID=501
AAD_TENANT_ID=your-azure-tenant-id
AAD_CLIENT_ID=your-azure-client-id
AAD_CLIENT_SECRET=your-azure-client-secret
AZURE_REDIRECT_URI=http://localhost:8080/oauth-authorized/azure
```

**Note:**
- The `.env` file is not included in the repository for security reasons.
- All four Azure variables are required for OAuth login to work.
- Use your actual Azure values in place of the example values above.