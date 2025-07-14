# security_analyzer.py
"""
Core Security Analyzer for Wolfkit
Orchestrates comprehensive security analysis of codebases
"""
import os
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Tuple, Set
from dataclasses import dataclass, field

# Local imports for patterns and detection
from security_patterns import PatternMatcher, PatternMatch


@dataclass
class SecurityFinding:
    """Individual security finding with complete metadata"""
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW, INFO
    category: str  # OWASP category or custom category
    issue: str     # Brief description of the issue
    file_path: str # File where issue was found
    line_number: Optional[int] = None # Line number if applicable
    code_snippet: Optional[str] = None # Relevant code snippet
    recommendation: str = "" # How to fix the issue
    confidence: str = "MEDIUM" # HIGH, MEDIUM, LOW confidence in finding
    cwe_id: Optional[str] = None # Common Weakness Enumeration ID
    pattern_name: str = "" # Internal pattern identifier


@dataclass 
class SecurityReport:
    """Complete security analysis report"""
    scan_date: datetime
    codebase_path: str
    framework_detected: Optional[str]
    database_type: Optional[str]
    total_files_scanned: int
    findings: List[SecurityFinding] = field(default_factory=list)
    risk_score: int = 0  # 0-100 calculated risk score
    summary_stats: Dict[str, int] = field(default_factory=dict)


