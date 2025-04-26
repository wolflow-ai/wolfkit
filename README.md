# 🐺 Wolfkit

[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-BY--NC%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)

**Try, Test, Trust.**

Wolfkit is a lightweight GUI tool for developers who want a fast, safe way to test AI-generated code in real projects. It’s built for developers who value speed, simplicity, and rollback control—without using Git or the terminal.

---

## ⚡ What It Does
- ✅ Drop in one or more test files (even with different names)
- ✅ Choose which project files to replace
- ✅ Launch your project in a real app window
- ✅ Accept or revert changes with one click—individually or in batches

It’s the “test chamber” for your dev cycle.

---

## 🚀 Quickstart

```bash
# 1. Clone the repo
# 2. Create and activate a virtual environment
pip install ttkbootstrap

# 3. Run the app
python main.py
```

---

## 🧠 Why Use Wolfkit?
If you're working with LLMs or iterating on new code quickly, Wolfkit:
- Keeps your original files safe
- Handles renamed test files with ease
- Launches your app for visual QA
- Lets you cleanly accept or roll back changes

Perfect for testing things like:
- `main.py → main-test-3.py`
- `controller.py → controller_v2.py`
- `tab_model_card.py → temp_tab_fix.py`

---

## 🛠 Features
- Set a target project directory
- Select one or more Python test files
- Choose target file for each test file
- Auto-backup any replaced file
- Launch the app in a new terminal window
- Accept or revert the entire test batch

---

## 🧪 Try → Test → Trust Workflow

1. **Set Project Directory**
2. **Select File(s) to Test**
3. **Choose Target File(s) to Replace or Add**
4. **Run Test** → App window launches
5. **Accept** (keep new versions) or **Revert** (restore originals)

---

## 📂 Backups
Backups are stored in:
```
/backups/<project-name>/<filename>.bak
```
Each replacement file is backed up so you can safely revert.

---

## 🧱 Roadmap
- [x] Multi-file batch support
- [ ] Custom test commands
- [ ] Snapshot + diff integration
- [ ] Configurable project presets

---

## 💬 Built By
A developer who wanted to feel safe experimenting—and finally found the right flow.

If you build with LLMs, test often, and don’t want to fight with tooling...

**Wolfkit is for you.**

