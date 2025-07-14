# 🐺 Wolfkit

**Try, Test, Trust.**

Wolfkit is a comprehensive AI-powered development tool that combines safe code testing with intelligent document organization. Test AI-generated code in real projects with automatic backups, analyze code quality before deployment, and seamlessly cluster related documents using semantic AI.

**Current Version:** `v1.3.1` - Now with **Refactored Architecture & Enhanced UX**

---

## ⚡ What It Does

### 🔍 **AI Code Review** (Priority #1)
- ✅ **Pre-flight check**: Analyze LLM-generated code for common issues
- ✅ **Multi-file analysis**: Review entire batches at once
- ✅ **Smart detection**: Finds syntax errors, missing imports, logic gaps
- ✅ **Markdown reports**: Professional analysis reports you can save and share
- ✅ **Budget-friendly**: Uses gpt-4o-mini (~$0.002-0.005 per file)

### 📄 **Document Clustering & Merge** (Priority #2)
- ✅ **Semantic clustering**: Group related documents using AI embeddings
- ✅ **Universal support**: PDF, Word, Text, Markdown, Code files
- ✅ **Smart merging**: AI-powered content consolidation with duplicate removal
- ✅ **In-app interface**: Visual cluster cards with instant merge actions
- ✅ **Intelligent naming**: Auto-suggests meaningful merge filenames
- ✅ **Cost effective**: ~$0.01-0.05 per document batch

### 🚀 **File Testing Workflow** (Priority #3)
- ✅ Drop in one or more test files (even with different names)
- ✅ Choose which project files to replace — or add new files anywhere in the project
- ✅ Launch your project (Python app or Static Web page)
- ✅ Accept or revert changes with one click — individually or in batches
- ✅ Auto-detect and launch the project's own virtual environment (if available)

### 📚 **Built-in Documentation** (Priority #4)
- ✅ **Complete user manual**: No external docs needed
- ✅ **Quick navigation**: Jump to any section instantly
- ✅ **Step-by-step workflows**: Clear instructions for every feature
- ✅ **Troubleshooting guide**: Common issues and solutions

---

## 🎯 New in v1.3.1: Enhanced User Experience

### **Improved Tab Organization**
- **Priority-based ordering**: Most valuable AI features get top billing
- **Clear naming**: "File Testing" instead of confusing "Main Workflow"
- **Logical flow**: Code Review → Document Merge → File Testing → Documentation

### **Refactored Architecture** 
- **85% code reduction**: Main orchestrator reduced from 1,306 → 200 lines
- **Clean separation**: Each component has single responsibility
- **Type safety**: Comprehensive type hints throughout
- **Maintainable**: Easy to add features without breaking existing code

### **Enhanced Navigation**
- **Working quick links**: Documentation navigation now functions perfectly
- **Visual feedback**: Highlights show exactly where you jump to
- **Consistent naming**: Interface terminology matches throughout app

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

# 4. Set up AI features (required for Code Review and Document Merge)
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

## 🤖 AI Features Setup

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

### 4. Document Merge Costs
| Operation | Cost Range | Description |
|-----------|------------|-------------|
| **Document Clustering** | $0.01-0.05 per batch | Semantic analysis of document folder |
| **Document Merging** | $0.02-0.10 per merge | AI-powered content consolidation |
| **Typical Usage** | <$5/month | Active developer with regular analysis |

---

## 🧐 Why Use Wolfkit?

### The Modern Developer Challenge
When working with LLMs and managing multiple document versions, you face:
- **Code Issues**: Files that look right but have subtle bugs
- **Document Chaos**: Multiple versions, duplicates, scattered content
- **Risk Management**: Fear of breaking working code with new changes
- **Time Waste**: Manual debugging and document organization

### The Wolfkit Solution
**Three-Phase Approach:**

1. **🔍 AI Review Phase**: Analyze code and cluster documents before action
2. **🚀 Test Phase**: Deploy files that pass review with automatic backups
3. ✅ **Trust Phase**: Accept changes confidently or revert instantly

This **eliminates broken deployments** and **organizes document chaos** while speeding up your development cycle.

---

## 🛠 Complete Feature Set

### 🤖 **Code Review Tab** (Priority #1)
* Select files for AI analysis (independent of staging)
* One-click batch analysis with progress tracking
* Professional markdown reports saved locally
* Configuration checking and status updates
* Cross-platform report opening

### 📄 **Document Merge Tab** (Priority #2)
* Select folder for document analysis
* Configure clustering (manual count or auto-detection)
* Visual cluster cards with similarity scores
* In-app merge previews and document lists
* Editable merge filenames with smart suggestions
* One-click merging with output directory selection
* Skip/preview options for each cluster

