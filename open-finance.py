import requests
import datetime
from dateutil.relativedelta import relativedelta
from tabulate import tabulate

BASE_URL = "https://api.itau/open-banking"
CLIENT_ID = "seu-client-id"
CLIENT_SECRET = "seu-client-secret"
CONSENT_ID = "seu-consent-id"
ACCESS_TOKEN_URL = "https://sts.itau.com.br/api/token"
CERT = ("client.crt", "client.key")
HEADERS = {"x-fapi-financial-id": "itau"}

def get_access_token():
    data = {
        "grant_type": "client_credentials",
        "scope": "credit-cards-accounts:transactions:read"
    }
    response = requests.post(
        ACCESS_TOKEN_URL,
        data=data,
        auth=(CLIENT_ID, CLIENT_SECRET),
        cert=CERT,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    response.raise_for_status()
    return response.json()["access_token"]

def fetch_transactions(access_token):
    today = datetime.date.today()
    start_date = (today - relativedelta(days=360)).isoformat()
    end_date = today.isoformat()

    url = f"{BASE_URL}/credit-cards-accounts/v1/transactions"
    headers = {
        **HEADERS,
        "Authorization": f"Bearer {access_token}",
        "Consent-ID": CONSENT_ID
    }
    params = {
        "fromTransactionDate": start_date,
        "toTransactionDate": end_date,
        "page": 1,
        "page-size": 100
    }

    all_transactions = []

    while True:
        response = requests.get(url, headers=headers, params=params, cert=CERT)
        response.raise_for_status()
        data = response.json()
        transactions = data.get("data", {}).get("transaction", [])
        all_transactions.extend(transactions)

        if "next" not in data.get("links", {}):
            break
        params["page"] += 1

    return all_transactions

if __name__ == "__main__":
    try:
        token = get_access_token()
        transactions = fetch_transactions(token)
        rows = [
            [t["transactionName"], t["transactionDate"], t["amount"]["amount"], t["amount"]["currency"]]
            for t in transactions
        ]
        headers = ["Transaction", "Date", "Amount", "Currency"]
        print(tabulate(rows, headers=headers, tablefmt="grid"))
    except Exception as e:
        print(f"Erro: {e}")