class CodebaseSecurityAnalyzer:
    """
    Main security analyzer that orchestrates all security checks
    """
    
    def __init__(self, codebase_path: str):
        """
        Initialize the security analyzer
        
        Args:
            codebase_path: Path to the codebase to analyze
        """
        self.codebase_path = Path(codebase_path).resolve()
        self.findings: List[SecurityFinding] = []
        self.framework_detected: Optional[str] = None
        self.database_type: Optional[str] = None
        self.files_scanned: int = 0
        
        # Initialize pattern matcher
        self.pattern_matcher = PatternMatcher()
        
        # File extensions to analyze
        self.source_extensions = {
            '.py', '.js', '.ts', '.jsx', '.tsx', '.html', '.css', 
            '.json', '.md', '.txt', '.yml', '.yaml', '.env', 
            '.config', '.cfg', '.ini', '.toml'
        }
        
        # Directories to skip for performance
        self.skip_dirs = {
            'node_modules', 'venv', 'env', '.git', '__pycache__',
            '.pytest_cache', 'dist', 'build', '.vscode', '.idea',
            'coverage', '.coverage', 'htmlcov', '.tox'
        }
    
    def analyze(self) -> SecurityReport:
        """
        Main analysis entry point
        
        Returns:
            Complete security report with findings and metadata
        """
        print(f"Starting security analysis of: {self.codebase_path}")
        
        # Phase 1: Discovery
        print("Phase 1: Discovering architecture...")
        self._discover_architecture()
        
        # Phase 2: Static Analysis
        print("Phase 2: Running static analysis...")
        self._run_static_analysis()
        
        # Phase 3: Framework-specific analysis
        print("Phase 3: Framework-specific analysis...")
        self._run_framework_analysis()
        
        # Phase 4: Generate report
        print("Phase 4: Generating report...")
        return self._generate_report()
    
    def _discover_architecture(self) -> None:
        """
        Identify framework, database, and architecture patterns
        """
        all_content = ""
        
        # Read a sample of files to detect architecture
        sample_files = list(self._get_source_files())[:20]  # Limit for performance
        
        for file_path in sample_files:
            try:
                content = self._read_file(file_path)
                all_content += content + "\n"
            except Exception as e:
                print(f"Warning: Could not read {file_path}: {e}")
                continue
        
        # Detect framework and database
        self.framework_detected = self.pattern_matcher.detect_framework(all_content)
        self.database_type = self.pattern_matcher.detect_database(all_content)
        
        print(f"Framework detected: {self.framework_detected or 'Unknown'}")
        print(f"Database detected: {self.database_type or 'Unknown'}")
    
    def _run_static_analysis(self) -> None:
        """
        Run language-agnostic security analysis on all source files
        """
        source_files = list(self._get_source_files())
        
        for file_path in source_files:
            try:
                self._analyze_file(file_path)
                self.files_scanned += 1
                
                # Progress indication
                if self.files_scanned % 10 == 0:
                    print(f"Analyzed {self.files_scanned} files...")
                    
            except Exception as e:
                print(f"Warning: Could not analyze {file_path}: {e}")
                continue
        
        print(f"Static analysis complete. Scanned {self.files_scanned} files.")
    
    def _analyze_file(self, file_path: Path) -> None:
        """
        Analyze a single file for security issues
        
        Args:
            file_path: Path to the file to analyze
        """
        try:
            content = self._read_file(file_path)
            relative_path = str(file_path.relative_to(self.codebase_path))
            
            # Find pattern matches
            matches = self.pattern_matcher.find_matches(content, relative_path)
            
            # Convert matches to findings
            for match in matches:
                finding = self._pattern_match_to_finding(match, relative_path)
                if finding:
                    self.findings.append(finding)
                    
        except Exception as e:
            # Log error but continue analysis
            print(f"Error analyzing {file_path}: {e}")
    
    def _pattern_match_to_finding(self, match: PatternMatch, file_path: str) -> Optional[SecurityFinding]:
        """
        Convert a pattern match to a security finding
        
        Args:
            match: Pattern match result
            file_path: Relative file path
            
        Returns:
            SecurityFinding or None if match should be ignored
        """
        # Determine severity and category based on pattern
        severity, category, issue, recommendation, cwe_id = self._categorize_pattern(match.pattern_name, match.code_snippet)
        
        # Skip if this is a safe pattern (reduces false positives)
        if severity == "SKIP":
            return None
        
        return SecurityFinding(
            severity=severity,
            category=category,
            issue=issue,
            file_path=file_path,
            line_number=match.line_number,
            code_snippet=match.code_snippet,
            recommendation=recommendation,
            confidence=match.confidence,
            cwe_id=cwe_id,
            pattern_name=match.pattern_name
        )
    
    def _categorize_pattern(self, pattern_name: str, code_snippet: str) -> Tuple[str, str, str, str, Optional[str]]:
        """
        Categorize a pattern match into OWASP categories with metadata
        
        Returns:
            Tuple of (severity, category, issue, recommendation, cwe_id)
        """
        # Authentication patterns
        if "auth" in pattern_name:
            if "unprotected" in pattern_name:
                return ("HIGH", "Broken Access Control", 
                       "Unprotected API endpoint detected",
                       "Add authentication middleware or decorators",
                       "CWE-862")
            elif "session" in pattern_name and "insecure" in pattern_name:
                return ("MEDIUM", "Broken Access Control",
                       "Insecure session configuration",
                       "Enable secure, httponly, and samesite cookie attributes",
                       "CWE-614")
            elif "password" in pattern_name and "vulnerable" in pattern_name:
                return ("HIGH", "Cryptographic Failures",
                       "Weak password handling detected",
                       "Use bcrypt, scrypt, or pbkdf2 for password hashing",
                       "CWE-916")
        
        # Injection patterns
        elif "injection" in pattern_name:
            if "sql" in pattern_name and "vulnerable" in pattern_name:
                return ("HIGH", "Injection",
                       "Potential SQL injection vulnerability",
                       "Use parameterized queries or prepared statements",
                       "CWE-89")
            elif "xss" in pattern_name and "vulnerable" in pattern_name:
                return ("MEDIUM", "Injection",
                       "Potential Cross-Site Scripting (XSS) vulnerability",
                       "Sanitize and escape all user input before rendering",
                       "CWE-79")
            elif "command" in pattern_name and "vulnerable" in pattern_name:
                return ("HIGH", "Injection",
                       "Potential command injection vulnerability",
                       "Use subprocess with list arguments instead of shell=True",
                       "CWE-78")
        
        # Secret management patterns
        elif "secret" in pattern_name:
            if "hardcoded" in pattern_name:
                return ("CRITICAL", "Cryptographic Failures",
                       "Hardcoded secret or credential detected",
                       "Move secrets to environment variables or secure key management",
                       "CWE-798")
            elif "weak" in pattern_name:
                return ("HIGH", "Cryptographic Failures",
                       "Weak or default credentials detected",
                       "Use strong, randomly generated credentials",
                       "CWE-521")
        
        # Cryptographic patterns
        elif "crypto" in pattern_name:
            if "weak" in pattern_name:
                return ("HIGH", "Cryptographic Failures",
                       "Weak cryptographic algorithm detected",
                       "Use SHA-256, SHA-512, AES, or other strong algorithms",
                       "CWE-327")
            elif "insecure_random" in pattern_name:
                return ("MEDIUM", "Cryptographic Failures",
                       "Insecure random number generation",
                       "Use cryptographically secure random generators (secrets module)",
                       "CWE-338")
        
        # Configuration patterns
        elif "config" in pattern_name:
            if "debug" in pattern_name:
                return ("MEDIUM", "Security Misconfiguration",
                       "Debug mode enabled in production",
                       "Disable debug mode in production environments",
                       "CWE-489")
            elif "cors" in pattern_name:
                return ("MEDIUM", "Security Misconfiguration",
                       "Insecure CORS configuration",
                       "Restrict CORS origins to specific trusted domains",
                       "CWE-942")
        
        # Framework-specific patterns
        elif "fastapi" in pattern_name or "flask" in pattern_name:
            if "security_issues" in pattern_name:
                return ("HIGH", "Security Misconfiguration",
                       "Framework security misconfiguration",
                       "Follow framework security best practices",
                       "CWE-16")
            elif "missing" in pattern_name:
                return ("MEDIUM", "Security Misconfiguration",
                       "Missing security feature",
                       "Implement recommended security middleware",
                       "CWE-693")
        
        # Safe patterns (ignore these)
        elif any(safe_word in pattern_name for safe_word in ["safe", "secure", "environment"]):
            return ("SKIP", "", "", "", None)
        
        # Default categorization for unknown patterns
        return ("LOW", "Security Misconfiguration",
               f"Potential security issue detected",
               "Review code for security implications",
               None)
    
    def _run_framework_analysis(self) -> None:
        """
        Run framework-specific security analysis
        """
        if not self.framework_detected:
            print("No specific framework detected, skipping framework analysis.")
            return
        
        print(f"Running {self.framework_detected}-specific analysis...")
        
        if self.framework_detected == "fastapi":
            self._analyze_fastapi_security()
        elif self.framework_detected == "flask":
            self._analyze_flask_security()
        elif self.framework_detected == "django":
            self._analyze_django_security()
    
    def _analyze_fastapi_security(self) -> None:
        """FastAPI-specific security analysis"""
        # Look for specific FastAPI security patterns
        fastapi_files = []
        for file_path in self._get_source_files():
            if file_path.suffix == '.py':
                try:
                    content = self._read_file(file_path)
                    if 'fastapi' in content.lower():
                        fastapi_files.append((file_path, content))
                except Exception:
                    continue
        
        for file_path, content in fastapi_files:
            relative_path = str(file_path.relative_to(self.codebase_path))
            
            # Check for missing CORS middleware
            if 'FastAPI' in content and 'CORSMiddleware' not in content:
                self.findings.append(SecurityFinding(
                    severity="MEDIUM",
                    category="Security Misconfiguration",
                    issue="Missing CORS middleware configuration",
                    file_path=relative_path,
                    recommendation="Add CORSMiddleware with proper origin restrictions",
                    confidence="HIGH",
                    cwe_id="CWE-942"
                ))
            
            # Check for missing rate limiting
            if '@app.' in content and 'slowapi' not in content and 'rate' not in content.lower():
                self.findings.append(SecurityFinding(
                    severity="MEDIUM",
                    category="Security Misconfiguration",
                    issue="No rate limiting detected",
                    file_path=relative_path,
                    recommendation="Implement rate limiting with slowapi or similar",
                    confidence="MEDIUM",
                    cwe_id="CWE-770"
                ))
    
    def _analyze_flask_security(self) -> None:
        """Flask-specific security analysis"""
        flask_files = []
        for file_path in self._get_source_files():
            if file_path.suffix == '.py':
                try:
                    content = self._read_file(file_path)
                    if 'flask' in content.lower():
                        flask_files.append((file_path, content))
                except Exception:
                    continue
        
        for file_path, content in flask_files:
            relative_path = str(file_path.relative_to(self.codebase_path))
            
            # Check for missing SECRET_KEY
            if 'Flask' in content and 'SECRET_KEY' not in content:
                self.findings.append(SecurityFinding(
                    severity="HIGH",
                    category="Cryptographic Failures",
                    issue="Missing Flask SECRET_KEY configuration",
                    file_path=relative_path,
                    recommendation="Configure SECRET_KEY for session security",
                    confidence="HIGH",
                    cwe_id="CWE-798"
                ))
            
            # Check for missing CSRF protection
            if 'Flask' in content and 'csrf' not in content.lower():
                self.findings.append(SecurityFinding(
                    severity="MEDIUM",
                    category="Security Misconfiguration",
                    issue="No CSRF protection detected",
                    file_path=relative_path,
                    recommendation="Implement CSRF protection with Flask-WTF",
                    confidence="MEDIUM",
                    cwe_id="CWE-352"
                ))
    
    def _analyze_django_security(self) -> None:
        """Django-specific security analysis"""
        # Basic Django analysis - can be expanded
        settings_files = []
        for file_path in self._get_source_files():
            if 'settings' in file_path.name.lower() and file_path.suffix == '.py':
                try:
                    content = self._read_file(file_path)
                    settings_files.append((file_path, content))
                except Exception:
                    continue
        
        for file_path, content in settings_files:
            relative_path = str(file_path.relative_to(self.codebase_path))
            
            # Check for DEBUG=True in production
            if 'DEBUG = True' in content:
                self.findings.append(SecurityFinding(
                    severity="HIGH",
                    category="Security Misconfiguration",
                    issue="DEBUG mode enabled",
                    file_path=relative_path,
                    recommendation="Set DEBUG = False in production",
                    confidence="HIGH",
                    cwe_id="CWE-489"
                ))
    
    def _generate_report(self) -> SecurityReport:
        """
        Generate final security report with risk scoring
        
        Returns:
            Complete SecurityReport with all findings and metadata
        """
        # Calculate summary statistics
        summary_stats = self._calculate_summary_stats()
        
        # Calculate risk score
        risk_score = self._calculate_risk_score()
        
        return SecurityReport(
            scan_date=datetime.now(),
            codebase_path=str(self.codebase_path),
            framework_detected=self.framework_detected,
            database_type=self.database_type,
            total_files_scanned=self.files_scanned,
            findings=self.findings,
            risk_score=risk_score,
            summary_stats=summary_stats
        )
    
    def _calculate_summary_stats(self) -> Dict[str, int]:
        """Calculate summary statistics for findings"""
        stats = {
            "CRITICAL": 0,
            "HIGH": 0,
            "MEDIUM": 0,
            "LOW": 0,
            "INFO": 0,
            "total": len(self.findings)
        }
        
        for finding in self.findings:
            stats[finding.severity] = stats.get(finding.severity, 0) + 1
        
        return stats
    
    def _calculate_risk_score(self) -> int:
        """
        Calculate overall risk score (0-100) based on findings
        
        Returns:
            Risk score from 0 (low risk) to 100 (critical risk)
        """
        severity_weights = {
            "CRITICAL": 25,
            "HIGH": 15,
            "MEDIUM": 8,
            "LOW": 3,
            "INFO": 1
        }
        
        category_multipliers = {
            "Broken Access Control": 1.5,
            "Cryptographic Failures": 1.4,
            "Injection": 1.3,
            "Insecure Design": 1.2,
            "Security Misconfiguration": 1.1,
            "Vulnerable Components": 1.0,
            "Authentication Failures": 1.4,
            "Software Integrity Failures": 1.0,
            "Logging Failures": 0.8,
            "Server-Side Request Forgery": 1.1
        }
        
        total_score = 0
        for finding in self.findings:
            base_score = severity_weights.get(finding.severity, 1)
            multiplier = category_multipliers.get(finding.category, 1.0)
            
            # Confidence factor
            confidence_factor = {
                "HIGH": 1.0, 
                "MEDIUM": 0.7, 
                "LOW": 0.4
            }.get(finding.confidence, 0.5)
            
            total_score += base_score * multiplier * confidence_factor
        
        # Normalize to 0-100 scale and apply diminishing returns
        normalized_score = min(100, int(total_score * 0.8))
        return normalized_score
    
    def _get_source_files(self):
        """
        Generator that yields all source files in the codebase
        
        Yields:
            Path objects for source files to analyze
        """
        for root, dirs, files in os.walk(self.codebase_path):
            # Skip directories we don't want to analyze
            dirs[:] = [d for d in dirs if d not in self.skip_dirs]
            
            for file in files:
                file_path = Path(root) / file
                
                # Check if it's a source file we want to analyze
                if (file_path.suffix.lower() in self.source_extensions or
                    file_path.name.lower() in ['.env', 'dockerfile', 'docker-compose.yml']):
                    yield file_path
    
    def _read_file(self, file_path: Path) -> str:
        """
        Safely read file content with encoding detection
        
        Args:
            file_path: Path to file to read
            
        Returns:
            File content as string
        """
        encodings = ['utf-8', 'latin-1', 'cp1252']
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    return f.read()
            except UnicodeDecodeError:
                continue
            except Exception as e:
                raise Exception(f"Could not read file {file_path}: {e}")
        
        raise Exception(f"Could not decode file {file_path} with any supported encoding")


def check_security_analyzer_config() -> Tuple[bool, str]:
    """
    Check if security analyzer is properly configured
    
    Returns:
        Tuple of (success, message)
    """
    try:
        # Test pattern compilation
        matcher = PatternMatcher()
        return True, "✅ Security analyzer ready - all patterns compiled successfully"
    except Exception as e:
        return False, f"❌ Security analyzer configuration error: {str(e)}"