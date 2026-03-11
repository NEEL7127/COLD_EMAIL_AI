# 🤖 Cold Email AI

> Paste any LinkedIn profile → get a hyper-personalized cold email in seconds.

Built with **FastAPI + Groq API (Llama 3) + HTML/CSS/JS** — completely free to run.

---

## ✨ Features

- 📋 Paste LinkedIn profile → AI writes personalized cold email
- 🎭 4 tone options — Professional, Casual, Bold, Humble
- ⚡ Powered by Groq (Llama 3.3 70B) — free and fast
- 💾 Tracks emails generated per user
- 📋 One-click copy to clipboard
- 🔄 Regenerate different versions instantly
- 🌐 Pure HTML frontend — no React, no npm needed

---

## 🚀 Setup (5 minutes)

### Step 1 — Get Free Groq API Key
1. Go to [console.groq.com](https://console.groq.com)
2. Sign up free (no credit card)
3. Click **API Keys → Create API Key**
4. Copy the key

### Step 2 — Clone & Install
```bash
git clone https://github.com/NEEL7127/COLD_EMAIL_AI 
cd cold-email-ai/backend
pip install -r requirements.txt
```

### Step 3 — Add Your API Key
Create a `.env` file inside `/backend`:
```
GROQ_API_KEY=your_groq_key_here
```

### Step 4 — Run Backend
```bash
uvicorn main:app --reload
```
Server starts at `http://localhost:8000`

### Step 5 — Open Frontend
Just double-click `frontend/cold-email-ai.html` in your browser.

**That's it. You're ready to go!** 🎉

---

## 📁 Project Structure

```
cold-email-ai/
│
├── backend/
│   ├── email_generator.py   ← AI brain (Groq + Llama 3)
│   ├── main.py              ← FastAPI server
│   ├── requirements.txt     ← Python dependencies
│   └── .env                 ← Your API key (create this yourself)
│
├── frontend/
│   └── cold-email-ai.html   ← Full UI (single file)
│
└── README.md
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| AI Model | Llama 3.3 70B via Groq API |
| Backend | FastAPI (Python) |
| Frontend | HTML + CSS + Vanilla JS |
| Database | JSON file (users.json) |
| Payments | Razorpay / UPI (optional) |

---

## 💡 How It Works

```
User pastes LinkedIn profile text
            ↓
FastAPI receives the request
            ↓
Groq API (Llama 3) generates personalized email
            ↓
Subject + Body returned to frontend
            ↓
User copies and sends the email
```

---

## 🔧 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Health check |
| GET | `/user/{email}` | Get user plan info |
| POST | `/generate-email` | Generate cold email |
| POST | `/confirm-payment` | Activate paid plan |

Full API docs at `http://localhost:8000/docs` (Swagger UI)

---

## 📸 Screenshots

> Add your screenshots here after running the project!

---

## 🤝 Contributing

Pull requests are welcome! Feel free to open issues for bugs or feature requests.

---

## 📄 License

MIT License — free to use, modify and distribute.

---

## 👨‍💻 Built By

**Neel Deshmane** — Diploma Computer Engineering Student | Aspiring AI & ML Engineer


