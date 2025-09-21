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
    from airflow.operators.python import PythonOperator

    def check_secrets():
        val = Variable.get("test-var")
        assert val is not None, "Variable not found"
        conn = BaseHook.get_connection("test-conn")
        assert conn is not None, "Connection not found"
        print("✅ Key Vault backend working, variable and connection retrieved.")
        print("Variable keys:", val)
        print("Connection password (secret):", conn)

    check_secrets_task = PythonOperator(
        task_id="check_secrets",
        python_callable=check_secrets,
    )

run_this = test_secrets()
