from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
import uuid
from datetime import datetime
from pydantic import BaseModel
import os   

app = FastAPI(title="Nexport Fraud Detection API") 

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)


DATABASE_URL = os.getenv"postgresql://postgres:PhAaLrAsKh-03@db.htkhgsbkcnwmphpmegyb.supabase.co:5432/postgres"
def get_db():
    return psycopg2.connect(
        DATABASE_URL,
        sslmode='require',
        connect_timeout=10
    )

class UserData(BaseModel):
    entity_type: str
    country_code: str
    years_in_business: int
    kyc_verified: int
    documents_verified: int
    website_exists: int
    email_domain_age_days: int
    failed_transactions: int
    complaints_received: int
    ip_country_mismatch: int
    multiple_accounts_flag: int
    transaction_amount: float

def calculate_scores(data):
    score = 100
    if data.kyc_verified == 0:           score -= 25
    if data.documents_verified == 0:     score -= 20
    if data.website_exists == 0:         score -= 10
    if data.email_domain_age_days < 180: score -= 15
    if data.failed_transactions > 15:    score -= 15
    if data.complaints_received > 8:     score -= 15
    if data.ip_country_mismatch == 1:    score -= 10
    if data.multiple_accounts_flag == 1: score -= 10
    if data.years_in_business > 5:       score += 10
    trust_score = max(0, min(100, score))

    beh = 0
    if data.failed_transactions > 15:    beh += 25
    if data.complaints_received > 8:     beh += 20
    if data.ip_country_mismatch == 1:    beh += 35
    if data.multiple_accounts_flag == 1: beh += 35
    beh = min(beh, 100)

    final_risk = (
        (100 - trust_score) * 0.40 +
        beh * 0.40 +
        (20 if data.transaction_amount > 50000 else 0) * 0.20
    )
    final_risk = min(100, final_risk)

    if final_risk > 70:
        action = "BLOCK"
        risk_cat = "HIGH RISK"
    elif final_risk > 40:
        action = "REVIEW"
        risk_cat = "MEDIUM RISK"
    else:
        action = "ALLOW"
        risk_cat = "LOW RISK"

    return trust_score, beh, final_risk, action, risk_cat

@app.post("/register")
def register_user(data: UserData):
    try:
        trust_score, beh_score, final_risk, action, risk_cat = calculate_scores(data)
        
        entity_id = f"USR{str(uuid.uuid4())[:8].upper()}"

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO users 
            (entity_id, entity_type, country_code, kyc_verified,
             trust_score, final_risk_score, risk_category, action, created_at)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            entity_id,
            data.entity_type,
            data.country_code,
            data.kyc_verified,
            trust_score,
            final_risk,
            risk_cat,
            action,
            datetime.now()
        ))

        conn.commit()
        cursor.close()   # ✅ FIX 3
        conn.close()

        return {
            "entity_id": entity_id,
            "trust_score": trust_score,
            "behavioral_score": beh_score,
            "final_risk_score": final_risk,
            "risk_category": risk_cat,
            "action": action
        }

    except Exception as e:
        return {"error": str(e)}

@app.get("/users")
def get_all_users():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users ORDER BY created_at DESC")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return {"users": rows}

@app.get("/stats")
def get_stats():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    total = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM users WHERE action='BLOCK'")
    blocked = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM users WHERE action='ALLOW'")
    allowed = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM users WHERE action='REVIEW'")
    review = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return {
        "total": total,
        "blocked": blocked,
        "allowed": allowed,
        "review": review
    }

@app.get("/")
def health():
    return {"status": "Nexport API Running! 🚀"}
