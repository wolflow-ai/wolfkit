# 🐺 Wolfkit

**Try, Test, Trust.**

Wolfkit is a lightweight GUI tool for developers who want a fast, safe way to test AI-generated code in real projects. Now with **AI-powered code review** to catch issues before you even deploy!

**Current Version:** `v1.2.0`

---

## ⚡ What It Does

### 🔍 **NEW: AI Code Review**
- ✅ **Pre-flight check**: Analyze LLM-generated code for common issues
- ✅ **Multi-file analysis**: Review entire batches at once
- ✅ **Smart detection**: Finds syntax errors, missing imports, logic gaps
- ✅ **Markdown reports**: Professional analysis reports you can save and share
- ✅ **Budget-friendly**: Uses gpt-4o-mini (~$0.002-0.005 per file)

### 🚀 **Core Workflow**
- ✅ Drop in one or more test files (even with different names)
- ✅ Choose which project files to replace — or add new files anywhere in the project
- ✅ Launch your project (Python app or Static Web page)
- ✅ Accept or revert changes with one click — individually or in batches
- ✅ Auto-detect and launch the project's own virtual environment (if available)

---

## 📸 Demo Video (Press Play)

https://github.com/user-attachments/assets/245d7690-bbb1-48d8-9730-c6541a200cc7

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

# 4. Set up AI Code Review (optional)
cp .env.example .env
# Edit .env and add your OpenAI API key

# 5. Run the app
python main.py
```

### ▶️ Windows Users: `launch-wolfkit.bat`

```bat
@echo off
cd /d %~dp0
call venv\Scripts\activate.bat
start "" pythonw main.py > log.txt 2>&1
```

* Create a shortcut to `launch-wolfkit.bat` on your desktop
* This runs Wolfkit in the background (no console window)
* Output is logged to `log.txt` in the same folder

---

## 🤖 AI Code Review Setup

### 1. Get an OpenAI API Key
- Visit [OpenAI Platform](https://platform.openai.com/api-keys)
- Create a new API key
- Copy it for the next step

### 2. Configure Wolfkit
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your API key:
OPENAI_API_KEY=sk-your-actual-api-key-here

# Optional: Choose a different model (default is gpt-4o-mini)
OPENAI_MODEL=gpt-4o-mini
```

### 3. Model Recommendations
| Model | Cost per File* | Best For |
|-------|---------------|----------|
| `gpt-4o-mini` | ~$0.002-0.005 | **Recommended**: Great quality, budget-friendly |
| `gpt-4.1-nano` | ~$0.001-0.003 | Ultra-budget option |
| `gpt-4o` | ~$0.03-0.07 | Premium quality (15x more expensive) |

*Based on typical 500-1000 line code files

---

## 🧐 Why Use Wolfkit?

### The Problem
When working with LLMs to generate code, you often get files that **look right** but have subtle issues:
- Missing imports
- Undefined functions
- Syntax errors
- Logic gaps

Finding these issues manually in 800+ lines of code is painful and time-consuming.

### The Solution
**Wolfkit's Two-Phase Approach:**

1. **🔍 AI Review Phase**: Analyze code for issues before deployment
2. **🚀 Test Phase**: Deploy and test files that pass review

This saves you from deploying broken code and speeds up your development cycle.

---

## 🛠 Complete Feature Set

### 🤖 **AI Code Review Tab**
* Select files for AI analysis (independent of staging)
* One-click batch analysis with progress tracking
* Professional markdown reports saved locally
* Configuration checking and status updates
* Cross-platform report opening

### 🚀 **Main Workflow Tab**
* Set a target project directory
* Select one or more test files
* Choose where to replace or add files
* Auto-backup any replaced file
* Launch your app (Python project or static web page)
* Accept or revert the entire test batch
* Console output for clear feedback

---

## 🧪 Updated Workflow: Analyze → Try → Test → Trust

