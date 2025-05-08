# 🐺 Wolfkit

**Try, Test, Trust.**

Wolfkit is a lightweight GUI tool for developers who want a fast, safe way to test AI-generated code in real projects. It’s built for devs who value speed, simplicity, and rollback control—without needing Git or the terminal.

**Current Version:** `v1.1.1`

---

## ⚡ What It Does

- ✅ Drop in one or more test files (even with different names)
- ✅ Choose which project files to replace — or add new files anywhere in the project
- ✅ Launch your project (Python app or Static Web page)
- ✅ Accept or revert changes with one click — individually or in batches
- ✅ Auto-detect and launch the project’s own virtual environment (if available)

---
## 📸 Demo Video (Press Play)


https://github.com/user-attachments/assets/245d7690-bbb1-48d8-9730-c6541a200cc7


---

## 🚀 Quickstart

```bash
# 1. Clone the repo
# 2. Create and activate a virtual environment
pip install -r requirements.txt

# 3. Run the app
python main.py
````

Or use the included `.bat` file for Windows:

### ▶️ `launch-wolfkit.bat`

```bat
@echo off
cd /d %~dp0
call venv\Scripts\activate.bat
start "" pythonw main.py > log.txt 2>&1
```

* Create a shortcut to `launch-wolfkit.bat` on your desktop
* This runs Wolfkit in the background (no console window)
* Output is logged to `log.txt` in the same folder

If you prefer visible console output (for debugging), uncomment this version:

```bat
REM @echo off
REM cd /d %~dp0
REM call venv\Scripts\activate.bat
REM python main.py
REM pause
```

---

## 🧐 Why Use Wolfkit?

If you're working with LLMs or iterating on new code quickly, Wolfkit:

* Keeps your original files safe
* Handles renamed test files with ease
* Lets you add new files to any subfolder in a project
* Launches your app for visual QA (Python GUI or static site)
* Lets you cleanly accept or roll back changes

Great for testing things like:

* `main.py → main-test-3.py`
* `controller.py → controller_v2.py`
* Adding a new `todo_form.py` into `/components/forms/`
* Dropping in a new `about.html` into `/pages/`

---

## 🛠 Features

* Set a target project directory
* Select one or more test files
* Choose where to replace or add files
* Auto-backup any replaced file
* Launch your app:

  * Python project (`main.py`)
  * Static web page (`index.html`)
* Accept or revert the entire test batch
* Console output for clear feedback

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

Each replacement file is backed up until you choose to accept the test version. Reverts are safe and repeatable.

---

## 🛡️ Roadmap Highlights

* [x] Multi-file batch support
* [x] Static Web Page launch support
* [x] Folder choice when adding new files
* [x] Auto-detect Python virtual environments
* [ ] Custom command launch (e.g., npm start)
* [ ] File type filters when selecting files
* [ ] Visual highlight of staged files
* [ ] Snapshot + diff integration
* [ ] Background process handling
* [ ] Dockerized and compiled app support

---

## 🧙‍♂️ Part of the Wolflow Ecosystem

- [✨ Wolfscribe](https://github.com/CLewisMessina/wolfscribe) – Turn documents into datasets for LLM training, locally
- [🐺 Wolftrain](https://github.com/CLewisMessina/wolftrain) – Local LoRA fine-tuning app
- [📈 Wolftrack](https://github.com/CLewisMessina) – Token usage + metrics tracker *(coming soon)*

---


## 💬 Built By

A developer who wanted to feel safe experimenting—and finally found the right flow.

If you build with LLMs, test often, and don’t want to fight with tooling...

**Wolfkit is for you.**


