# Stock Hunter AI: Azure Foundry Ready

## Structure

- Modular agents: ingestion, preprocessing, training, inference API, risk, orchestration, monitoring, security.
- Config: `/config/*.json`
- Logs: `/monitoring/`
- Code is operational, staged for Azure Foundry / AML Online Endpoint.

## Setup/Testing

1. `pip install -r requirements.txt`
2. Configure `/config` for sources and add your secrets in Azure Key Vault.
3. Run: `bash run_all.sh`
4. All tests: `pytest tests/`
5. To deploy: `bash deploy_azure.sh`
6. API runs at `:8000`, docs at `/docs`.

## Security / Deployment

- No secrets in config/code
- Add Key Vault and Managed Identity for Azure
- Uses Dockerfile for quick build

---
