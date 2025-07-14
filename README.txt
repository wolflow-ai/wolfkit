# 🐺 Wolfkit

**Try, Test, Trust.**

Wolfkit is a powerful AI-powered desktop app that helps developers and teams test LLM-generated code, merge and organize documents, and scan projects for security issues with clarity and confidence. 

Everything happens on your machine — with clear boundaries and full control.

**Current Version:** `v1.3.2` — Now with **Security Analysis & Enhanced Architecture**

---

## ⚡ What It Does

### 🧠 AI Code Review
- Analyze LLM-generated code for syntax, logic, and import issues
- Multi-file batch support with markdown report generation
- Requires OpenAI API key (nothing uploaded, just prompts)
- Uses `gpt-4o-mini` (~$0.002–0.005 per file)

### 📄 Document Clustering & Merge
- Organize mixed-format documents using semantic AI
- Smart merge previews with similarity scoring
- Supports TXT, MD, DOCX, PDF, source files, and more
- Requires OpenAI API key (document content is summarized, not uploaded)

### 🛡️ Security Analysis (New!)
- OWASP Top 10 vulnerability scanning
- Framework-specific checks (FastAPI, Flask, Django, Express, etc.)
- Local file analysis only — code is not uploaded
- **Requires OpenAI API key** to generate insights
- Professional reports with CWE tags, severity levels, and score (0–100)

### 🚀 File Testing Workflow
- Drop in test files and apply them to any project structure
- Auto-backups and virtualenv detection
- Accept/revert changes with one click

### 📚 Built-in Documentation
- Full user manual inside the app
- Step-by-step workflows and troubleshooting

---

## 🚀 Quickstart

```bash
# 1. Clone the repo
git clone https://github.com/your-username/wolfkit.git
cd wolfkit

# 2. Create and activate a virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up .env (for AI features)
cp .env.example .env
# Add your OpenAI API key

# 5. Launch the app
python main.py
```

### ▶️ Windows Shortcut
```bat
@echo off
cd /d %~dp0
call venv\Scripts\activate.bat
start "" pythonw main.py > log.txt 2>&1
```

---

## 🚧 AI Features Setup

### ✅ Required For:
- Code Review tab
- Document Merge tab
- Security Analysis tab

### 🔑 Setup Instructions
1. Get an OpenAI API key from [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Add it to your `.env` file:
```bash
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini
```

### 🎁 Model Costs
| Model         | Est. Cost per File | Notes                 |
|---------------|--------------------|------------------------|
| `gpt-4o-mini` | ~$0.002–0.005      | Best mix of cost + quality |
| `gpt-4.1-nano`| ~$0.001–0.003      | Budget option         |
| `gpt-4o`      | ~$0.03–0.07        | Premium pricing       |

> Documents and code are never uploaded — only structured prompts are sent.

---

## 🛡️ Security Analysis Features

### 🔍 What It Does
- Detects OWASP Top 10 vulnerabilities (SQLi, XSS, hardcoded secrets, CORS issues, etc.)
- Scores your project 0–100 with severity breakdown
- Uses tailored checks per framework (FastAPI, Flask, Django, Express, etc.)
- Generates clean, exportable reports (Markdown, HTML, JSON)

### ⚠️ API Key Required
Security analysis is performed locally on your machine, but it uses OpenAI to generate security reports. This means:
- Your actual code is **never sent**
- **Structured summaries** (like "this file has an open API route") are used as prompts
- All findings are stored in the `/reports/` folder

---

## 🤔 Why Use Wolfkit?

Modern development moves fast — and LLMs move even faster. But speed often comes with risks:
- Subtle bugs or security flaws
- Confusing document sprawl
- Fear of breaking existing code

Wolfkit helps you:
- Analyze LLM code before trusting it
- Organize your files with clarity
- Scan for vulnerabilities before you deploy

One app. Five verbs: **Analyze → Organize → Secure → Test → Trust.**

---

## 📊 Sample Report

```markdown
# 🛡️ Security Analysis Report
Generated: 2025-07-14
Score: 67/100 — HIGH

Findings:
- 🚨 Hardcoded API keys
- ⚠️ 5 unprotected endpoints
- 🔔 Missing CORS config

Recommended Actions:
- Move keys to environment variables
- Add auth middleware
- Configure secure CORS
```

---

## 🔒 Safety & Privacy
- Code and documents are analyzed **locally**
- Only prompts (not raw files) are sent to OpenAI
- OpenAI does **not retain data** per their API terms
- No user tracking, storage, or telemetry
- Security scans are performed on your machine, not in the cloud

---

## 🚧 Folder Structure
```
wolfkit/
├── main.py
├── controller.py
├── code_reviewer.py
├── document_merger.py
├── security_analyzer.py
├── security_patterns.py
├── security_reporter.py
├── ui/
│   ├── app_frame.py
│   ├── base_tab.py
│   ├── ...
├── reports/
├── backups/
├── requirements.txt
└── .env.example
```

---

## 💼 License
MIT — Use it freely.

---

## 🚀 Try It Today
```bash
git clone https://github.com/your-username/wolfkit.git
cd wolfkit
pip install -r requirements.txt
python main.py
```

**Try it. Test it. Secure it. Trust it.** 🐺
