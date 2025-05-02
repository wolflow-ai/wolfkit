# 🐺 Wolfkit

[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-BY--NC%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)

**Try, Test, Trust.**

Wolfkit is a lightweight GUI tool for developers who want a fast, safe way to test AI-generated code in real projects. It’s built for developers who value speed, simplicity, and rollback control—without using Git or the terminal.

**Current Version:** `v1.1`

---

## ⚡ What It Does
- ✅ Drop in one or more test files (even with different names)
- ✅ Choose which project files to replace — or add new files anywhere in the project
- ✅ Launch your project (Python app or Static Web page)
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

## 🧐 Why Use Wolfkit?
If you're working with LLMs or iterating on new code quickly, Wolfkit:
- Keeps your original files safe
- Handles renamed test files with ease
- Lets you add new files to any project subfolder
- Launches your app for visual QA (Python GUI or Static Web)
- Lets you cleanly accept or roll back changes

Perfect for testing things like:
- `main.py → main-test-3.py`
- `controller.py → controller_v2.py`
- Adding a new `todo_form.py` into `/components/forms/`
- Dropping in a new `about.html` into `/pages/`

---

## 🛠 Features
- Set a target project directory
- Select one or more test files
- Choose where to replace or add files
- Auto-backup any replaced file
- Launch your app:
  - Python project (`python main.py`)
  - Static web page (`index.html`)
- Accept or revert the entire test batch
- Console output for clear feedback

---

## 🖥️ Screenshot

![Wolfkit Interface Top](https://github.com/CLewisMessina/wolfkit/blob/main/assets/screenshots/wolfkit-screenshot.png)


---

## 🧪 Try → Test → Trust Workflow

1. **Set Project Directory**
2. **Select File(s) to Test**
3. **Choose Target File(s) to Replace or Add**
4. **Pick Launch Type** (Python App or Static Web Page)
5. **Run Test** → App or site launches
6. **Accept** (keep new versions) or **Revert** (restore originals)

---

## 📂 Backups
Backups are stored in:
```
/backups/<project-name>/<filename>.bak
```
Each replacement file is backed up so you can safely revert.

---

## 🛡️ Roadmap Highlights
- [x] Multi-file batch support
- [x] Static Web Page launch support
- [x] Folder choice when adding new files
- [ ] Custom command launch (e.g., npm start)
- [ ] File type filters when selecting files
- [ ] Visual highlight of staged files
- [ ] Snapshot + diff integration
- [ ] Background process handling
- [ ] Dockerized and compiled app support

---

## 💬 Built By
A developer who wanted to feel safe experimenting—and finally found the right flow.

If you build with LLMs, test often, and don’t want to fight with tooling...

**Wolfkit is for you.**

---

### 🎉 Notes
- **v1.0:** Core file staging, testing, and rollback for Python apps.
- **v1.1:** Added Static Web support + new file folder placement.

---

[See full changelog ➔](CHANGELOG.md)
