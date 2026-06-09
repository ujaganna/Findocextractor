import json
import os
from openai import AzureOpenAI, OpenAI
from dotenv import load_dotenv

load_dotenv()

EXTRACTION_SCHEMA = {
    "company_name": "string",
    "filing_type": "10-K or 10-Q",
    "fiscal_year": "YYYY",
    "revenue_current": "number in millions USD or null",
    "revenue_prior": "number in millions USD or null",
    "net_income_current": "number in millions USD or null",
    "net_income_prior": "number in millions USD or null",
    "eps_basic": "number or null",
    "eps_diluted": "number or null",
    "ebitda": "number in millions USD or null",
    "total_debt": "number in millions USD or null",
    "total_equity": "number in millions USD or null",
    "operating_cash_flow": "number in millions USD or null",
    "audit_opinion": "Unqualified / Qualified / Adverse / Going Concern / Disclaimer or null",
    "auditor_name": "string or null",
}


def _get_client():
    if os.getenv("USE_GITHUB_MODELS", "false").lower() == "true":
        return OpenAI(
            base_url="https://models.inference.ai.azure.com",
            api_key=os.getenv("GITHUB_TOKEN"),
        ), os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o")
    return AzureOpenAI(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_KEY"),
        api_version="2024-08-01-preview",
    ), os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o")


def extract_metrics(filing_text: str) -> dict:
    """
    Extract structured financial metrics from an SEC filing using GPT-4o.
    Uses first + last 8000 chars to capture header info and financial tables.
    """
    client, model = _get_client()
    chunk = filing_text[:8000] + "\n...[middle omitted]...\n" + filing_text[-8000:]

    prompt = f"""You are a financial analyst. Extract key metrics from this SEC filing.
Return ONLY valid JSON matching this schema exactly (use null for any missing values):
{json.dumps(EXTRACTION_SCHEMA, indent=2)}

All monetary values should be in millions of USD as plain numbers (e.g. 1234.5, not "$1,234.5M").

FILING TEXT:
{chunk}
"""

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        temperature=0,
    )

    return json.loads(response.choices[0].message.content)
