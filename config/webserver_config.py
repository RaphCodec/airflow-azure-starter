from flask_appbuilder.security.manager import AUTH_OAUTH
import os
from airflow.providers.fab.auth_manager.security_manager.override import FabAirflowSecurityManagerOverride
from airflow.utils.log.logging_mixin import LoggingMixin


# Set up Redis for Rate Limiting
RATELIMIT_ENABLED = True
RATELIMIT_STORAGE_URI: "redis://redis:6379/0"
# using fixed window for simplicity and memory opitimization. change as needed.
RATELIMIT_STRATEGY = "fixed-window" 
RATELIMIT_DEFAULT = "200/hour;50/minute"
RATELIMIT_APPLICATION = "2000/day"

AUTH_TYPE = AUTH_OAUTH
AUTH_USER_REGISTRATION = True
AUTH_USER_REGISTRATION_ROLE = "Public"  # For testing, gives all new users admin rights, CHANGE TO Public FOR PRODUCTION
AUTH_ROLES_SYNC_AT_LOGIN = True
AUTH_ROLES_MAPPING = {
    "airflow_prod_admin": ["Admin"],
    "airflow_prod_user": ["Op"],
    "airflow_prod_viewer": ["Viewer"]
}
# force users to re-auth after 30min of inactivity (to keep roles in sync)
PERMANENT_SESSION_LIFETIME = 1800

# If you wish, you can add multiple OAuth providers.
OAUTH_PROVIDERS = [
    {
        "name": "azure",
        "icon": "fa-windows",
        "token_key": "access_token",
        "remote_app": {
            "base_url": "https://graph.microsoft.com/v1.0/",
            "request_token_params": {"scope": "openid"},
            "access_token_url": f"https://login.microsoftonline.com/{os.environ.get('AAD_TENANT_ID')}/oauth2/token",
            "authorize_url": f"https://login.microsoftonline.com/{os.environ.get('AAD_TENANT_ID')}/oauth2/authorize",
            "request_token_url": None,
            "client_id": os.environ.get('AAD_CLIENT_ID'),
            "client_secret": os.environ.get('AAD_CLIENT_SECRET'),
        },
    },
]

class AzureOAuth(FabAirflowSecurityManagerOverride, LoggingMixin):
    def get_azure_user_info(self, provider, response=None):
        try:
            me = super().get_azure_user_info(provider, response)
        except Exception as e:
            import traceback
            traceback.print_exc()
            self.log.debug(e)

        return {
            "name": me["first_name"] + " " + me["last_name"],
            "email": me["email"],
            "first_name": me["first_name"],
            "last_name": me["last_name"],
            "id": me["id"],
            "username": me["email"],
            "role_keys": me.get("role_keys", ["Public"])
        }
    

SECURITY_MANAGER_CLASS = AzureOAuth