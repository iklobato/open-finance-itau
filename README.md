````markdown
# Itaú Open Finance Credit Card Transactions Fetcher

This script connects to Itaú's Open Finance API and retrieves **credit card transactions for the past 360 days** using the `credit-cards-accounts` scope. It uses **OAuth2 Client Credentials**, **Mutual TLS**, and displays the results in a beautiful tabular format using `tabulate`.

---

## ✅ Features

- Connects to Itaú's Open Finance production or sandbox environment
- Authenticates using OAuth2 with mTLS (Mutual TLS)
- Retrieves transactions from the `/credit-cards-accounts/v1/transactions` endpoint
- Paginates through the full result set
- Displays results in a tabular report

---

## 🧰 Prerequisites

Before running this script, make sure you have:

### 1. Open Finance Access via Itaú

You must be a **registered TPP (Third Party Provider)** via the Brazilian Open Finance ecosystem and authorized by the Central Bank.

#### Register as a TPP:

- Visit [Open Finance Brasil Directory](https://www.bcb.gov.br/en/financialstability/openfinance)
- Obtain your **Software Statement Assertion (SSA)** via your **Directory participant registration**
- Register with Itaú via their [Developer Portal](https://devportal.itau.com.br/)

### 2. Required Information

You will need:

| Name              | Description                                                                 |
|-------------------|-----------------------------------------------------------------------------|
| `client_id`       | Provided by Itaú upon registering your app                                  |
| `client_secret`   | Provided by Itaú (used with mTLS OAuth2 authentication)                     |
| `consent_id`      | Obtained via consent flow with user authorization                           |
| `client.crt`      | Your **x.509 client certificate** signed by a recognized CA (e.g., Serpro)  |
| `client.key`      | The **private key** corresponding to `client.crt`                           |

---

## 📦 Installation

```bash
git clone https://github.com/seu-usuario/openfinance-itau-transactions.git
cd openfinance-itau-transactions
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
````

`requirements.txt` should contain:

```
requests
python-dateutil
tabulate
```

---

## 🔧 Configuration

Update the following variables at the top of the script (`fetch_itau_transactions.py`):

```python
CLIENT_ID = "seu-client-id"
CLIENT_SECRET = "seu-client-secret"
CONSENT_ID = "seu-consent-id"
CERT = ("client.crt", "client.key")
```

> Use full paths to the certificate and key files if not in the same directory.

---

## 🔐 Consent Flow (Important)

The `CONSENT_ID` must come from a prior **OAuth2 Authorization Code Flow** executed by your front-end with the user.

This means:

1. Your user authorizes your TPP to access their card data.
2. You capture the `consentId` returned in the callback.
3. Store this `consentId` and use it in the script.

For a guide on implementing the consent flow, see:
[Itaú Open Finance Consent Flow Guide (PT-BR)](https://devportal.itau.com.br/apis/open-banking/autenticacao/autenticacao-dos-usuarios)

---

## 🚀 Running the Script

Once configured:

```bash
python fetch_itau_transactions.py
```

Expected output:

```
+--------------------------+------------+----------+-----------+
| Transaction              | Date       | Amount   | Currency  |
+==========================+============+==========+===========+
| Compra Netflix           | 2024-09-10 | -39.90   | BRL       |
| Padaria dos Pães         | 2024-09-12 | -12.00   | BRL       |
| ...                      | ...        | ...      | ...       |
+--------------------------+------------+----------+-----------+
```

---

## 🧪 Using Sandbox (Optional)

To test with Itaú Sandbox:

Change the following lines in the script:

```python
BASE_URL = "https://api.sandbox.itau/open-banking"
ACCESS_TOKEN_URL = "https://sts.sandbox.itau.com.br/api/token"
```

> Note: Sandbox requires separate credentials and mock consent from Itaú's Sandbox Console.

---

## 📋 Additional Notes

* Be sure your **mTLS certificates** are authorized and signed by a valid Open Finance CA (e.g., Serpro).
* All traffic must be encrypted (HTTPS) and use **strong TLS 1.2+ cipher suites**.
* Itaú may throttle or reject unauthenticated or non-compliant traffic.

---

## 🛟 Troubleshooting

| Problem                               | Solution                                                           |
| ------------------------------------- | ------------------------------------------------------------------ |
| `401 Unauthorized`                    | Check `client_id`, `client_secret`, and mTLS certs                 |
| `403 Forbidden`                       | Ensure `consent_id` is active and permissions include credit cards |
| `SSLError: certificate verify failed` | Check your cert and key files, and verify chain with OpenSSL       |
| `KeyError` on missing fields          | Itaú Sandbox responses may differ from production                  |

---

## 📜 License

MIT License.

---

## 📞 Need Help?

* [Open Finance Brasil Official Site](https://www.bcb.gov.br/en/financialstability/openfinance)
* [Itaú Developer Portal](https://devportal.itau.com.br/)
* [OpenID Foundation Brazil](https://www.openid.net.br/)

```
NvimTree_1 open-finance-itau
# open-finance-itau
