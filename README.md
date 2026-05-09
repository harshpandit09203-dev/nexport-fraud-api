# ⚡ Nexport Fraud Detection API

> FastAPI-based fraud detection backend for the Nexport B2B Trade Platform

[

![API Live](https://img.shields.io/badge/API-Live-green?style=for-the-badge)

](https://nexport-fraud-api-1.onrender.com)
[

![Docs](https://img.shields.io/badge/Docs-ReDoc-blue?style=for-the-badge)

](https://nexport-fraud-api-1.onrender.com/redoc)
[

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge)

](https://python.org)

---

## 📌 What This Does

REST API that accepts buyer/seller trade data and returns a real-time fraud risk score. Backend for the [Nexport Fraud Detection App](https://nexport-fraud-detection.onrender.com/).

---

## 🔗 Live Links

| | URL |
|--|-----|
| API Base | https://nexport-fraud-api-1.onrender.com |
| API Docs | https://nexport-fraud-api-1.onrender.com/redoc |
| Frontend | https://nexport-fraud-detection.onrender.com/ |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | FastAPI |
| Database | PostgreSQL (Railway) |
| Deployment | Render |
| Language | Python 3.10+ |

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/register` | Submit entity data, get fraud score |
| GET | `/users` | Fetch all scanned users |
| GET | `/stats` | Summary stats |
| GET | `/` | Health check |

---

## 📥 Sample Request

```json
POST /register

{
  "entity_type": "Buyer",
  "country_code": "IN",
  "years_in_business": 3,
  "kyc_verified": 1,
  "documents_verified": 1,
  "website_exists": 1,
  "email_domain_age_days": 200,
  "failed_transactions": 2,
  "complaints_received": 1,
  "ip_country_mismatch": 0,
  "multiple_accounts_flag": 0,
  "transaction_amount": 10000
}
```

## 📤 Sample Response

```json
{
  "entity_id": "USR4F2A1B3C",
  "trust_score": 85,
  "behavioral_score": 0,
  "final_risk_score": 6.0,
  "risk_category": "LOW RISK",
  "action": "ALLOW"
}
```

---

## 🧠 Scoring Logic

| Score | Category | Action |
|-------|----------|--------|
| < 40 | LOW RISK | ALLOW |
| 40–70 | MEDIUM RISK | REVIEW |
| > 70 | HIGH RISK | BLOCK |

**Trust Score deductions:**
- KYC not verified → -25
- Documents not verified → -20
- No website → -10
- Email domain < 180 days → -15
- Failed transactions > 15 → -15
- Complaints > 8 → -15
- IP country mismatch → -10
- Multiple accounts → -10
- Business > 5 years → +10

---

## 🗂️ Project Structure

```
nexport-fraud-api/
├── api.py
├── requirements.txt
└── README.md
```

---

## ⚙️ Run Locally

```bash
git clone https://github.com/harshpandit09203-dev/nexport-fraud-api
cd nexport-fraud-api
pip install -r requirements.txt
export DATABASE_URL="your_postgresql_url"
uvicorn api:app --reload
```

---

## 👤 Author

**Harsh Pandit**
Founder @ Nexport Trade Pvt Ltd
B.Sc. Computer Science | Data Science & AI-ML
GitHub: [@harshpandit09203-dev](https://github.com/harshpandit09203-dev)
