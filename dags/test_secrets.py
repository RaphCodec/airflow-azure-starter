from __future__ import annotations

import logging
import sys

from airflow.models import Variable
from airflow.hooks.base import BaseHook

from airflow.sdk import dag, task

log = logging.getLogger(__name__)

PATH_TO_PYTHON_BINARY = sys.executable

@dag(
    schedule=None,
    description="""
    A simple tutorial DAG to show the usage of secrets backend. 
    This Dag should be used with a dummy airflow connection and variable stored in Azure Key Vault.
    This is not intended for production use and is only for demonstration purposes.
    This DAG requires the 'apache-airflow-providers-microsoft-azure' package.
    what this dag does is BAD PRACTICE and is only for demonstration purposes.
    DO NOT STORE SECRETS IN YOUR DAGs OR CODE.
    DO NOT PRINT SECRETS IN YOUR LOGS.
    DO NOT PRINT OR LOG SECRETS OR SENSITIVE VARIABLES ANYWHERE.

    ONCE YOU HAVE CONFIRMED IT WORKS, DELETE THIS DAG AND THE DUMMY CONNECTION AND VARIABLE.
    """,
)
def test_secrets():
    # Fetch a variable from Key Vault via the secrets backend
    # Omit the variable prefix "air-var". Airflow adds it automatically.
    val = Variable.get("test-var")
    assert val is not None, "Variable not found"
    # Fetch a connection from Key Vault via the secrets backend
    # Omit the connection prefix "air-conn". Airflow adds it automatically.
    conn = BaseHook.get_connection("test-conn")
    assert conn is not None, "Connection not found"
    # Only print confirmation, not the value
    print("✅ Key Vault backend working, variable and connection retrieved.")

run_this = test_secrets()