# 🐺 Wolfkit

**Try, Test, Trust.**

Wolfkit is a comprehensive AI-powered development tool that combines safe code testing with intelligent document organization and enterprise-grade security analysis. Test AI-generated code in real projects with automatic backups, analyze code quality before deployment, scan for vulnerabilities with zero-cost local analysis, and seamlessly cluster related documents using semantic AI.

**Current Version:** `v1.3.2` — Now with **Security Analysis & Enhanced Architecture**

---

## Table of Contents
- [What It Does](#-what-it-does)
- [New in v1.3.2](#-new-in-v132-security-analysis-revolution)
- [Quickstart](#-quickstart)
- [AI Setup](#-ai-features-setup)
- [Security Features](#-security-analysis-features)
- [Why Use Wolfkit?](#-why-use-wolfkit)
- [Full Feature List](#-complete-feature-set)
- [Workflows](#-enhanced-workflow-analyze--organize--secure--test--trust)
- [Architecture](#-architecture-overview)
- [Sample Report](#-sample-security-analysis-report)
- [Safety & Privacy](#-safety--data-privacy)
- [Roadmap](#-version-history--roadmap)
- [Costs](#-total-cost-transparency)
- [Use Cases](#-real-world-use-cases)
- [Contributing](#-contributing)
- [License](#-license)
- [About](#-built-by)

---

## ⚡ What It Does

### 🤖 **AI Code Review** 🔐
- Analyze LLM-generated code for syntax, logic, and import issues
- Multi-file batch support with markdown report generation
- Budget-conscious: gpt-4o-mini (~$0.002–0.005 per file)

### 📄 **Document Clustering & Merge** 🔐
- Organize mixed-format documents using semantic AI
- Smart merge previews with similarity scoring
- Merge outputs with suggested filenames

### 🛡️ **Security Analysis**
- OWASP Top 10 vulnerability scanning
- Framework-specific checks (FastAPI, Flask, Django, Express, etc.)
- Local-only, zero-cost analysis with professional-grade reports

### 🚀 **File Testing Workflow**
- Drop in test files and apply them to any project structure
- Auto-backups and virtualenv detection
- Accept/revert changes with one click

### 📚 **Built-in Documentation**
- Full user manual inside the app with step-by-step workflows
- Troubleshooting and instant navigation

---

## 🌟 New in v1.3.2: Security Analysis Revolution

**Enterprise-grade security scanning is here!**

- OWASP vulnerability detection across frameworks
- Local-only analysis, zero dependencies
- Risk scoring and CWE-classified reports
- Seamless UI integration with BaseTab

For full details, see the [Security Analysis Tab](#-security-analysis-tab---new).

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

# 4. Set up .env if using AI features (see below)
cp .env.example .env

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

## 🤖 AI Features Setup 🔐

Only needed for Code Review and Document Merge.

1. Get your OpenAI API key from https://platform.openai.com/api-keys
2. Add to `.env`:
```bash
OPENAI_API_KEY=sk-your-key-here
```
3. Optionally select model:
```bash
OPENAI_MODEL=gpt-4o-mini
```

### Model Cost Estimates
| Model | Per File | Best For |
|-------|----------|----------|
| gpt-4o-mini | ~$0.002–0.005 | Great quality & speed |
| gpt-4.1-nano | ~$0.001–0.003 | Ultra-budget option |
| gpt-4o | ~$0.03–0.07 | Premium results |

---

## 🛡️ Security Analysis Features

Covers OWASP Top 10, with custom scanners per framework. No internet or API key required.

- Critical: SQLi, XSS, hardcoded keys, weak crypto
- Framework insights: e.g., FastAPI missing CORS/auth, Flask missing `SECRET_KEY`
- Risk scoring: 0–100 with CWE references and summaries
- Export to Markdown, HTML, or JSON

---

## 🤔 Why Use Wolfkit?

Modern developers deal with:
- AI-generated code with subtle bugs
- Security risks hidden in large codebases
- Duplicate or scattered documentation
- Time wasted on manual testing

**Wolfkit = sanity, speed, and safety.**

1. Analyze →
2. Organize →
3. Secure →
4. Test →
5. Trust

---

## 🛠️ Complete Feature Set

### 🤖 Code Review Tab 🔐
- Batch analyze files
- Generate and save markdown reports
- Tracks config status and opens reports in your default editor

### 📄 Document Merge Tab 🔐
- Cluster and merge files by meaning
- Preview clusters and similarity
- Merge results with editable names

### 🛡️ Security Analysis Tab
- Scan project directories
- Filter by severity
- Risk scoring + exportable results

### 🚀 File Testing Tab
- Replace or add files with full control
- Launch Python apps or static HTML
- Accept or revert with auto-backups

### 📚 Documentation Tab
- Fully built-in manual
- Workflow guidance and troubleshooting

---

## 🧪 Enhanced Workflow: Analyze → Organize → Secure → Test → Trust

> Use only what you need. Skip what you don't.

### For Code:
1. 🤖 Review with AI
2. 🚀 Test in target project
3. 🛡️ Scan for security flaws

### For Documents:
1. 📄 Drop in a messy folder
2. 🤖 Cluster & merge
3. 🔖 Export clean results

### For Security:
1. 🔹 Scan the codebase
2. 🔢 Get risk score & summary
3. 🔄 Fix & re-scan

---

## 📏 Architecture Overview

```
wolfkit/
├── main.py
├── controller.py
├── code_reviewer.py           # 🔐
├── document_merger.py         # 🔐
├── security_analyzer.py
├── security_patterns.py
├── security_reporter.py
├── ui/
│   ├── app_frame.py
│   ├── base_tab.py
│   ├── ... (tabs)
│   └── widgets/
├── assets/
├── backups/
├── reports/
├── requirements.txt
└── README.md
```

**Notes:**
- Security engine uses only standard Python
- All major modules under 400 LOC
- Reports saved to `/reports/`

---

## 📄 Sample Security Report

```markdown
# 🛡️ Security Analysis Report
Generated: 2025-07-14
Score: 67/100 — HIGH

Findings:
- 🚨 Hardcoded API keys
- ⚠️ 5 unprotected endpoints
- 🔔 Missing CORS config

Actions:
- Move keys to env vars
- Add auth middleware
- Configure secure CORS
```

---

## 🛡️ Safety & Privacy
- AI-powered features send metadata only (not code/content)
- OpenAI does not retain inputs (per API TOS)
- Backups and reverts built into test workflow
- Local-only analysis for security scanning

---

## 🚀 Version History & Roadmap

### v1.3.2 – Security Revolution
- Security scanner with OWASP detection
- Zero-dependency implementation
- Full risk reports with scoring

### v1.3.1 – Enhanced UX
- UI restructured
- Navigation bug fixes

### v1.3.0 – Feature Foundation
- Code review + clustering
- Batch file testing
- Markdown reporting

### Coming Soon
- Dependency CVE lookup
- CI/CD hooks
- Custom scan rules
- Inline annotations

---

## 💰 Total Cost Transparency

| User Type | Est. Monthly Cost |
|-----------|-------------------|
| Light | ~$2–3 |
| Active | ~$8–12 |
| Power | ~$30–50 |

- No subscriptions
- No storage fees
- Security tools are **FREE**
- AI features = **pay-as-you-go**

---

## 🌍 Real-World Use Cases

### Developers
- Safely test LLM code
- Avoid logic bugs and missing imports
- Organize scattered notes or API docs

### Security Teams
- Run compliance scans in seconds
- Generate client-ready vulnerability reports

### Content Creators
- Merge articles, outlines, transcripts
- Clean up multi-version content messes

### Professionals
- Consolidate resumes, contracts, training docs

---

## 🤝 Contributing

PRs welcome! Please:
- Follow existing code style
- Include tests where possible
- Use type hints in all new code

Setup:
```bash
git clone https://github.com/your-username/wolfkit.git
cd wolfkit
python -m venv dev-env
source dev-env/bin/activate
pip install -r requirements.txt
python main.py
```

---

## 📄 License
MIT — see LICENSE file for details.

---

## 💬 Built By

A developer who got tired of:
- Breaking code with LLM hallucinations
- Worrying about hidden vulnerabilities
- Drowning in 15 versions of the same file

**If that’s you, Wolfkit is for you.**

---

## 🚀 Ready to Try It?

```bash
git clone https://github.com/your-username/wolfkit.git
cd wolfkit
pip install -r requirements.txt
python main.py
```

**Try it. Test it. Secure it. Trust it.** 🐺

