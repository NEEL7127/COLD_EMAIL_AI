# main.py — Cold Email AI Backend v3.0
# Unlimited for everyone (open source version)

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json, os
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from email_generator import generate_cold_email

app = FastAPI(title="Cold Email AI", version="3.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# DATABASE (Simple JSON file)
# {
#   "neel@gmail.com": {
#     "plan": "free",
#     "emails_used": 5,
#     "plan_start": "2026-03-11",
#     "plan_end": null,
#     "maintenance_paid_till": null
#   }
# }
# ============================================

DB_FILE = "users.json"

def load_db():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_db(data: dict):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_user(email: str) -> dict:
    db = load_db()
    if email not in db:
        db[email] = {
            "plan":                  "free",
            "emails_used":           0,
            "plan_start":            str(date.today()),
            "plan_end":              None,
            "maintenance_paid_till": None
        }
        save_db(db)
    return db[email]

def save_user(email: str, data: dict):
    db = load_db()
    db[email] = data
    save_db(db)


# ============================================
# PLAN CHECKER
# ============================================
def check_access(email: str) -> dict:
    user  = get_user(email)
    today = date.today()
    plan  = user["plan"]

    # FREE — unlimited for everyone
    if plan == "free":
        return {
            "can_generate": True,
            "plan":         "free",
            "emails_left":  999999
        }

    # MONTHLY
    if plan == "monthly":
        plan_end = datetime.strptime(user["plan_end"], "%Y-%m-%d").date()
        if today > plan_end:
            user["plan"] = "free"
            save_user(email, user)
            return {
                "can_generate": False,
                "plan":         "expired_monthly",
                "reason":       "subscription_expired"
            }
        return {
            "can_generate": True,
            "plan":         "monthly",
            "plan_end":     user["plan_end"]
        }

    # LIFETIME
    if plan == "lifetime":
        if user["maintenance_paid_till"] is None:
            return {
                "can_generate": True,
                "plan":         "lifetime"
            }
        maint_till = datetime.strptime(user["maintenance_paid_till"], "%Y-%m-%d").date()
        if today > maint_till:
            return {
                "can_generate": False,
                "plan":         "lifetime",
                "reason":       "maintenance_expired",
                "message":      "Your maintenance has expired. Please renew."
            }
        return {
            "can_generate":          True,
            "plan":                  "lifetime",
            "maintenance_paid_till": user["maintenance_paid_till"]
        }

    return {"can_generate": False, "reason": "unknown_plan"}


# ============================================
# REQUEST MODELS
# ============================================
class EmailRequest(BaseModel):
    linkedin_profile: str
    sender_name:      str
    sender_product:   str
    tone:             str = "professional"
    user_email:       str

class PaymentRequest(BaseModel):
    user_email: str
    payment_id: str
    plan:       str


# ============================================
# ROUTES
# ============================================

@app.get("/")
def home():
    return {"status": "✅ Cold Email AI v3.0 running!"}


@app.get("/user/{email}")
def get_user_info(email: str):
    email  = email.lower().strip()
    user   = get_user(email)
    access = check_access(email)
    return {
        "email":       email,
        "plan":        user["plan"],
        "emails_used": user["emails_used"],
        "access":      access
    }


@app.post("/generate-email")
def generate_email(request: EmailRequest):
    email = request.user_email.lower().strip()

    # Validate inputs only — NO access check (unlimited for everyone)
    if len(request.linkedin_profile.strip()) < 20:
        raise HTTPException(status_code=400, detail="LinkedIn profile too short. Paste more details.")
    if not request.sender_name.strip():
        raise HTTPException(status_code=400, detail="Sender name cannot be empty.")
    if not email:
        raise HTTPException(status_code=400, detail="Please enter your email.")

    # Generate the email
    result = generate_cold_email(
        linkedin_profile=request.linkedin_profile,
        sender_name=request.sender_name,
        sender_product=request.sender_product,
        tone=request.tone
    )

    # Track usage count (just for stats, not for blocking)
    user = get_user(email)
    user["emails_used"] += 1
    save_user(email, user)

    return {
        "success": True,
        "subject": result["subject"],
        "body":    result["body"],
        "access":  check_access(email)
    }


@app.post("/confirm-payment")
def confirm_payment(req: PaymentRequest):
    email = req.user_email.lower().strip()
    user  = get_user(email)
    today = date.today()

    if req.plan == "monthly":
        user["plan"]       = "monthly"
        user["plan_start"] = str(today)
        user["plan_end"]   = str(today + relativedelta(months=1))

    elif req.plan == "lifetime":
        user["plan"]                  = "lifetime"
        user["plan_start"]            = str(today)
        user["plan_end"]              = None
        user["maintenance_paid_till"] = str(today + relativedelta(months=1))

    elif req.plan == "maintenance":
        if user["plan"] != "lifetime":
            raise HTTPException(status_code=400, detail="Only lifetime users need maintenance.")
        current_end = user.get("maintenance_paid_till")
        if current_end:
            base = datetime.strptime(current_end, "%Y-%m-%d").date()
            if base < today:
                base = today
        else:
            base = today
        user["maintenance_paid_till"] = str(base + relativedelta(months=1))

    save_user(email, user)

    return {
        "success": True,
        "message": f"✅ Plan updated to {req.plan}!",
        "user":    user
    }