### 🚀 **File Testing Tab** (Priority #3)
* Set a target project directory
* Select one or more test files
* Choose where to replace or add files
* Auto-backup any replaced file
* Launch your app (Python project or static web page)
* Accept or revert the entire test batch
* Console output for clear feedback

### 📖 **Documentation Tab** (Priority #4)
* Complete user manual built into the app
* Quick navigation to specific features
* Step-by-step workflows and examples
* Troubleshooting guide and best practices
* Working navigation links with visual feedback

---

## 🧪 Enhanced Workflow: Analyze → Cluster → Test → Trust

### **For Code Development:**
1. **🔍 Code Review**: Analyze LLM-generated code for issues before deployment
2. **📂 Set Project Directory**
3. **📁 Select File(s) to Test** (only files that passed review!)
4. **🎯 Choose Target File(s)** to Replace or Add
5. **⚙️ Pick Launch Type** (Python App or Static Web Page)
6. **▶️ Run Test** → App or site launches
7. **✅ Accept** (keep new versions) or **🔄 Revert** (restore originals)

### **For Document Organization:**
1. **📁 Select Document Folder** with mixed/duplicate files
2. **🔍 Analyze Documents** → AI finds semantic clusters
3. **👀 Review Clusters** → See similarity scores and previews
4. **✏️ Edit Merge Names** → Customize output filenames
5. **🔄 Merge Selected** → Choose clusters to consolidate
6. **📄 Enjoy Clean Results** → Organized, merged documents

---

## 🏗️ Architecture Overview

### **Clean, Maintainable Structure**
```
wolfkit/
├── main.py                    # Application entry point
├── controller.py              # Core business logic + AI integration
├── code_reviewer.py           # AI-powered code analysis
├── document_merger.py         # Document clustering and merging
├── ui/
│   ├── __init__.py           # Clean package exports
│   ├── app_frame.py          # Main orchestrator (200 lines)
│   ├── base_tab.py           # Common tab functionality
│   ├── code_review_tab.py    # AI analysis interface
│   ├── document_merge_tab.py # Document clustering interface
│   ├── main_workflow_tab.py  # File staging interface
│   ├── documentation_tab.py  # Built-in help system
│   └── widgets/
│       ├── cluster_card.py   # Custom cluster visualization
│       ├── console_output.py # Reusable console widget
│       └── progress_tracker.py # Progress indication
├── assets/
│   └── wolfkit-icon.png     # App icon
├── backups/                  # Auto-generated file backups
├── reports/                  # AI analysis reports
├── requirements.txt          # Dependencies
├── .env.example             # Configuration template
└── README.md               # This file
```

### **Refactoring Achievement**
- **Main file reduction**: 1,306 lines → 200 lines (**85% reduction**)
- **Single responsibility**: Each file has one clear purpose
- **Type safety**: Comprehensive type hints throughout
- **Local imports**: Heavy dependencies loaded only when needed
- **Easy testing**: Individual components can be unit tested

---

## 📄 Sample AI Analysis Report

```markdown
# Wolfkit AI Code Review
**Generated:** 2025-07-14 15:45:12
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

## 📄 Sample Document Cluster Analysis

```markdown
# Wolfkit Document Clustering Analysis
**Generated:** 2025-07-14 10:53:43
**Clusters Found:** 3
**Total Documents:** 24

---

## Cluster 1 (Similarity: 79.19%)

**Suggested Merge Name:** `merged_resume_documents.md`

**Documents in Cluster:**
- Resume_v1.docx
- Resume_final.pdf
- Resume_latest.md
- [9 more documents...]

