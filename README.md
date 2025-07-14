# 🐺 Wolfkit

**Try, Test, Trust.**

Wolfkit is a comprehensive AI-powered development tool that combines safe code testing with intelligent document organization and enterprise-grade security analysis. Test AI-generated code in real projects with automatic backups, analyze code quality before deployment, scan for vulnerabilities with AI-powered insights, and seamlessly cluster related documents using semantic AI.

**Current Version:** `v1.1.1` — Now with **Security Analysis & Enhanced Architecture**

---

## Table of Contents
- [What It Does](#-what-it-does)
- [New in v1.1.1](#-new-in-v111-security-analysis-revolution)
- [Quickstart](#-quickstart)
- [AI Setup](#-ai-features-setup)
- [Security Features](#-security-analysis-features)
- [Why Use Wolfkit?](#-why-use-wolfkit)
- [Complete Feature Set](#-complete-feature-set)
- [Enhanced Workflow](#-enhanced-workflow-analyze--organize--secure--test--trust)
- [Architecture Overview](#-architecture-overview)
- [Sample Reports](#-sample-reports)
- [Safety & Privacy](#-safety--data-privacy)
- [Version History & Roadmap](#-version-history--roadmap)
- [Cost Transparency](#-cost-transparency)
- [Real-World Use Cases](#-real-world-use-cases)
- [Contributing](#-contributing)
- [License](#-license)

---

## ⚡ What It Does

### 🤖 **AI Code Review** 🔐
- Analyze LLM-generated code for syntax, logic, and import issues
- Multi-file batch support with markdown report generation
- Budget-conscious: gpt-4o-mini (~$0.002–0.005 per file)

### 📄 **Document Clustering & Merge** 🔐
- Organize mixed-format documents using semantic AI
- Smart merge previews with similarity scoring
- Supports PDF, Word, Text, Markdown, Code files
- Merge outputs with suggested filenames

### 🛡️ **Security Analysis** 🔐
- OWASP Top 10 vulnerability scanning with local pattern detection
- Framework-specific checks (FastAPI, Flask, Django, Express, etc.)
- **Local code analysis** - your code never leaves your machine
- **AI-powered reporting** - professional insights and risk assessment
- Professional reports with CWE references and 0-100 risk scoring

### 🚀 **File Testing Workflow**
- Drop in test files and apply them to any project structure
- Auto-backups and virtualenv detection
- Accept/revert changes with one click

### 📚 **Built-in Documentation**
- Full user manual inside the app with step-by-step workflows
- Troubleshooting and instant navigation

---

## 🌟 New in v1.1.1: Security Analysis Revolution

**Enterprise-grade security scanning is here!**

- **Hybrid Architecture**: Local vulnerability detection + AI-powered insights
- **OWASP Coverage**: Comprehensive Top 10 vulnerability detection
- **Framework Intelligence**: Tailored analysis for FastAPI, Flask, Django, Express
- **Professional Reports**: Executive summaries with technical details and CWE references
- **Privacy-First**: Code analysis stays local, only insights sent for report generation
- **Seamless Integration**: Perfect fit into existing BaseTab architecture

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

# 4. Set up AI features (required for most features)
cp .env.example .env
# Edit .env and add your OpenAI API key

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

## 🤖 AI Features Setup

### 🔑 Required For:
- **Code Review tab** 🔐
- **Document Merge tab** 🔐
- **Security Analysis tab** 🔐

### ✅ Setup Instructions
1. Get an OpenAI API key from [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Add it to your `.env` file:
```bash
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4o-mini
```

### 💰 Model Cost Estimates
| Model | Per File | Best For |
|-------|----------|----------|
| `gpt-4o-mini` | ~$0.002–0.005 | **Recommended**: Great quality & speed |
| `gpt-4.1-nano` | ~$0.001–0.003 | Ultra-budget option |
| `gpt-4o` | ~$0.03–0.07 | Premium results |

> **Privacy Note**: Documents and code are analyzed locally. Only structured summaries and prompts are sent to OpenAI for insights and report generation.

---

## 🛡️ Security Analysis Features

### 🔍 Comprehensive Vulnerability Detection
| Category | Description | Examples |
|----------|-------------|----------|
| **Injection** | SQL injection, XSS, Command injection | Unsafe query construction, HTML rendering |
| **Broken Access Control** | Unprotected endpoints, missing auth | APIs without authentication decorators |
| **Cryptographic Failures** | Weak crypto, hardcoded secrets | MD5/SHA1 usage, API keys in source |
| **Security Misconfiguration** | Debug mode, insecure CORS | Production debugging, wildcard origins |
| **Framework Security** | Platform-specific issues | Missing Flask SECRET_KEY, FastAPI CORS |

### 🎯 Framework-Specific Intelligence
- **FastAPI**: Missing CORS middleware, no rate limiting, unprotected endpoints
- **Flask**: Missing SECRET_KEY, no CSRF protection, insecure sessions  
- **Django**: DEBUG=True in production, missing security middleware
- **Express**: Insecure middleware, missing helmet configuration
- **Generic**: Cross-platform security patterns and best practices

### 📊 Hybrid Analysis Approach
1. **Local Pattern Detection**: Vulnerability scanning happens on your machine
2. **Privacy Protection**: Your actual code never leaves your computer
3. **AI-Powered Insights**: Structured findings sent to OpenAI for professional reporting
4. **Professional Output**: Executive summaries with technical details and risk scoring

### 📄 Professional Reporting
- **Executive Summary**: Management-focused risk assessment with business impact
- **Technical Details**: Developer-focused findings with code snippets and CWE references
- **Risk Scoring**: 0-100 scale considering severity, category, and confidence
- **Export Options**: Markdown, HTML, and JSON formats for documentation

---

## 🤔 Why Use Wolfkit?

Modern developers deal with:
- **AI-generated code** with subtle bugs and security vulnerabilities
- **Security risks** hidden in large codebases
- **Document chaos** with duplicates and scattered content
- **Risk anxiety** when deploying untested code changes

**Wolfkit = Confidence in your development workflow.**

### 🎯 The Five-Phase Approach:
1. **🤖 Analyze** → Review code quality and logic before staging
2. **📄 Organize** → Cluster and merge related documents intelligently  
3. **🛡️ Secure** → Scan for vulnerabilities with professional insights
4. **🚀 Test** → Stage secure, reviewed code with automatic backups
5. **✅ Trust** → Deploy with confidence or revert instantly

---

## 🛠 Complete Feature Set

### 🤖 Code Review Tab 🔐
- Select files for AI analysis (independent of staging)
- One-click batch analysis with progress tracking
- Professional markdown reports saved to `/reports/`
- Configuration checking and status updates
- Cross-platform report opening in default editor

### 📄 Document Merge Tab 🔐
- Select folder for document analysis and clustering
- Configure clustering (manual count or auto-detection)
- Visual cluster cards with similarity scores and previews
- In-app merge previews with expandable document lists
- Editable merge filenames with smart suggestions
- One-click merging with output directory selection

### 🛡️ Security Analysis Tab 🔐
- Select codebase directory for comprehensive scanning
- Configure analysis options (dependencies, config files, severity filters)
- Real-time progress tracking with framework detection
- Professional risk assessment with 0-100 scoring
- Export detailed reports with executive summaries
- Local code analysis with AI-powered professional insights

### 🚀 File Testing Tab
- Set target project directory with auto-detection
- Select one or more test files for staging
- Choose where to replace existing files or add new ones
- Automatic backup of any replaced files
- Launch your project (Python app or static web page)
- Accept or revert the entire test batch with one click

### 📚 Documentation Tab
- Complete user manual built into the app
- Quick navigation to specific features with visual feedback
- Step-by-step workflows for all major operations
- Troubleshooting guide and best practices
- Updated with Security Analysis documentation

---

## 🧪 Enhanced Workflow: Analyze → Organize → Secure → Test → Trust

> **Use only what you need. Skip what you don't.**

### **For Code Development:**
1. **🤖 Code Review**: Analyze LLM-generated code for syntax and logic issues
2. **📄 Document Merge**: Organize related project documentation  
3. **🛡️ Security Analysis**: Scan for vulnerabilities and get professional insights
4. **🚀 File Testing**: Stage secure, reviewed code with automatic backups
5. **✅ Trust**: Accept changes confidently or revert instantly

### **For Document Organization:**
1. **📁 Select Document Folder** with mixed/duplicate files
2. **🔍 Analyze Documents** → AI finds semantic clusters
3. **👀 Review Clusters** → See similarity scores and merge previews
4. **✏️ Edit Merge Names** → Customize output filenames
5. **🔄 Merge Selected** → Choose clusters to consolidate

### **For Security Auditing:**
1. **📂 Select Codebase** → Choose project directory for analysis
2. **⚙️ Configure Scan** → Set options and severity filters
3. **🔍 Run Analysis** → Local vulnerability detection + AI insights
4. **📊 Review Results** → Professional risk scoring and detailed findings
5. **📄 Export Report** → Executive summaries for compliance documentation

---

## 📏 Architecture Overview

```
wolfkit/
├── main.py                    # Application entry point
├── controller.py              # Core business logic & workflow coordination
├── code_reviewer.py           # 🔐 AI-powered code analysis
├── document_merger.py         # 🔐 Document clustering and merging
├── security_analyzer.py      # 🔐 Local security vulnerability scanning
├── security_patterns.py      # Security pattern detection engine
├── security_reporter.py      # 🔐 Professional AI-powered report generation
├── ui/
│   ├── app_frame.py          # Main orchestrator with tab management
│   ├── base_tab.py           # Common tab functionality and utilities
│   ├── code_review_tab.py    # 🔐 AI analysis interface
│   ├── document_merge_tab.py # 🔐 Document clustering interface
│   ├── security_analysis_tab.py # 🔐 Security scanning interface
│   ├── main_workflow_tab.py  # File staging and testing interface
│   ├── documentation_tab.py  # Built-in help system
│   └── widgets/
│       ├── cluster_card.py   # Custom cluster visualization
│       ├── console_output.py # Reusable console widget
│       └── progress_tracker.py # Progress indication
├── assets/
├── backups/                  # Auto-generated file backups
├── reports/                  # AI analysis & security reports
└── requirements.txt
```

### **Key Design Principles:**
- **Clean Architecture**: BaseTab inheritance with single responsibility
- **Privacy-First**: Local analysis with selective AI integration
- **Type Safety**: Comprehensive type hints throughout
- **Modular Design**: Each feature in its own focused module
- **Professional Output**: Enterprise-grade reporting and documentation

---

## 📄 Sample Reports

### **Code Review Report**
```markdown
# Wolfkit AI Code Review
**Generated:** 2025-07-14 15:45:12
**Files Analyzed:** 3
**Model Used:** gpt-4o-mini

---

### Analysis of `auth.py`
**File Type:** Python
**Syntax Check:** ❌ Issues found

**Issues Found:**
- ❌ [Critical Issue]: Missing import for `bcrypt` module
- ⚠️ [Warning]: Hardcoded salt value detected
- ✅ [Good Practice Found]: Proper password validation logic

**Summary:**
Add bcrypt import and move salt to environment variables.
```

### **Security Analysis Report**
```markdown
# 🛡️ Wolfkit Security Analysis Report
**Generated:** 2025-07-14 15:45:12
**Codebase:** `my-fastapi-project`
**Framework:** FastAPI
**Files Scanned:** 47

## 🚨 Security Status: **HIGH** (Score: 67/100)

| Severity | Count |
|----------|--------|
| 🔴 **Critical** | 2 |
| 🟠 **High** | 5 |
| 🟡 **Medium** | 12 |
| **Total** | 19 |

### Executive Summary
The security analysis reveals a HIGH risk level requiring immediate 
attention for 2 critical hardcoded API keys and 5 unprotected endpoints.

### Immediate Actions Required:
- 🚨 Move API keys to environment variables
- ⚠️ Add authentication to admin endpoints  
- 🔧 Configure CORS middleware properly
```

---

## 🛡️ Safety & Data Privacy

### **What Stays Local:**
- ✅ **All source code** - never uploaded or transmitted
- ✅ **Document content** - analyzed locally for clustering
- ✅ **Security vulnerability detection** - pattern matching on your machine
- ✅ **File backups** - stored in local `/backups/` directory

### **What Uses AI (OpenAI API):**
- 🔐 **Code analysis prompts** - structured questions about code quality
- 🔐 **Document clustering** - content summaries for semantic grouping
- 🔐 **Security report generation** - findings summaries for professional insights
- 🔐 **Report formatting** - structured data for executive summaries

### **Privacy Guarantees:**
- **No Raw Code Transmitted**: Only structured prompts and findings summaries
- **OpenAI Data Policy**: No data retention per OpenAI API terms of service
- **Automatic Backups**: Every file replacement backed up until you accept changes
- **Reversible Operations**: All merges and staging operations can be undone
- **Local Reports**: All analysis saved to your `/reports/` directory

---

## 🚀 Version History & Roadmap

### ✅ v1.1.1 – Security Analysis Revolution
- **Comprehensive Security Analysis**: OWASP Top 10 vulnerability detection
- **Hybrid Architecture**: Local scanning + AI-powered professional reporting
- **Framework Intelligence**: FastAPI, Flask, Django specific security checks
- **Professional Reporting**: Executive summaries with technical details
- **Enhanced Documentation**: Complete Security Analysis user guide
- **Improved Launch**: Better Windows batch launcher with console/silent modes

### ✅ v1.1.0 – Enhanced Features
- **Launch Type Selection**: Python App or Static Web Page options
- **Destination Folder Support**: Choose where to add new files
- **Project Structure Management**: Improved file staging workflow
- **Enhanced README**: Comprehensive feature documentation

### ✅ v1.0.0 – Foundation
- **Core File Testing**: Snapshotting, staging, backup, and rollback
- **Console Output**: Simple feedback and status tracking
- **Initial Release**: Basic workflow for safe code testing

### 🔮 Coming Soon (v1.2.0+)
- [ ] **Custom Security Patterns**: User-defined vulnerability rules
- [ ] **Dependency CVE Scanning**: Integration with known vulnerability databases
- [ ] **CI/CD Integration**: Hooks for automated security scanning
- [ ] **Enhanced Cluster Visualization**: Security risk indicators for documents
- [ ] **Team Collaboration**: Shared security findings and reports

### 🌟 Advanced Features (v2.0+)
- [ ] **Real-time Security Monitoring**: Live analysis during development
- [ ] **IDE Integration**: VS Code extension with security feedback
- [ ] **Enterprise Features**: SSO, team management, compliance frameworks
- [ ] **API Integration**: Security orchestration platform connectivity

---

## 💰 Cost Transparency

### 🔑 API Requirements Summary
| Feature | API Required | Typical Cost |
|---------|-------------|--------------|
| 🤖 Code Review | ✅ OpenAI | ~$0.002-0.005/file |
| 📄 Document Merge | ✅ OpenAI | ~$0.01-0.05/batch |
| 🛡️ Security Analysis | ✅ OpenAI | ~$0.01-0.03/scan |
| 🚀 File Testing | ❌ None | **FREE** |
| 📚 Documentation | ❌ None | **FREE** |

### 📊 Monthly Budget Examples (using gpt-4o-mini):
- **Light User**: 20 code reviews + 5 document merges + 10 security scans = ~$3-5/month
- **Active Developer**: 100 code reviews + 20 document merges + 30 security scans = ~$10-15/month  
- **Heavy User**: 500 code reviews + 100 document merges + 100 security scans = ~$40-60/month

### ✅ No Hidden Costs:
- **No subscription fees** - pay only for AI usage
- **No per-user licensing** - single purchase, unlimited local use  
- **No data storage charges** - everything stored locally
- **Transparent billing** - direct OpenAI API usage tracking

---

## 🌍 Real-World Use Cases

### **For Developers:**
- **Safe LLM Testing**: Review ChatGPT/Claude-generated code before deployment
- **Security-First Development**: Scan for vulnerabilities during development
- **Documentation Organization**: Merge scattered API docs and technical notes
- **Code Quality Assurance**: Catch syntax and logic errors early

### **For Security Teams:**
- **Regular Vulnerability Assessment**: Professional scanning without external tools
- **Compliance Documentation**: Executive-ready security reports
- **Framework-Specific Audits**: Tailored analysis for your technology stack
- **Risk Management**: Quantified security scoring for management reporting

### **For Content Creators:**
- **Document Consolidation**: Merge multiple article drafts and research notes
- **Content Organization**: Cluster interview transcripts and meeting notes
- **Asset Management**: Clean up duplicate files and organize by topic

### **For Professionals:**
- **Document Management**: Organize resume versions, contracts, proposals
- **Knowledge Base**: Consolidate training materials and documentation
- **Project Organization**: Merge related documents by semantic similarity

---

## 🤝 Contributing

Found a bug? Have a feature request? Want to contribute?

### **How to Help:**
1. **Report Issues**: Check existing issues on GitHub, create detailed bug reports
2. **Feature Requests**: Suggest enhancements with use case descriptions  
3. **Code Contributions**: PRs welcome for bug fixes and improvements
4. **Documentation**: Help improve user guides and troubleshooting

### **Development Setup:**
```bash
# Fork and clone the repo
git clone https://github.com/your-username/wolfkit.git
cd wolfkit

# Create development environment
python -m venv dev-env
source dev-env/bin/activate  # or dev-env\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

### **Code Standards:**
- **Type Hints Required**: All new code must include comprehensive type annotations
- **Single Responsibility**: Each module/class should have one clear purpose
- **Local Imports**: Heavy dependencies should use local imports for startup performance
- **Error Handling**: Graceful fallbacks with user-friendly error messages
- **Privacy-First**: Minimize data transmission, maximize local processing

---

## 📄 License

MIT License - Use freely in your own projects! See LICENSE file for details.

---

## 💬 Built By

A developer who got tired of:
- ✋ **Breaking working code** with AI-generated "improvements"
- 🔓 **Deploying vulnerabilities** hidden in complex codebases  
- 📄 **Managing chaos** across 15+ versions of the same document
- 🐛 **Debugging issues** that could be caught before staging
- 🗂️ **Document sprawl** with duplicates and scattered content

If you build with LLMs, care about security, work with multiple document versions, and want to **analyze safely**, **organize intelligently**, and **deploy confidently**...

**Wolfkit is for you.**

---

## 🚀 Get Started Today

```bash
git clone https://github.com/your-username/wolfkit.git
cd wolfkit
pip install -r requirements.txt
python main.py
```

**Try it. Test it. Secure it. Trust it.** 🐺

---

*"The best code review is the one that happens before you deploy. The best security analysis is the one that happens before you stage. The best document organization is the one that happens automatically."*

**Star ⭐ this repo if Wolfkit enhances your development workflow!**