1. **🔍 Analyze**: Review code with AI before deployment
2. **📂 Set Project Directory**
3. **📁 Select File(s) to Test** (only files that passed review!)
4. **🎯 Choose Target File(s)** to Replace or Add
5. **⚙️ Pick Launch Type** (Python App or Static Web Page)
6. **▶️ Run Test** → App or site launches
7. **✅ Accept** (keep new versions) or **🔄 Revert** (restore originals)

---

## 📂 File Structure

```
wolfkit/
├── main.py                    # Application entry point
├── controller.py              # Core business logic + AI integration
├── code_reviewer.py           # AI-powered code analysis
├── ui/
│   ├── __init__.py
│   └── app_frame.py          # Main GUI with tabs
├── assets/
│   └── wolfkit-icon.png     # App icon
├── backups/                  # Auto-generated file backups
├── reports/                  # AI analysis reports
├── requirements.txt          # Dependencies
├── .env.example             # Configuration template
└── README.md               # This file
```

---

## 📄 Sample AI Analysis Report

```markdown
# Wolfkit AI Code Review
**Generated:** 2025-07-11 14:30:15
**Files Analyzed:** 2
**Model Used:** gpt-4o-mini

---

### Analysis of `controller.py`

**File Type:** Python
**Syntax Check:** ✅ Valid

**Issues Found:**
- ❌ **Missing Import**: `from typing import List` needed for type hints on line 45
- ⚠️ **Potential Issue**: Function `process_data()` called but not defined
- ✅ **Good Practice**: Proper error handling with try/catch blocks

**Summary:**
Code structure is solid but needs import fix and missing function definition.
```

---

## 🛡️ Backups & Safety

- Backups stored in `/backups/<project-name>/<filename>.bak`
- Each replacement file is backed up until you accept the test version
- Reverts are safe and repeatable
- AI analysis reports saved in `/reports/` with timestamps

---

## 🛡️ Roadmap Highlights

### ✅ Completed
* [x] Multi-file batch support
* [x] Static Web Page launch support  
* [x] Folder choice when adding new files
* [x] Auto-detect Python virtual environments
* [x] **AI-powered code review with OpenAI integration**
* [x] **Professional markdown analysis reports**
* [x] **Budget-friendly model recommendations**

### 🔮 Coming Soon
* [ ] Support for additional AI providers (Anthropic Claude, local models)
* [ ] Custom analysis prompts and rulesets
* [ ] Inline code annotation and highlighting
* [ ] Project-wide analysis in one click
* [ ] Custom command launch (e.g., npm start)
* [ ] File type filters when selecting files
* [ ] Background process handling

---

## 💰 Cost Transparency

Using the recommended `gpt-4o-mini` model:
- **Typical cost per file**: $0.002-0.005
- **100 file analyses**: ~$0.20-0.50
- **Monthly budget for active developer**: <$5

No subscription required - pay only for what you analyze!

---

## 🧙‍♂️ Part of the Wolflow Ecosystem

- [✨ Wolfscribe](https://github.com/CLewisMessina/wolfscribe) – Turn documents into datasets for LLM training, locally
- [🐺 Wolftrain](https://github.com/CLewisMessina/wolftrain) – Local LoRA fine-tuning app
- [🔍 WolfMerge](https://github.com/CLewisMessina/wolfmerge) – AI-powered German compliance platform for SMEs *(in active development)*

---

## 🤝 Contributing

Found a bug? Have a feature request? 

1. Check existing issues
2. Create a new issue with details
3. PRs welcome for bug fixes and improvements

---

## 📄 License

MIT License - feel free to use in your own projects!

---

## 💬 Built By

A developer who wanted to feel safe experimenting with AI-generated code—and finally found the right flow.

If you build with LLMs, test often, and want to catch issues before deployment...

**Wolfkit is for you.**

---

*"The best code review is the one that happens before you deploy."* 🐺