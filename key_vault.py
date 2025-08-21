from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import os

def get_secret(secret_name, vault_url=None):
    vault_url = vault_url or os.environ.get("AZURE_KEY_VAULT_URL")
    if not vault_url:
        raise RuntimeError("Set AZURE_KEY_VAULT_URL in environment.")
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=vault_url, credential=credential)
    return client.get_secret(secret_name).value

if __name__ == "__main__":
    secret = get_secret("MY_TEST_SECRET")
    print(secret)
