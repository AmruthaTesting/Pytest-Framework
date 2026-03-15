import boto3
import json
from botocore.exceptions import ClientError

REGION = "us-east-1"


def get_secret(secret_name, key):
    """Fetch and return a value from AWS Secrets Manager."""
    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=REGION)
    try:
        response = client.get_secret_value(SecretId=secret_name)
        secret_str = response["SecretString"]
        secret_dict = json.loads(secret_str)
        return secret_dict[key]
    except ClientError as e:
        raise e
    except (KeyError, json.JSONDecodeError) as e:
        raise ValueError(
            f"Invalid secret format for '{secret_name}' or missing key '{key}'"
        ) from e


def PASSWORD():
    return get_secret(secret_name="SRM-QA-PASSWORD", key="PASSWORD")


def USER():
    return get_secret(secret_name="SRM-QA-USER", key="USER")
