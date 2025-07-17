# 🐺 Wolfkit

**Try, Test, Trust.**

Wolfkit is a comprehensive AI-powered development tool that combines safe code testing with intelligent document organization and enterprise-grade security analysis. Test AI-generated code in real projects with automatic backups, analyze code quality before deployment with **revolutionary multi-file context awareness**, scan for vulnerabilities with AI-powered insights, and seamlessly cluster related documents using semantic AI.

**Current Version:** `v1.4.0` — Now with **Multi-File Code Analysis & Enhanced Architecture**

---

## Table of Contents
- [What It Does](#-what-it-does)
- [🆕 New in v1.4.0](#-new-in-v140-multi-file-analysis)
- [Quickstart](#-quickstart)
- [AI Setup](#-ai-features-setup)
- [Multi-File Analysis](#-multi-file-analysis-features)
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

### 🤖 **AI Code Review** 🔐 **NEW: Multi-File Analysis**
- **Three Analysis Modes**: Single file, Module analysis, and Project-level architectural review
- **Smart Dependency Detection**: Identifies missing imports available in other files
- **False Positive Reduction**: Understands project structure to avoid incorrect flagging
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

## 🆕 New in v1.4.0: Multi-File Analysis 

### 🎯 **Problem Solved**
**Before**: *"Missing import error for `helper_function` - but it's defined in `utils.py`!"*
**After**: *"✅ `helper_function` available in utils.py - suggested import: `from utils import helper_function`"*

### 🚀 **Three Analysis Modes**

#### **1. Single File Analysis** (Original)
- Traditional per-file analysis
- Fast and focused
- Perfect for quick reviews

#### **2. Module Analysis** (NEW)
- **Cross-file context awareness**
- **Dependency resolution across files**
- **Missing import detection with suggestions**
- **Interface consistency checking**
- **Module cohesion analysis**

#### **3. Project Analysis** (NEW)
- **Full architectural review**
- **Dependency graph analysis**
- **Framework compliance checking**
- **Scalability assessment**
- **Project-wide pattern detection**

### 🧠 **Smart Context Building**
- **Framework Detection**: FastAPI, Flask, Django, React, Vue, Express, Next.js
- **Dependency Mapping**: Complete import/export analysis with AST parsing
- **Global Symbol Resolution**: Tracks functions/classes across entire codebase
- **Cross-Reference Validation**: Identifies missing imports available in other files
- **Architecture Analysis**: Circular dependency detection and coupling assessment

### 📊 **Enhanced Reporting**
```markdown
# Multi-File Analysis Report
**Framework:** FastAPI
**Files Analyzed:** 12
**Cross-file Dependencies:** 23
**Missing Imports Found:** 3

## Cross-File Issues Found:
- ❌ main.py: 'helper_function' available in utils.py but not imported
- ⚠️ config.py: Circular dependency detected with database.py
- ✅ Strong module cohesion detected in auth/ directory

## Integration Summary:
Files work well together with minor import issues easily resolved.
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

### 📊 **Project Architecture Analysis**
- **Dependency Graph**: Visual representation of file relationships
- **Framework Detection**: Auto-identify tech stack and best practices
- **Scalability Assessment**: Identify potential architectural bottlenecks
- **Code Quality Metrics**: Consistency analysis across entire project
- **Security Integration**: Cross-reference with security analysis findings

### 🔧 **Analysis Workflow**
1. **Select Analysis Mode**: Single/Module/Project
2. **Smart File Selection**: Context-aware file picker
3. **Framework Detection**: Automatic tech stack identification
4. **Dependency Mapping**: Complete import/export analysis
5. **Context Building**: Cross-file relationship mapping
6. **AI Analysis**: Enhanced prompts with full context
7. **Professional Reporting**: Comprehensive insights and recommendations

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
- **Risk anxiety** when deploying untested code changes

**Wolfkit = Confidence in your development workflow.**

### 🎯 The Enhanced Five-Phase Approach:
1. **🤖 Analyze** → Multi-file code review with cross-file context awareness
2. **📄 Organize** → Cluster and merge related documents intelligently  
3. **🛡️ Secure** → Scan for vulnerabilities with professional insights
4. **🚀 Test** → Stage secure, reviewed code with automatic backups
5. **✅ Trust** → Deploy with confidence or revert instantly

---

## 🛠 Complete Feature Set

### 🤖 Code Review Tab 🔐 **ENHANCED**
- **Three Analysis Modes**: Single file, Module, and Project analysis
- **Smart Context Building**: Framework detection and dependency mapping
- **Cross-file Validation**: Missing import detection and resolution
- **Professional Reports**: Enhanced markdown reports with project insights
- **Configuration Checking**: Multi-file capability verification
- **Progress Tracking**: Real-time analysis feedback

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
- Updated with Multi-File Analysis documentation

---

## 🧪 Enhanced Workflow: Analyze → Organize → Secure → Test → Trust

> **Use only what you need. Skip what you don't.**

### **For Code Development:**
1. **🤖 Code Review**: 
   - **Single File**: Quick individual file analysis
   - **Module**: Cross-file analysis with context awareness
   - **Project**: Full architectural review and dependency analysis
2. **📄 Document Merge**: Organize related project documentation  
3. **🛡️ Security Analysis**: Scan for vulnerabilities and get professional insights
4. **🚀 File Testing**: Stage secure, reviewed code with automatic backups
5. **✅ Trust**: Accept changes confidently or revert instantly

### **For Multi-File Analysis:**
1. **📂 Select Analysis Mode** → Choose Single/Module/Project analysis
2. **📁 Smart Selection** → Context-aware file or project selection
3. **🔍 Framework Detection** → Automatic tech stack identification
4. **🧠 Context Building** → Cross-file dependency mapping
5. **🤖 AI Analysis** → Enhanced analysis with full project context
6. **📊 Professional Reporting** → Comprehensive insights and recommendations

### **For Project Architecture Review:**
1. **🏗️ Select Project Directory** → Choose entire project for analysis
2. **⚙️ Configure Analysis** → Set options and framework preferences
3. **🔍 Run Analysis** → Multi-file architectural review
4. **📊 Review Results** → Dependency graphs and scalability assessment
5. **📄 Export Report** → Professional documentation for team review

---

## 📏 Architecture Overview

```
wolfkit/
├── main.py                      # Application entry point
├── controller.py                # Core business logic & workflow coordination
├── code_reviewer.py            # 🔐 Enhanced multi-file AI analysis orchestrator
├── dependency_mapper.py        # 🆕 Import/export analysis and dependency graphs
├── code_context_analyzer.py    # 🆕 Project structure analysis and context building
├── multi_file_analyzer.py      # 🆕 Multi-file analysis coordination
├── document_merger.py          # 🔐 Document clustering and merging
├── security_analyzer.py        # 🔐 Local security vulnerability scanning
├── security_patterns.py        # Security pattern detection engine
├── security_reporter.py        # 🔐 Professional AI-powered report generation
├── ui/
│   ├── app_frame.py            # Main orchestrator with tab management
│   ├── base_tab.py             # Common tab functionality and utilities
│   ├── code_review_tab.py      # 🔐 Enhanced multi-file analysis interface
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
├── test_multi_file_analysis.py # 🆕 Comprehensive test suite
└── requirements.txt
```


---

## 📄 Sample Reports

### **Enhanced Multi-File Analysis Report**
```markdown
# Wolfkit AI Code Review (Module Analysis)
**Generated:** 2025-07-17 14:30:22
**Analysis Type:** Module
**Framework:** FastAPI
**Files Analyzed:** 4

## Analysis Summary
- **Target Files:** 4
- **External Dependencies:** 8
- **Missing Imports Found:** 2
- **Cross-file Dependencies:** 6

## Target Files
- `main.py`
- `utils.py`
- `config.py`
- `models.py`

---

### Module Analysis Results

**Overall Assessment:** Module shows good structure with minor import issues easily resolved.

**Cross-File Issues Found:**
- ❌ main.py: 'helper_function' available in utils.py but not imported
  - Suggested fix: `from utils import helper_function`
- ❌ models.py: 'DATABASE_URL' used but not imported from config.py
  - Suggested fix: `from config import DATABASE_URL`
- ✅ Strong FastAPI patterns detected with proper route organization

**Integration Summary:**
Files work well together as a cohesive module. The FastAPI application structure follows best practices with clear separation of concerns between routing, utilities, and configuration.

**Recommendations:**
1. Add missing imports identified above
2. Consider creating an `__init__.py` file for proper package structure
3. The database connection logic could be centralized in models.py

---

*This module analysis was generated by Wolfkit's enhanced code review system with cross-file context awareness.*
```

### **Security Analysis Report**
```markdown
# 🛡️ Wolfkit Security Analysis Report
**Generated:** 2025-07-17 14:30:22
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
- ✅ **Dependency analysis** - AST parsing happens locally

### **What Uses AI (OpenAI API):**
- 🔐 **Code analysis prompts** - structured questions with project context
- 🔐 **Document clustering** - content summaries for semantic grouping
- 🔐 **Security report generation** - findings summaries for professional insights
- 🔐 **Report formatting** - structured data for executive summaries

### **Privacy Guarantees:**
- **No Raw Code Transmitted**: Only structured prompts and project context
- **Enhanced Context Privacy**: Cross-file relationships analyzed locally
- **OpenAI Data Policy**: No data retention per OpenAI API terms of service
- **Automatic Backups**: Every file replacement backed up until you accept changes
- **Reversible Operations**: All merges and staging operations can be undone
- **Local Reports**: All analysis saved to your `/reports/` directory

---

## 🚀 Version History & Roadmap

### ✅ v1.4.0 – Multi-File Analysis
- **Revolutionary Enhancement**: Cross-file context awareness for code review
- **Three Analysis Modes**: Single file, Module, and Project-level analysis
- **Smart Dependency Detection**: Missing import identification with suggestions
- **Framework Intelligence**: Auto-detection of FastAPI, Flask, Django, React, etc.
- **Professional Architecture**: 4 focused modules under 400 lines each
- **Enhanced Reporting**: Context-aware insights and recommendations
- **Performance Optimized**: AST parsing with intelligent caching
- **Backward Compatible**: All existing functionality preserved

### ✅ v1.3.2 – Security Analysis Revolution
- **Comprehensive Security Analysis**: OWASP Top 10 vulnerability detection
- **Hybrid Architecture**: Local scanning + AI-powered professional reporting
- **Framework Intelligence**: FastAPI, Flask, Django specific security checks
- **Professional Reporting**: Executive summaries with technical details
- **Enhanced Documentation**: Complete Security Analysis user guide

### ✅ v1.3.1 – Enhanced Features & Architecture
- **85% Code Reduction**: Main orchestrator from 1,306 → 200 lines
- **Priority-Based Tab Ordering**: Logical workflow optimization
- **Clear Interface Naming**: Improved user experience
- **Working Navigation**: Fixed documentation with visual feedback

### ✅ v1.3.0 – Document Clustering & Merge
- **Document Merge Tab**: AI-powered semantic document organization
- **Universal Document Support**: PDF, Word, Text, Markdown, Code files
- **Smart Clustering**: AI embeddings for content similarity
- **Visual Interface**: Interactive cluster cards with previews

### ✅ v1.2.0 – AI Code Review Foundation
- **AI Code Review Tab**: Pre-flight analysis of LLM-generated code
- **Multi-File Analysis**: Review entire batches with progress tracking
- **Professional Reports**: Markdown analysis reports
- **Budget-Friendly**: gpt-4o-mini integration


---

## 💰 Cost Transparency

### 🔑 API Requirements Summary
| Feature | API Required | Typical Cost | Notes |
|---------|-------------|--------------|-------|
| 🤖 Code Review (Single) | ✅ OpenAI | ~$0.002-0.005/file | Traditional analysis |
| 🤖 Code Review (Module) | ✅ OpenAI | ~$0.01-0.02/module | 🆕 Cross-file analysis |
| 🤖 Code Review (Project) | ✅ OpenAI | ~$0.05-0.15/project | 🆕 Architectural review |
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
- **No per-user licensing** - single purchase, unlimited local use  
- **No data storage charges** - everything stored locally
- **Transparent billing** - direct OpenAI API usage tracking
- **Enhanced value** - Multi-file analysis provides significantly more insight per dollar

---

## 🌍 Real-World Use Cases

### **For Developers:**
- **Multi-Module Projects**: Analyze entire Flask/FastAPI applications with cross-file context
- **AI Code Integration**: Review ChatGPT/Claude-generated code across multiple files
- **Refactoring Projects**: Understand dependencies before major code restructuring
- **Framework Migration**: Assess compatibility when moving between frameworks
- **Code Quality Assurance**: Catch cross-file issues that single-file analysis misses

### **For Development Teams:**
- **Code Review Process**: Enhanced PR reviews with architectural insights
- **Onboarding**: Help new developers understand project structure and dependencies
- **Technical Debt Assessment**: Identify architectural issues and improvement opportunities
- **Framework Compliance**: Ensure adherence to team coding standards
- **Knowledge Transfer**: Generate comprehensive project documentation

### **For Security Teams:**
- **Holistic Security Assessment**: Understand security implications across entire projects
- **Compliance Documentation**: Professional reports for regulatory requirements
- **Risk Management**: Quantified security scoring for management reporting
- **Framework-Specific Audits**: Tailored analysis for your technology stack

### **For Content Creators:**
- **Documentation Organization**: Merge scattered technical documentation
- **Content Consolidation**: Organize research notes and article drafts
- **Asset Management**: Clean up duplicate files and organize by topic

---

## 🤝 Contributing

Found a bug? Have a feature request? Want to contribute to the multi-file analysis engine?

### **How to Help:**
1. **Report Issues**: Check existing issues on GitHub, create detailed bug reports
2. **Feature Requests**: Suggest enhancements for multi-file analysis capabilities
3. **Code Contributions**: PRs welcome for analysis improvements and new features
4. **Documentation**: Help improve user guides and troubleshooting
5. **Testing**: Help test the multi-file analysis with different project structures

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

# Run comprehensive tests
python test_multi_file_analysis.py

# Run the application
python main.py
```

### **Code Standards:**
- **Type Hints Required**: All new code must include comprehensive type annotations
- **400-Line Limit**: Try to keep all modules under 400 lines for maintainability
- **Single Responsibility**: Each module/class should have one clear purpose
- **Local Imports**: Heavy dependencies should use local imports for startup performance
- **Error Handling**: Graceful fallbacks with user-friendly error messages
- **Privacy-First**: Minimize data transmission, maximize local processing
- **Multi-File Aware**: Consider cross-file implications in new features

---

## 📄 License

MIT License - Use freely in your own projects! See LICENSE file for details.

---

## 💬 Built By

A developer who got tired of:
- ✋ **Breaking working code** with AI-generated "improvements"
- 🤯 **Missing cross-file dependencies** that cause runtime errors
- 🔓 **Deploying vulnerabilities** hidden in complex codebases  
- 📄 **Managing chaos** across 15+ versions of the same document
- 🐛 **Debugging issues** that span multiple files and could be caught earlier
- 🗂️ **Document sprawl** with duplicates and scattered content

If you build with LLMs, work with multi-file projects, care about security, and want to **analyze intelligently**, **organize efficiently**, and **deploy confidently**...

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

*"The best code review is the one that understands your entire project. The best security analysis is the one that happens before you deploy. The best document organization is the one that happens automatically."*

**Star ⭐ this repo if Wolfkit's multi-file analysis revolutionizes your development workflow!**