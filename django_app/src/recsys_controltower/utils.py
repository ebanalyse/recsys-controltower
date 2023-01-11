import logging
import os
from typing import Dict, Any
import json

import boto3
from botocore.exceptions import ClientError

AWS_REGION = "eu-west-1"

DEFAULT_DATABASE_SECRET_ENV_VAR = "DATABASE_SECRET"

logger = logging.getLogger(__name__)

SM_CLIENT = None


def get_secretsmanager_client():
    global SM_CLIENT
    if SM_CLIENT is None:
        SM_CLIENT = boto3.client(
            service_name="secretsmanager", region_name=AWS_REGION)
    return SM_CLIENT


def get_secret(secret_id: str) -> Dict[str, Any]:
    # Create a Secrets Manager client
    client = get_secretsmanager_client()
    try:
        secret_value_response = client.get_secret_value(SecretId=secret_id)
    except ClientError as e:
        logger.exception(e)
        raise e
    # Decrypts secret using the associated KMS CMK.
    # Depending on whether the secret is a string or binary, one of these fields will be populated.
    if "SecretString" in secret_value_response:
        secret = secret_value_response["SecretString"]
        return json.loads(secret)
    raise ValueError("Response does not contain 'SecretString'")


def get_db_credentials(env: str, read_only: bool = False) -> Dict[str, str]:
    """
    Get db credentials as used by Django with keys
    HOST, NAME, USER, PASSWORD, PORT
    """
    # Dict with 'Django db settings name to env var name, default_value
    # For read only user env vars are subscripted with _RO
    env_keys = {
        "HOST": ("DJANGO_DB_HOST", "db"),
        "USER": ("DJANGO_DB_USER", "postgres"),
        "PASSWORD": ("DJANGO_DB_PASSWORD", "postgres"),
        "NAME": ("DJANGO_DB_NAME", "postgres"),
        "PORT": ("DJANGO_DB_PORT", "5432"),
    }
    if read_only:
        # env keys subscripted with _RO, e.g. DJANGO_DB_HOST_RO
        for key in env_keys:
            var_name, default = env_keys[key]
            env_keys[key] = (var_name + "_RO", default)
    if env_keys["HOST"][0] in os.environ or env == "local":
        # Use env vars - with defaults (for local)
        creds = {key: os.getenv(val[0], val[1])
                 for key, val in env_keys.items()}
        return creds
    # Else a CDK style rds secret - will fail if relevant secret id is not set in as env var
    secret_id_env_var = DEFAULT_DATABASE_SECRET_ENV_VAR
    logger.info("Will read secret id from env var %s", secret_id_env_var)
    secret_id = os.environ[secret_id_env_var]
    logger.info("Will credentials from secret id", secret_id)
    secret = get_secret(secret_id)
    host = secret["host"]
    if read_only:
        if host.endswith(".rds.amazonaws.com") and "cluster-ro" not in host:
            old_host = host
            host = host.replace("cluster-", "cluster-ro-")
            logger.info("Modifying %s to read only endpoint %s",
                        old_host, host)
    return {
        "HOST": host,
        "USER": secret["username"],
        "PASSWORD": secret["password"],
        "NAME": secret["dbname"],
        "PORT": str(secret["port"]),
    }