**Merge Preview:**
Consolidated resume combining all versions with duplicate content removed
and professional formatting applied...
```

---

## 🛡️ Safety & Data Privacy

- **Local Processing**: All document content processed locally, only metadata sent to OpenAI
- **Automatic Backups**: Every file replacement backed up until you accept changes
- **Reversible Operations**: All merges and staging operations can be undone
- **No Data Retention**: OpenAI doesn't retain your content (per their API policy)
- **Offline Capable**: File testing functions without internet (AI features require connection)

---

## 🎯 Version History & Roadmap

### ✅ Completed in v1.3.1
* [x] **Complete UI refactoring**: 85% reduction in main file complexity
* [x] **Enhanced user experience**: Priority-based tab ordering
* [x] **Working navigation**: Fixed documentation quick links
* [x] **Type safety**: Comprehensive type hints throughout
* [x] **Modular architecture**: Single responsibility per component
* [x] **Performance improvements**: Lazy loading of heavy dependencies

### ✅ Previous Achievements (v1.3.0)
* [x] Multi-file batch support
* [x] Static Web Page launch support  
* [x] Folder choice when adding new files
* [x] Auto-detect Python virtual environments
* [x] AI-powered code review with OpenAI integration
* [x] Professional markdown analysis reports
* [x] Document clustering and semantic merging
* [x] In-app cluster visualization and management
* [x] Comprehensive built-in documentation

### 🔮 Coming Soon (v1.4.0+)
* [ ] Support for additional AI providers (Anthropic Claude, local models)
* [ ] Custom analysis prompts and rulesets
* [ ] Enhanced auto-clustering with silhouette analysis
* [ ] Drag-and-drop file interfaces
* [ ] Project templates and workflow presets
* [ ] Batch export/import of cluster configurations
* [ ] Integration with popular IDEs (VS Code extension)
* [ ] Team collaboration features

### 🌟 Advanced Features (v2.0+)
* [ ] Real-time document synchronization
* [ ] Advanced merge conflict resolution
* [ ] Custom merge templates by document type
* [ ] Machine learning model fine-tuning
* [ ] Enterprise SSO and team management
* [ ] API for integration with other tools

---

## 💰 Total Cost Transparency

### Monthly Budget Examples (using gpt-4o-mini):
- **Light User**: 20 code reviews + 5 document merges = ~$2-3/month
- **Active Developer**: 100 code reviews + 20 document merges = ~$8-12/month  
- **Heavy User**: 500 code reviews + 100 document merges = ~$30-50/month

### No Hidden Costs:
- ✅ **No subscription fees**
- ✅ **No per-user licensing**
- ✅ **No data storage charges**
- ✅ **Pay only for AI analysis usage**
- ✅ **Transparent OpenAI billing**

---

## 🧙‍♂️ Part of the Wolflow Ecosystem

- [✨ Wolfscribe](https://github.com/CLewisMessina/wolfscribe) – Turn documents into datasets for LLM training, locally
- [🐺 Wolftrain](https://github.com/CLewisMessina/wolftrain) – Local LoRA fine-tuning app
- [🔍 WolfMerge](https://github.com/CLewisMessina/wolfmerge) – AI-powered German compliance platform for SMEs *(in active development)*

---

## 🎯 Real-World Use Cases

### **For Developers:**
- Test ChatGPT/Claude-generated code safely
- Organize technical documentation
- Merge API documentation from multiple sources
- Consolidate meeting notes by project
- Clean up duplicate configuration files

### **For Content Creators:**
- Merge multiple article drafts
- Organize research notes by topic
- Consolidate interview transcripts
- Clean up duplicate assets and files

### **For Professionals:**
- Organize resume/CV versions (like the demo!)
- Merge contract drafts and legal documents
- Consolidate project proposals
- Organize training materials by subject

### **For Teams:**
- Standardize coding practices with AI review
- Organize shared documentation
- Merge knowledge base articles
- Consolidate onboarding materials

---

## 🤝 Contributing

Found a bug? Have a feature request? Want to contribute?

1. Check existing issues on GitHub
2. Create a new issue with detailed description
3. PRs welcome for bug fixes and improvements
4. Follow the existing code style and add tests

### Development Setup:
```bash
# Fork and clone the repo
git clone https://github.com/your-username/wolfkit.git
cd wolfkit

# Create development environment
python -m venv dev-env
source dev-env/bin/activate  # or dev-env\Scripts\activate on Windows

# Install with development dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

### Code Architecture:
- Each UI component is in its own file with single responsibility
- Type hints are required for all new code
- Local imports for heavy dependencies to improve startup time
- Comprehensive error handling with graceful fallbacks

---

## 📄 License

MIT License - feel free to use in your own projects! See LICENSE file for details.

---

## 💬 Built By

A developer who got tired of:
- ✋ Breaking working code with AI-generated "improvements"
- 📄 Managing 24 different versions of the same resume
- 🐛 Spending hours debugging issues that could be caught upfront
- 🗂️ Drowning in duplicate and scattered documents

If you build with LLMs, work with multiple document versions, and want to **try code safely** and **organize intelligently**...

**Wolfkit is for you.**

---

## 🌟 What Users Are Saying

> *"This is absolutely amazing. I cannot even begin to express how impressed I am with this."*
> — Early Beta User

> *"The document clustering found patterns I never would have noticed manually."*
> — Content Manager

> *"Finally, a tool that lets me test AI code without fear!"*
> — Full-Stack Developer

> *"The refactored interface is so much cleaner - everything makes sense now."*
> — UI/UX Designer

---

## 🚀 Get Started Today

```bash
git clone https://github.com/your-username/wolfkit.git
cd wolfkit
pip install -r requirements.txt
python main.py
```

**Try it. Test it. Trust it.** 🐺

---

*"The best code review is the one that happens before you deploy. The best document organization is the one that happens automatically."* 🐺

**Star ⭐ this repo if Wolfkit helps your workflow!**