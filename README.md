# 🐺 Wolfkit

**Try, Test, Trust.**

Wolfkit is a comprehensive AI-powered development tool that combines safe code testing with intelligent document organization and enterprise-grade security analysis. Test AI-generated code in real projects with automatic backups, analyze code quality before deployment with **multi-file context awareness**, scan for vulnerabilities with AI-powered insights, and seamlessly cluster related documents using semantic AI. **Now includes file size monitoring to catch oversized files before they become maintenance problems.**

**Current Version:** `v1.4.1` — Now with **File Size Analysis & Monitoring**

---

## Table of Contents
- [What It Does](#-what-it-does)
- [🆕 New in v1.4.1](#-new-in-v141-file-size-analysis)
- [Quickstart](#-quickstart)
- [AI Setup](#-ai-features-setup)
- [Multi-File Analysis](#-multi-file-analysis-features)
- [File Size Monitoring](#-file-size-monitoring-features)
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

### 🤖 **AI Code Review** 🔐 **Enhanced with File Size Analysis**
- **Three Analysis Modes**: Single file, Module analysis, and Project-level architectural review
- **Smart Dependency Detection**: Identifies missing imports available in other files
- **File Size Monitoring**: Configurable thresholds to catch oversized files
- **Framework Intelligence**: Auto-detects FastAPI, Flask, Django, React, Vue, Express
- Professional markdown reports with comprehensive project insights

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

## 🆕 New in v1.4.1: File Size Analysis

### 📏 **File Size Monitoring**
Keep your codebase maintainable by monitoring file sizes and getting alerts when files grow too large.

### **Key Features:**
- **Configurable Thresholds**: Choose from preset limits or define custom values
- **Explicit Problem Identification**: Clear alerts for files that exceed size limits
- **Smart Refactoring Suggestions**: Context-aware recommendations for splitting large files
- **Quick Size Check**: Instant file size analysis without full AI review
- **Integrated Reporting**: File size analysis included in all code review reports

### **Threshold Presets:**
- **Strict**: Optimal ≤250, Warning 500+, Critical 700+ lines
- **Standard**: Optimal ≤400, Warning 800+, Critical 1200+ lines (Recommended)
- **Relaxed**: Optimal ≤600, Warning 1000+, Critical 1500+ lines
- **Legacy**: Optimal ≤800, Warning 1500+, Critical 2000+ lines
- **Custom**: Define your own thresholds

### **Sample Output:**
```
🚨 DANGEROUS FILES (>1200 lines) - IMMEDIATE ACTION REQUIRED:
• models.py (1,247 lines) - 647 lines over optimal limit
  └─ Split into separate model files by domain

⚠️  WARNING FILES (600-800 lines) - SHOULD BE REFACTORED:
• api_handlers.py (743 lines) - 343 lines over optimal limit
  └─ Split endpoints by feature area into separate files
```

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
- **Code Review tab** 🔐 (All analysis modes)
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
| Model | Per File | Per Module (5 files) | Per Project (50 files) | Best For |
|-------|----------|---------------------|------------------------|----------|
| `gpt-4o-mini` | ~$0.002–0.005 | ~$0.01–0.02 | ~$0.05–0.15 | **Recommended**: Great quality & speed |
| `gpt-4.1-nano` | ~$0.001–0.003 | ~$0.005–0.015 | ~$0.03–0.10 | Ultra-budget option |
| `gpt-4o` | ~$0.03–0.07 | ~$0.15–0.30 | ~$0.75–2.00 | Premium results |

> **Privacy Note**: Only structured analysis prompts and project context are sent to OpenAI. Your actual code stays local during analysis.

---

## 🔬 Multi-File Analysis Features

### 🎯 **Smart Dependency Detection**
| Feature | Description | Example |
|---------|-------------|---------|
| **Missing Import Detection** | Finds undefined symbols available in other files | `helper_function` in main.py available in utils.py |
| **Cross-file Validation** | Verifies function calls work across files | Validates API calls match endpoint definitions |
| **Framework Compliance** | Checks adherence to detected framework patterns | FastAPI route decorators, Flask app structure |
| **Circular Dependency Detection** | Identifies problematic import cycles | module_a imports module_b which imports module_a |

### 🧠 **Context-Aware Analysis**
```python
# Before: Single file analysis misses context
# main.py - ERROR: helper_function not defined
from config import DATABASE_URL
result = helper_function("data")  # ❌ Flagged as undefined

# After: Module analysis provides context
# ✅ Analysis Context:
# - helper_function available in utils.py
# - Suggested import: from utils import helper_function
# - Framework: FastAPI detected
# - Database: PostgreSQL detected from imports
```

---

## 📏 File Size Monitoring Features

### 🎯 **Proactive Code Quality**
File size monitoring helps maintain clean, readable codebases by catching oversized files before they become maintenance problems.

### **Analysis Integration:**
- **Single File**: Check individual file sizes during analysis
- **Module Analysis**: Monitor file sizes across related files with context
- **Project Analysis**: Comprehensive file size assessment for entire codebase
- **Quick Size Check**: Instant analysis without full AI review

### **Smart Suggestions:**
- **Context-Aware**: Suggestions based on file type and naming patterns
- **Actionable**: Specific recommendations for splitting files
- **Prioritized**: Focus on files that need immediate attention

### **Professional Reporting:**
- File size analysis section in all reports
- Visual indicators for problematic files
- Architecture health assessment
- Detailed refactoring roadmap

### **Configuration Options:**
- Enable/disable file size analysis
- Choose from preset thresholds or create custom limits
- Real-time threshold preview
- Settings persist across analysis sessions

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

### 📄 Professional Reporting
- **Executive Summary**: Management-focused risk assessment with business impact
- **Technical Details**: Developer-focused findings with code snippets and CWE references
- **Risk Scoring**: 0-100 scale considering severity, category, and confidence
- **Export Options**: Markdown, HTML, and JSON formats for documentation

---

## 🤔 Why Use Wolfkit?

Modern developers deal with:
- **AI-generated code** with subtle bugs and security vulnerabilities
- **Multi-file complexity** where issues span across modules
- **Security risks** hidden in large codebases
- **Document chaos** with duplicates and scattered content
- **Oversized files** that become maintenance nightmares
- **Risk anxiety** when deploying untested code changes

**Wolfkit = Confidence in your development workflow.**

### 🎯 The Complete Five-Phase Approach:
1. **🤖 Analyze** → Multi-file code review with cross-file context awareness and file size monitoring
2. **📄 Organize** → Cluster and merge related documents intelligently  
3. **🛡️ Secure** → Scan for vulnerabilities with professional insights
4. **🚀 Test** → Stage secure, reviewed code with automatic backups
5. **✅ Trust** → Deploy with confidence or revert instantly

---

## 🛠 Complete Feature Set

### 🤖 Code Review Tab 🔐 **Enhanced with File Size Analysis**
- **Three Analysis Modes**: Single file, Module, and Project analysis
- **Smart Context Building**: Framework detection and dependency mapping
- **Cross-file Validation**: Missing import detection and resolution
- **File Size Monitoring**: Configurable thresholds with explicit problem identification
- **Quick Size Check**: Instant file size analysis without full AI review
- **Professional Reports**: Enhanced markdown reports with project insights and file metrics
- **Configuration Management**: Persistent settings for thresholds and analysis options

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
- Updated with File Size Analysis documentation

---

## 🧪 Enhanced Workflow: Analyze → Organize → Secure → Test → Trust

> **Use only what you need. Skip what you don't.**

### **For Code Development:**
1. **🤖 Code Review**: 
   - **Single File**: Quick individual file analysis with size check
   - **Module**: Cross-file analysis with context awareness and size monitoring
   - **Project**: Full architectural review with comprehensive file size assessment
2. **📄 Document Merge**: Organize related project documentation  
3. **🛡️ Security Analysis**: Scan for vulnerabilities and get professional insights
4. **🚀 File Testing**: Stage secure, reviewed code with automatic backups
5. **✅ Trust**: Accept changes confidently or revert instantly

### **For File Size Management:**
1. **📏 Quick Size Check** → Instant assessment of file sizes across your project
2. **⚙️ Configure Thresholds** → Set limits that match your team's standards
3. **🔍 Identify Problems** → Get explicit alerts for files that need attention
4. **📋 Follow Suggestions** → Use context-aware refactoring recommendations
5. **📊 Track Progress** → Monitor file size health over time

---

## 📏 Architecture Overview

```
wolfkit/
├── main.py                      # Application entry point
├── controller.py                # Core business logic & workflow coordination
├── code_reviewer.py            # 🔐 Enhanced multi-file AI analysis orchestrator
├── file_metrics_analyzer.py    # 🆕 File size analysis and monitoring engine
├── dependency_mapper.py        # Import/export analysis and dependency graphs
├── code_context_analyzer.py    # Project structure analysis and context building
├── multi_file_analyzer.py      # Multi-file analysis coordination
├── document_merger.py          # 🔐 Document clustering and merging
├── security_analyzer.py        # 🔐 Local security vulnerability scanning
├── security_patterns.py        # Security pattern detection engine
├── security_reporter.py        # 🔐 Professional AI-powered report generation
├── ui/
│   ├── app_frame.py            # Main orchestrator with tab management
│   ├── base_tab.py             # Common tab functionality and utilities
│   ├── code_review_tab.py      # 🔐 Enhanced analysis interface with file size controls
│   ├── document_merge_tab.py   # 🔐 Document clustering interface
│   ├── security_analysis_tab.py # 🔐 Security scanning interface
│   ├── main_workflow_tab.py    # File staging and testing interface
│   ├── documentation_tab.py    # Built-in help system
│   └── widgets/
│       ├── cluster_card.py     # Custom cluster visualization
│       ├── console_output.py   # Reusable console widget
│       └── progress_tracker.py # Progress indication
├── assets/
├── backups/                    # Auto-generated file backups
├── reports/                    # AI analysis & security reports
└── requirements.txt
```

---

## 📄 Sample Reports

### **Enhanced Code Review Report with File Size Analysis**
```markdown
# Wolfkit AI Code Review (Module Analysis)
**Generated:** 2025-07-18 14:30:22
**Analysis Type:** Module
**Framework:** FastAPI
**Files Needing Size Attention:** 2
**Architecture Health:** CONCERNING

## Target Files
- `main.py` ⚠️
- `models.py` 🚨
- `utils.py`
- `config.py`

### Analysis Results
**Cross-File Issues Found:**
- ❌ main.py: 'helper_function' available in utils.py but not imported
- ✅ Strong FastAPI patterns detected

## 📏 File Size Analysis

### 🚨 Dangerous Files (>1200 lines)
| File | Lines | Over Optimal | Action Required |
|------|-------|--------------|-----------------|
| `models.py` | 1,247 | +847 | IMMEDIATE refactoring required |

### ⚠️ Warning Files (600-799 lines)  
| File | Lines | Over Optimal | Action Required |
|------|-------|--------------|-----------------|
| `main.py` | 743 | +343 | Should be refactored soon |

**Recommendations:**
1. **Immediate**: Split models.py into domain-specific files
2. **High Priority**: Add missing imports
3. **Medium Priority**: Extract API routes from main.py
```

---

## 🛡️ Safety & Data Privacy

### **What Stays Local:**
- ✅ **All source code** - never uploaded or transmitted
- ✅ **File size analysis** - completely local processing
- ✅ **Document content** - analyzed locally for clustering
- ✅ **Security vulnerability detection** - pattern matching on your machine
- ✅ **File backups** - stored in local `/backups/` directory
- ✅ **Dependency analysis** - AST parsing happens locally

### **What Uses AI (OpenAI API):**
- 🔐 **Code analysis prompts** - structured questions with project context
- 🔐 **Document clustering** - content summaries for semantic grouping
- 🔐 **Security report generation** - findings summaries for professional insights
- 🔐 **Report formatting** - structured data for executive summaries

### **Privacy Guarantees:**
- **No Raw Code Transmitted**: Only structured prompts and project context
- **File Size Analysis is Local**: No external API calls for size monitoring
- **OpenAI Data Policy**: No data retention per OpenAI API terms of service
- **Automatic Backups**: Every file replacement backed up until you accept changes
- **Reversible Operations**: All merges and staging operations can be undone
- **Local Reports**: All analysis saved to your `/reports/` directory

---

## 🚀 Version History & Roadmap

### ✅ v1.4.1 – File Size Analysis & Monitoring
- **File Size Monitoring**: Configurable thresholds to catch oversized files
- **Explicit Problem Identification**: Clear alerts for files needing attention
- **Smart Refactoring Suggestions**: Context-aware recommendations for splitting files
- **Quick Size Check**: Instant file size analysis without full AI review
- **Integrated Reporting**: File size analysis in all code review reports
- **Professional UI**: Clean settings panel with preset and custom thresholds
- **Zero Dependencies**: File size analysis uses only Python standard library

### ✅ v1.4.0 – Multi-File Analysis Revolution
- **Cross-file context awareness** for code review eliminates false positives
- **Three Analysis Modes**: Single file, Module analysis, and Project-level review
- **Smart Dependency Detection**: Missing import identification with suggestions
- **Framework Intelligence**: Auto-detection of FastAPI, Flask, Django, React, etc.
- **Professional Architecture**: Clean modular design with focused components

### ✅ v1.3.2 – Security Analysis Revolution
- **Comprehensive Security Analysis**: OWASP Top 10 vulnerability detection
- **Hybrid Architecture**: Local scanning + AI-powered professional reporting
- **Framework Intelligence**: Technology-specific security checks
- **Professional Reporting**: Executive summaries with technical details

---

## 💰 Cost Transparency

### 🔑 API Requirements Summary
| Feature | API Required | Typical Cost | Notes |
|---------|-------------|--------------|-------|
| 🤖 Code Review (Single) | ✅ OpenAI | ~$0.002-0.005/file | Traditional analysis |
| 🤖 Code Review (Module) | ✅ OpenAI | ~$0.01-0.02/module | Cross-file analysis |
| 🤖 Code Review (Project) | ✅ OpenAI | ~$0.05-0.15/project | Architectural review |
| 📏 File Size Analysis | ❌ None | **FREE** | Local processing only |
| 📄 Document Merge | ✅ OpenAI | ~$0.01-0.05/batch | Semantic clustering |
| 🛡️ Security Analysis | ✅ OpenAI | ~$0.01-0.03/scan | Professional reporting |
| 🚀 File Testing | ❌ None | **FREE** | Local file operations |
| 📚 Documentation | ❌ None | **FREE** | Built-in help system |

### 📊 Monthly Budget Examples (using gpt-4o-mini):
- **Light User**: 10 single + 5 module + 2 project reviews = ~$3-8/month
- **Active Developer**: 50 single + 20 module + 10 project reviews = ~$15-30/month  
- **Heavy User**: 200 single + 100 module + 50 project reviews = ~$50-100/month

### ✅ No Hidden Costs:
- **No subscription fees** - pay only for AI usage
- **File Size Analysis is FREE** - completely local processing
- **No per-user licensing** - single purchase, unlimited local use  
- **No data storage charges** - everything stored locally
- **Transparent billing** - direct OpenAI API usage tracking

---

## 🌍 Real-World Use Cases

### **For Developers:**
- **File Size Management**: Keep codebases maintainable with proactive size monitoring
- **Multi-Module Projects**: Analyze entire Flask/FastAPI applications with cross-file context
- **AI Code Integration**: Review ChatGPT/Claude-generated code across multiple files
- **Refactoring Projects**: Understand dependencies and file sizes before major restructuring
- **Code Quality Assurance**: Catch cross-file issues and oversized files early

### **For Development Teams:**
- **Code Standards Enforcement**: Set team-wide file size limits and monitor compliance
- **Technical Debt Management**: Identify and prioritize oversized files for refactoring
- **Code Review Process**: Enhanced PR reviews with architectural and size insights
- **Onboarding**: Help new developers understand project structure and standards

---

## 🤝 Contributing

Found a bug? Have a feature request? Want to contribute to the file size analysis engine?

### **How to Help:**
1. **Report Issues**: Check existing issues on GitHub, create detailed bug reports
2. **Feature Requests**: Suggest enhancements for file size monitoring or analysis
3. **Code Contributions**: PRs welcome for analysis improvements and new features
4. **Documentation**: Help improve user guides and troubleshooting
5. **Testing**: Help test file size analysis with different project structures

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
- **400-Line Limit**: Keep modules under 400 lines for maintainability (practice what we preach!)
- **Single Responsibility**: Each module/class should have one clear purpose
- **Local Processing**: Prefer local analysis over external API calls when possible
- **Graceful Fallbacks**: Handle missing dependencies and modules gracefully

---

## 📄 License

MIT License - Use freely in your own projects! See LICENSE file for details.

---

## 💬 Built By

A developer who got tired of:
- ✋ **Breaking working code** with AI-generated "improvements"
- 🤯 **Missing cross-file dependencies** that cause runtime errors
- 📏 **Maintaining massive files** that should have been split long ago
- 🔓 **Deploying vulnerabilities** hidden in complex codebases  
- 📄 **Managing chaos** across 15+ versions of the same document
- 🗂️ **Document sprawl** with duplicates and scattered content

If you build with LLMs, work with multi-file projects, care about code quality and maintainability, and want to **analyze intelligently**, **organize efficiently**, and **deploy confidently**...

**Wolfkit is for you.**

---

## 🚀 Get Started Today

```bash
git clone https://github.com/your-username/wolfkit.git
cd wolfkit
pip install -r requirements.txt
python main.py
```

**Try it. Test it. Analyze it. Trust it.** 🐺

---

*"The best code review is the one that understands your entire project and keeps your files maintainable. The best security analysis is the one that happens before you deploy. The best document organization is the one that happens automatically."*

**Star ⭐ this repo if Wolfkit's file size monitoring helps keep your codebase clean and maintainable!**