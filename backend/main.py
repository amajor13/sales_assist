# backend/main.py
from fastapi import FastAPI
from pydantic import BaseModel
import local_ai as llm
from fastapi.middleware.cors import CORSMiddleware
from emailer import send_email  # <-- import your emailer

app = FastAPI()

# Allow frontend (localhost:3000) to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict later to ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- CHAT ----------
class ChatRequest(BaseModel):
    text: str

@app.post("/chat")
async def chat(req: ChatRequest):
    response = llm.classify_reply(req.text)
    return {
        "reply": f"Bot thinks: {response['label']} (reason: {response['reason']})",
        "intent": response.get("label", "unknown"),
        "reason": response.get("reason", "n/a"),
    }

# ---------- EMAIL ----------
class EmailRequest(BaseModel):
    to_email: str
    subject: str
    template: str
    personalization: dict  # e.g. {"name": "Ashutosh", "company": "Visa"}

@app.post("/send_email")
async def send_email_api(req: EmailRequest):
    # Replace placeholders in template
    body = req.template
    for key, value in req.personalization.items():
        body = body.replace(f"{{{key}}}", value)

    # Send email using your existing emailer.py
    status = send_email(req.to_email, req.subject, body)

    if status == "sent":
        return {"success": True, "message": f"Email sent to {req.to_email}"}
    else:
        return {"success": False, "message": "Email sending failed"}
