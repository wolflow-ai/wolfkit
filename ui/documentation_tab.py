# ui/documentation_tab.py
"""
DocumentationTab - Built-in documentation and help
Updated to include Security Analysis documentation and proper tab ordering
"""
import tkinter as tk
from ttkbootstrap import Frame, Label, Button, Text, Scrollbar
from ttkbootstrap.constants import *
from ui.base_tab import BaseTab


class DocumentationTab(BaseTab):
    """Documentation tab with comprehensive instructions and navigation"""
    
    def __init__(self, parent, **kwargs):
        """Initialize DocumentationTab"""
        super().__init__(parent, **kwargs)
    
    def setup_tab(self):
        """Setup the documentation tab UI"""
        # Create scrollable text area for documentation
        docs_frame = Frame(self)
        docs_frame.pack(fill=BOTH, expand=YES, padx=10, pady=10)

        # Quick navigation section
        nav_frame = Frame(docs_frame)
        nav_frame.pack(fill=X, pady=(0, 10))

        nav_title = Label(nav_frame, text="📖 Wolfkit Documentation", font=("TkDefaultFont", 14, "bold"))
        nav_title.pack(anchor="w")

        nav_subtitle = Label(nav_frame, text="Complete guide to using Wolfkit's Try, Test, Trust workflow", font=("TkDefaultFont", 10))
        nav_subtitle.pack(anchor="w", pady=(0, 10))

        # Quick links - Updated to include Security Analysis
        links_frame = Frame(nav_frame)
        links_frame.pack(fill=X, pady=(0, 10))

        Label(links_frame, text="Quick Links:", font=("TkDefaultFont", 10, "bold")).pack(side=LEFT)

        self.jump_review_btn = Button(links_frame, text="Code Review", bootstyle="link", command=lambda: self._jump_to_section("review"))
        self.jump_review_btn.pack(side=LEFT, padx=(10, 5))

        self.jump_merge_btn = Button(links_frame, text="Document Merge", bootstyle="link", command=lambda: self._jump_to_section("merge"))
        self.jump_merge_btn.pack(side=LEFT, padx=5)

        self.jump_security_btn = Button(links_frame, text="Security Analysis", bootstyle="link", command=lambda: self._jump_to_section("security"))
        self.jump_security_btn.pack(side=LEFT, padx=5)

        self.jump_testing_btn = Button(links_frame, text="File Testing", bootstyle="link", command=lambda: self._jump_to_section("testing"))
        self.jump_testing_btn.pack(side=LEFT, padx=5)

        self.jump_setup_btn = Button(links_frame, text="Setup Guide", bootstyle="link", command=lambda: self._jump_to_section("setup"))
        self.jump_setup_btn.pack(side=LEFT, padx=5)

        # Main documentation text area
        text_frame = Frame(docs_frame)
        text_frame.pack(fill=BOTH, expand=YES)

        self.docs_text = Text(text_frame, wrap="word", font=("TkDefaultFont", 10), state="disabled")
        docs_scrollbar = Scrollbar(text_frame, command=self.docs_text.yview)
        self.docs_text.config(yscrollcommand=docs_scrollbar.set)

        self.docs_text.pack(side=LEFT, fill=BOTH, expand=YES)
        docs_scrollbar.pack(side=RIGHT, fill=Y)

        # Load documentation content
        self._load_documentation()

    def _jump_to_section(self, section):
        """Jump to a specific section in the documentation"""
        section_marks = {
            "review": "CODE_REVIEW_SECTION",
            "merge": "DOCUMENT_MERGE_SECTION",
            "security": "SECURITY_ANALYSIS_SECTION",
            "testing": "FILE_TESTING_SECTION",
            "setup": "SETUP_SECTION"
        }
        
        if section in section_marks:
            mark = section_marks[section]
            try:
                # First, make sure we can see the mark
                self.docs_text.see(mark)
                
                # Get the line with the mark and highlight it briefly
                start_line = self.docs_text.index(f"{mark} linestart")
                end_line = self.docs_text.index(f"{mark} lineend")
                
                # Clear any existing highlights
                self.docs_text.tag_delete("highlight")
                
                # Add highlight to the section header
                self.docs_text.tag_add("highlight", start_line, end_line)
                self.docs_text.tag_config("highlight", background="yellow", foreground="black")
                
                # Remove highlight after 2 seconds
                self.after(2000, lambda: self.docs_text.tag_delete("highlight"))
                
            except tk.TclError:
                # If mark not found, scroll to top as fallback
                self.docs_text.see("1.0")

    def _load_documentation(self):
        """Load the complete documentation content"""
        docs_content = """🐺 WOLFKIT DOCUMENTATION
================================

Try, Test, Trust - Your AI-Powered Development Workflow

Wolfkit helps developers safely test AI-generated code and intelligently organize documents using a powerful backup/rollback system with AI analysis and comprehensive security scanning.

VERSION: v1.3.1+ with Security Analysis


📋 TABLE OF CONTENTS
===================

1. CODE REVIEW - AI-Powered Analysis
2. DOCUMENT MERGE - Intelligent Clustering
3. SECURITY ANALYSIS - Vulnerability Scanning
4. FILE TESTING - Core File Staging
5. SETUP GUIDE - Getting Started
6. TROUBLESHOOTING - Common Issues
7. TIPS & BEST PRACTICES


🤖 CODE REVIEW - AI-Powered Analysis  
====================================

PURPOSE: Catch issues in AI-generated code before deployment

WORKFLOW:
1. CONFIGURATION CHECK
   • Click "Check Configuration" to verify OpenAI API setup
   • Must show ✅ Ready before proceeding

2. SELECT FILES FOR ANALYSIS
   • Click "Select Files to Analyze"
   • Choose code files (Python, JavaScript, HTML, CSS, etc.)
   • Supports multiple file selection

3. ANALYZE FILES
   • Click "🔍 Analyze Files"
   • AI will examine code for:
     - Syntax errors
     - Missing imports
     - Logic gaps
     - Undefined functions
     - Best practice violations

4. REVIEW RESULTS
   • Analysis appears in output area
   • Professional markdown report saved to /reports/
   • Click "📄 Open Last Report" to view full analysis

5. TAKE ACTION
   • Fix any issues found
   • Re-analyze if needed
   • Proceed to Security Analysis for vulnerability checking
   • Finally move to File Testing for staging

SUPPORTED FILE TYPES:
• Python (.py)
• JavaScript (.js), TypeScript (.ts)
• HTML (.html), CSS (.css)
• JSON (.json)
• Markdown (.md), Text (.txt)

COST ESTIMATE:
• ~$0.002-0.005 per file using gpt-4o-mini
• ~100 file analyses = $0.20-0.50
• No subscription required!

BEST PRACTICES:
• Analyze files BEFORE security scanning
• Review generated reports for insights
• Use "Clear Selection" to reset between batches
• Keep reports for project documentation


📄 DOCUMENT MERGE - Intelligent Clustering
==========================================

PURPOSE: Automatically cluster and merge related documents using AI

WORKFLOW:
1. CONFIGURATION CHECK
   • Click "Check Configuration" 
   • Verify OpenAI API setup (same as Code Review)

2. SELECT DOCUMENT FOLDER
   • Click "Select Document Folder"
   • Choose folder containing documents to organize
   • Supports: PDF, Word, Text, Markdown, Code files

3. CONFIGURE CLUSTERING
   • Set number of clusters manually (2-20)
   • OR click "Auto" for automatic detection
   • Auto uses smart algorithms to find optimal groupings

4. ANALYZE DOCUMENTS
   • Click "🔍 Analyze Documents"
   • AI will:
     - Extract content from all documents
     - Generate semantic embeddings
     - Cluster similar documents together
     - Create merge previews

5. REVIEW CLUSTER CARDS
   Each cluster shows:
   • Similarity percentage
   • List of documents (expandable)
   • Suggested merge filename (editable)
   • Content preview (expandable)

6. MERGE CLUSTERS
   • Edit merge filename if desired
   • Click "🔄 Merge This Cluster"
   • Choose output directory
   • AI creates merged document
   • Option to open result immediately

CLUSTER CARD ACTIONS:
• 🔄 Merge This Cluster: Perform the merge
• 👁 Preview Only: View full merge content in popup
• ❌ Skip: Ignore this cluster

SUPPORTED FORMATS:
• PDF documents (.pdf)
• Microsoft Word (.docx, .doc)
• Text files (.txt, .md)
• Code files (.py, .js, .html, .css)

AUTO-CLUSTERING LOGIC:
• Analyzes document similarity using AI embeddings
• Calculates optimal cluster count based on content
• May create fewer clusters if documents are very similar
• Minimum 2 clusters, scales with document count

COST ESTIMATE:
• ~$0.01-0.05 per document batch for clustering
• ~$0.02-0.10 per merged document
• Depends on document size and complexity

USE CASES:
• Consolidate multiple resume versions
• Merge related research papers
• Organize meeting notes by topic
• Combine code documentation
• Clean up duplicate project files


🛡️ SECURITY ANALYSIS - Vulnerability Scanning
==============================================

PURPOSE: Comprehensive security vulnerability detection for any codebase

WORKFLOW:
1. CONFIGURATION CHECK
   • Click "Check Configuration" to verify analyzer setup
   • Shows ✅ Ready when properly configured
   • No API keys required - completely local analysis

2. SELECT CODEBASE DIRECTORY
   • Click "Select Codebase Directory"
   • Choose root folder of your project
   • Analyzer will scan all source files recursively

3. CONFIGURE ANALYSIS OPTIONS
   • Include dependencies: Scan dependency files
   • Include config files: Check .env, settings, etc.
   • Quick scan mode: Faster analysis with core patterns
   • Minimum severity: Filter by CRITICAL/HIGH/MEDIUM/LOW

4. RUN SECURITY ANALYSIS
   • Click "🔍 Run Security Analysis"
   • Analysis runs in background (non-blocking)
   • Real-time progress updates in console
   • Estimated completion time shown

5. REVIEW SECURITY RESULTS
   • Risk level displayed: CRITICAL/HIGH/MEDIUM/LOW
   • Risk score: 0-100 scale with detailed breakdown
   • Findings summary by severity
   • Framework and database detection results

6. EXPORT DETAILED REPORT
   • Click "📄 Export Report" for full analysis
   • Professional markdown report saved to /reports/
   • Includes executive summary and technical details
   • Click "📂 Open Report" to view in external application

SECURITY CATEGORIES (OWASP-Aligned):
• Broken Access Control (unprotected endpoints)
• Cryptographic Failures (weak crypto, hardcoded secrets)
• Injection Vulnerabilities (SQL injection, XSS, command injection)
• Security Misconfiguration (debug mode, insecure CORS)
• Framework Security (FastAPI, Flask, Django specific issues)

VULNERABILITY DETECTION:
• SQL Injection: Unsafe query construction patterns
• Cross-Site Scripting (XSS): Unsafe HTML rendering
• Hardcoded Secrets: API keys, passwords in source code
• Weak Cryptography: MD5, SHA1, weak encryption algorithms
• Insecure Authentication: Missing auth decorators, weak sessions
• Configuration Issues: Debug mode, exposed info, insecure CORS

FRAMEWORK-SPECIFIC ANALYSIS:
• FastAPI: Missing CORS middleware, no rate limiting, unprotected endpoints
• Flask: Missing SECRET_KEY, no CSRF protection, insecure sessions
• Django: DEBUG=True in production, missing security middleware
• Generic: Access control issues, injection patterns, crypto problems

SUPPORTED FILE TYPES:
• Source Code: .py, .js, .ts, .jsx, .tsx, .html, .css
• Configuration: .env, .yml, .yaml, .json, .ini, .config
• Documentation: .md, .txt
• Container: Dockerfile, docker-compose.yml

ANALYSIS FEATURES:
• Zero Cost: Completely local analysis, no API calls
• Fast Scanning: Optimized pattern matching engine
• Confidence Levels: HIGH/MEDIUM/LOW confidence ratings
• Risk Scoring: Weighted algorithm considering severity and category
• Professional Reports: Executive summary + technical details
• CWE References: Common Weakness Enumeration IDs for each finding

COST ESTIMATE:
• FREE - No API calls, completely local analysis
• No network dependencies or rate limits
• Privacy-focused: All code stays on your machine

EXAMPLE WORKFLOW:
1. Code Review → Fix syntax/logic issues
2. Document Merge → Organize project documentation  
3. Security Analysis → Identify vulnerabilities
4. File Testing → Test secure, reviewed code
5. Deploy with confidence

BEST PRACTICES:
• Run security analysis after code review
• Focus on CRITICAL and HIGH severity findings first
• Review MEDIUM confidence findings for false positives
• Export reports for security documentation
• Re-scan after fixing vulnerabilities
• Integrate into CI/CD pipeline for continuous security


📁 FILE TESTING - Core File Staging
====================================

PURPOSE: Safely test AI-generated files in real projects with instant rollback

WORKFLOW:
1. SET PROJECT DIRECTORY
   • Click "Set Project Directory"
   • Choose your target project folder
   • Wolfkit will work within this directory

2. SELECT TEST FILES
   • Click "Select File(s) to Test"
   • Choose one or more files to test
   • For each file, decide:
     - REPLACE: Choose existing project file to replace
     - ADD NEW: Choose folder to add file to

3. CHOOSE LAUNCH TYPE
   • Python App: Runs main.py in project directory
   • Static Web Page: Opens index.html in browser

4. RUN TEST
   • Click "Run Test" to launch your project
   • Test the new functionality
   • Check console output for any issues

5. DECISION TIME
   • ACCEPT BATCH: Keep all test files, delete backups
   • REVERT BATCH: Restore original files, remove test files

SAFETY FEATURES:
• Automatic backups before any file replacement
• Batch operations (accept/revert multiple files at once)
• Auto-detects project virtual environments
• All operations logged to console

EXAMPLE WORKFLOW:
Project: my-web-app/
Test file: new-component.js
Action: Replace src/components/old-component.js
Result: old-component.js backed up, new-component.js staged
Test: Launch app, verify new component works
Decision: Accept (keep new) or Revert (restore old)


🚀 SETUP GUIDE
===============

INITIAL SETUP:
1. Ensure Python 3.8+ is installed
2. Install dependencies: pip install -r requirements.txt
3. Create .env file in project root (for AI features only)
4. Add your OpenAI API key: OPENAI_API_KEY=sk-your-key-here

OPENAI API KEY (Optional - Only for AI Features):
• Get key from: https://platform.openai.com/api-keys
• Required for Code Review and Document Merge features
• Security Analysis works without API key (local only)
• Estimated cost: $0.002-0.05 per analysis (very affordable!)

OPTIONAL SETTINGS:
• OPENAI_MODEL=gpt-4o-mini (default, recommended for cost)
• OPENAI_MODEL=gpt-4o (premium quality, 15x more expensive)

VERIFICATION:
• Use "Check Configuration" buttons in Code Review and Document Merge tabs
• Security Analysis "Check Configuration" verifies local analyzer
• Should show ✅ Ready messages when properly configured


🔧 TROUBLESHOOTING
==================

COMMON ISSUES:

"No OpenAI API key found" (Code Review/Document Merge)
• Create .env file in project root
• Add: OPENAI_API_KEY=your-actual-key
• Restart Wolfkit

"Security analyzer configuration error"
• Restart Wolfkit to reload pattern engine
• Check Python version (3.8+ required)
• Verify file permissions in project directory

"Analysis failed" / "Merge failed"
• Check internet connection (for AI features)
• Verify API key is valid
• Try smaller batch of files
• Check OpenAI API usage limits

"No project directory set"
• Click "Set Project Directory" in File Testing tab
• Choose a valid folder with your project files

"No files selected"
• Use file selection buttons before running operations
• Ensure files exist and are accessible

Virtual Environment Issues
• Wolfkit auto-detects venv in project directory
• Manually activate venv if needed: venv/Scripts/activate
• Check Python path in console output

File Permission Errors
• Ensure Wolfkit has read/write access to project folder
• Run as administrator if needed (Windows)
• Check file locks (close editors/IDEs)

Large Document Processing
• Very large PDFs may timeout
• Break into smaller batches
• Check available system memory

Security Analysis Issues
• Large codebases may take several minutes
• Use Quick Scan mode for faster results
• Check file encoding if analysis fails on specific files

API Rate Limits
• OpenAI has usage limits per minute/day
• Wait a moment and retry
• Consider upgrading API plan for heavy usage


💡 TIPS & BEST PRACTICES
========================

OPTIMAL WORKFLOW:
1. **🤖 Code Review**: Analyze LLM-generated code for issues before deployment
2. **📄 Document Merge**: Organize and consolidate project documentation
3. **🛡️ Security Analysis**: Scan for vulnerabilities and security issues
4. **🚀 File Testing**: Stage and test secure, reviewed code safely
5. **📖 Documentation**: Reference this guide for any questions

FILE TESTING TIPS:
• Always set project directory first
• Test with one file before batch operations
• Use descriptive commit messages in git before testing
• Keep console output visible for feedback

CODE REVIEW TIPS:
• Analyze before staging - catch issues early
• Save reports for documentation
• Review AI suggestions carefully
• Use for learning - understand common patterns

SECURITY ANALYSIS TIPS:
• Run after code review to catch vulnerabilities
• Focus on CRITICAL and HIGH severity findings first
• Review MEDIUM confidence findings for false positives
• Export reports for security documentation
• Re-scan after fixing issues

DOCUMENT MERGE TIPS:
• Organize files in folders by topic first
• Review cluster suggestions before merging
• Edit merge filenames to be descriptive
• Keep original files as backup

COST OPTIMIZATION:
• Use gpt-4o-mini for most tasks (recommended)
• Security Analysis is completely free (local only)
• Batch similar files together
• Review/edit files before AI analysis
• Monitor usage on OpenAI dashboard

WORKFLOW INTEGRATION:
1. Code Review → Find syntax/logic issues
2. Security Analysis → Identify vulnerabilities  
3. Fix issues manually
4. File Testing → Stage and test secure code
5. Document Merge → Organize final outputs

SAFETY PRACTICES:
• Always backup projects before major changes
• Test in isolated project copies first
• Use version control (git) alongside Wolfkit
• Review all AI-generated content manually

PROJECT ORGANIZATION:
• Keep test files in separate folder
• Use consistent naming conventions
• Document your Wolfkit workflow in README
• Share analysis reports with team

Remember: Wolfkit enhances your workflow but doesn't replace good development practices. Always review AI suggestions, validate security findings, and test thoroughly!


🐺 HAPPY CODING WITH WOLFKIT!
=============================

For more information, visit: https://github.com/your-username/wolfkit
Report issues: https://github.com/your-username/wolfkit/issues

"The best code review is the one that happens before you deploy. The best security analysis is the one that happens before you stage." 🐺

"""

        # Load content first, then create section marks
        self.docs_text.config(state="normal")
        self.docs_text.delete("1.0", "end")
        self.docs_text.insert("1.0", docs_content)
        
        # Now search for section headers and create marks at correct positions
        content = self.docs_text.get("1.0", "end")
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            # Search for section headers and create marks
            if "🤖 CODE REVIEW - AI-Powered Analysis" in line:
                self.docs_text.mark_set("CODE_REVIEW_SECTION", f"{line_num}.0")
            elif "📄 DOCUMENT MERGE - Intelligent Clustering" in line:
                self.docs_text.mark_set("DOCUMENT_MERGE_SECTION", f"{line_num}.0")
            elif "🛡️ SECURITY ANALYSIS - Vulnerability Scanning" in line:
                self.docs_text.mark_set("SECURITY_ANALYSIS_SECTION", f"{line_num}.0")
            elif "📁 FILE TESTING - Core File Staging" in line:
                self.docs_text.mark_set("FILE_TESTING_SECTION", f"{line_num}.0")
            elif "🚀 SETUP GUIDE" in line:
                self.docs_text.mark_set("SETUP_SECTION", f"{line_num}.0")
        
        # Make marks persistent (survive text modifications)
        for mark in ["CODE_REVIEW_SECTION", "DOCUMENT_MERGE_SECTION", "SECURITY_ANALYSIS_SECTION", "FILE_TESTING_SECTION", "SETUP_SECTION"]:
            try:
                self.docs_text.mark_gravity(mark, "left")
            except tk.TclError:
                pass  # Mark doesn't exist, that's okay
        
        self.docs_text.config(state="disabled")