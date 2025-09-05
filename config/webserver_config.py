from flask_appbuilder.security.manager import AUTH_OAUTH
import os
from airflow.providers.fab.auth_manager.security_manager.override import FABAirflowSecurityManagerOverride
from airflow.utils.log.logging_mixin import LoggingMixin


# RATELIMIT_STORAGE_URI: "redis://redis:6379"
AUTH_TYPE = AUTH_OAUTH
AUTH_USER_REGISTRATION = True
AUTH_USER_REGISTRATION_ROLE = "Public"
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
            "api_base_url": "https://login.microsoftonline.com/{}/".format(os.getenv("AAD_TENANT_ID")),
            "request_token_url": None,
            "request_token_params": {
                "scope": "openid email profile"
            },
            "access_token_url": "https://login.microsoftonline.com/{}/oauth2/v2.0/token".format(os.getenv("AAD_TENANT_ID")),
            "access_token_params": {
                "scope": "openid email profile"
            },
            "authorization_url": "https://login.microsoftonline.com/{}/oauth2/v2.0/authorize".format(os.getenv("AAD_TENANT_ID")),
            "authorization_params": {
                "scope": "openid email profile"
            },
            "client_id": os.getenv("AAD_CLIENT_ID"),
            "client_secret": os.getenv("AAD_CLIENT_SECRET"),
            "jwks_uri": "https://login.microsoftonline.com/common/discovery/v2.0/keys",
        },
    },
]

class AzureOAuth(FABAirflowSecurityManagerOverride, LoggingMixin):
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