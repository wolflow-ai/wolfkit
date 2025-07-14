# security_patterns.py
"""
Security Pattern Detection for Wolfkit Security Analysis
Comprehensive pattern matching for common security vulnerabilities
"""
import re
from typing import List, Dict, Tuple, Optional, Pattern
from dataclasses import dataclass


@dataclass
class PatternMatch:
    """Container for pattern match results"""
    pattern_name: str
    line_number: int
    code_snippet: str
    full_line: str
    confidence: str  # HIGH, MEDIUM, LOW


# === Framework Detection Patterns ===

FRAMEWORK_PATTERNS = {
    "web_framework": {
        "fastapi": [
            r"from\s+fastapi",
            r"FastAPI\s*\(",
            r"@app\.(get|post|put|delete|patch)",
            r"APIRouter\s*\("
        ],
        "flask": [
            r"from\s+flask",
            r"Flask\s*\(",
            r"@app\.route",
            r"request\.(args|form|json)"
        ],
        "django": [
            r"from\s+django",
            r"Django",
            r"settings\.py",
            r"@login_required",
            r"HttpResponse"
        ],
        "express": [
            r"express\s*\(",
            r"app\.(get|post|put|delete)",
            r"req\.(body|params|query)",
            r"res\.(send|json)"
        ],
        "spring": [
            r"@RestController",
            r"@SpringBootApplication",
            r"@RequestMapping",
            r"@GetMapping|@PostMapping"
        ]
    },
    "database": {
        "postgresql": [
            r"psycopg2",
            r"asyncpg",
            r"postgresql://",
            r"postgres://"
        ],
        "mysql": [
            r"mysql",
            r"pymysql",
            r"mysql://",
            r"MySQLdb"
        ],
        "mongodb": [
            r"pymongo",
            r"mongoose",
            r"mongodb://",
            r"MongoClient"
        ],
        "sqlite": [
            r"sqlite3",
            r"database\.db",
            r"\.sqlite",
            r"PRAGMA"
        ]
    },
    "authentication": {
        "jwt": [
            r"jwt",
            r"jsonwebtoken",
            r"python-jose",
            r"encode\(.*jwt",
            r"decode\(.*jwt"
        ],
        "oauth": [
            r"oauth",
            r"passport",
            r"authlib",
            r"OAuth2"
        ],
        "session": [
            r"session\[",
            r"flask-session",
            r"express-session"
        ]
    }
}

# === Authentication & Authorization Patterns ===

AUTHENTICATION_PATTERNS = {
    "unprotected_endpoints": {
        "vulnerable": [
            r"@app\.(get|post|put|delete|patch)\s*\([\"'][^\"']*[\"']\s*\)\s*\n\s*def\s+\w+\s*\([^)]*\):",
            r"@router\.(get|post|put|delete|patch)\s*\([\"'][^\"']*[\"']\s*\)\s*\n\s*def\s+\w+\s*\([^)]*\):",
            r"app\.(get|post|put|delete)\s*\([\"'][^\"']*[\"'],\s*function",
            r"def\s+\w+\s*\([^)]*request[^)]*\):",  # Direct request handlers
        ],
        "safe": [
            r"@.*auth.*required",
            r"@.*login.*required",
            r"@.*permission.*required",
            r"Depends\(.*auth",
            r"middleware.*auth"
        ]
    },
    "session_security": {
        "insecure": [
            r"session\[.*\]\s*=.*(?!.*secure)",
            r"set_cookie\(.*(?!.*secure=True)",
            r"set_cookie\(.*(?!.*httponly=True)",
            r"set_cookie\(.*(?!.*samesite)",
            r"SESSION_COOKIE_SECURE\s*=\s*False",
            r"SESSION_COOKIE_HTTPONLY\s*=\s*False"
        ],
        "secure": [
            r"secure\s*=\s*True",
            r"httponly\s*=\s*True",
            r"samesite\s*=\s*[\"']strict[\"']",
            r"SESSION_COOKIE_SECURE\s*=\s*True"
        ]
    },
    "password_handling": {
        "vulnerable": [
            r"password\s*==\s*[\"'][^\"']+[\"']",  # Plain text comparison
            r"\.password\s*=\s*[\"'][^\"']+[\"']",  # Direct assignment
            r"check_password\([^)]*,\s*[\"'][^\"']+[\"']\)",  # Hardcoded password
        ],
        "safe": [
            r"bcrypt\.",
            r"scrypt\.",
            r"pbkdf2",
            r"hash_password\(",
            r"check_password_hash\(",
            r"verify_password\("
        ]
    }
}

# === Injection Vulnerability Patterns ===

INJECTION_PATTERNS = {
    "sql_injection": {
        "vulnerable": [
            r"execute\s*\([^,)]*%[^,)]*\)",  # String formatting
            r"execute\s*\([^,)]*\+[^,)]*\)",  # String concatenation
            r"f[\"'].*(SELECT|INSERT|UPDATE|DELETE).*{.*}.*[\"']",  # f-strings in SQL
            r"format\s*\([^)]*\)\s*(?=.*SELECT|.*INSERT|.*UPDATE|.*DELETE)",
            r"(SELECT|INSERT|UPDATE|DELETE).*[\"']\s*\+",  # Concatenated queries
            r"cursor\.execute\s*\([^,)]*%",
            r"query\s*=.*[\"']\s*\+.*[\"']",  # Query building with +
        ],
        "safe": [
            r"execute\s*\([^,)]*,\s*[\[\(]",  # Parameterized queries
            r"\.prepare\s*\(",  # Prepared statements
            r"sqlalchemy.*text\s*\([^,)]*,",  # SQLAlchemy with params
            r"cursor\.execute\s*\([^,)]*,\s*[\[\(]",
            r"executemany\s*\("
        ]
    },
    "xss_prevention": {
        "vulnerable": [
            r"innerHTML\s*=.*\+",  # Direct HTML injection
            r"innerHTML\s*=.*[\"']\s*\+",
            r"document\.write\s*\(",  # Direct document writing
            r"eval\s*\(",  # Code evaluation
            r"setTimeout\s*\([\"'][^\"']*\+",  # Dynamic code in timeout
            r"setInterval\s*\([\"'][^\"']*\+",
            r"new\s+Function\s*\(",  # Dynamic function creation
            r"outerHTML\s*=.*\+"
        ],
        "safe": [
            r"escape\s*\(",  # HTML escaping
            r"sanitize\s*\(",  # Input sanitization
            r"textContent\s*=",  # Safe text insertion
            r"createTextNode\s*\(",
            r"\.text\s*\(",  # jQuery text method
            r"DOMPurify\.sanitize"
        ]
    },
    "command_injection": {
        "vulnerable": [
            r"os\.system\s*\([^)]*\+",
            r"subprocess\.(call|run|Popen)\s*\([^)]*\+",
            r"exec\s*\([^)]*\+",
            r"eval\s*\([^)]*input",
            r"shell=True.*\+",  # Shell injection via subprocess
        ],
        "safe": [
            r"subprocess\.(call|run|Popen)\s*\(\s*\[",  # List arguments
            r"shlex\.quote",
            r"shell=False"
        ]
    }
}

# === Secret Management Patterns ===

SECRET_PATTERNS = {
    "hardcoded_secrets": [
        r"password\s*=\s*[\"'][^\"']{8,}[\"']",
        r"api_?key\s*=\s*[\"'][A-Za-z0-9]{15,}[\"']",
        r"secret\s*=\s*[\"'][^\"']{16,}[\"']",
        r"token\s*=\s*[\"'][A-Za-z0-9]{20,}[\"']",
        r"SECRET_KEY\s*=\s*[\"'][^\"']{16,}[\"']",
        r"private_key\s*=\s*[\"'][^\"']{20,}[\"']",
        r"database_url\s*=\s*[\"'][^\"']*://[^\"']+:[^\"']+@",
        r"mongodb://[^\"']*:[^\"']*@",
        r"mysql://[^\"']*:[^\"']*@",
        r"postgresql://[^\"']*:[^\"']*@"
    ],
    "environment_variables": [
        r"os\.environ\s*\[\s*[\"'][^\"']+[\"']\s*\]",
        r"os\.getenv\s*\(",
        r"process\.env\.",
        r"System\.getenv\s*\("
    ],
    "weak_secrets": [
        r"password\s*=\s*[\"'](password|123456|admin|root|test)[\"']",
        r"secret\s*=\s*[\"'](secret|key|password)[\"']",
        r"token\s*=\s*[\"'](token|test|demo)[\"']"
    ]
}

# === Cryptographic Security Patterns ===

CRYPTO_PATTERNS = {
    "weak_algorithms": [
        r"md5\s*\(",
        r"sha1\s*\(",
        r"DES\s*\(",
        r"RC4\s*\(",
        r"hashlib\.md5",
        r"hashlib\.sha1",
        r"Cipher\.DES",
        r"crypto\.createHash\s*\(\s*[\"']md5[\"']",
        r"crypto\.createHash\s*\(\s*[\"']sha1[\"']"
    ],
    "strong_algorithms": [
        r"sha256\s*\(",
        r"sha512\s*\(",
        r"bcrypt\.",
        r"scrypt\.",
        r"pbkdf2",
        r"AES\.",
        r"hashlib\.sha256",
        r"hashlib\.sha512",
        r"crypto\.createHash\s*\(\s*[\"']sha256[\"']"
    ],
    "insecure_random": [
        r"random\.random\s*\(",
        r"Math\.random\s*\(",
        r"rand\s*\(",
        r"srand\s*\("
    ],
    "secure_random": [
        r"secrets\.",
        r"os\.urandom\s*\(",
        r"crypto\.getRandomValues",
        r"SecureRandom\."
    ]
}

# === Framework-Specific Patterns ===

FASTAPI_PATTERNS = {
    "security_issues": [
        r"@app\.(get|post|put|delete)\s*\([^)]*\)\s*\n\s*def\s+\w+\s*\([^)]*\):\s*(?!.*Depends)",
        r"CORSMiddleware.*allow_origins\s*=\s*\[\s*[\"']\*[\"']\s*\]",  # Allow all origins
        r"app\.add_middleware.*allow_credentials\s*=\s*True.*allow_origins\s*=.*\*",
    ],
    "missing_features": [
        r"(?!.*CORSMiddleware).*FastAPI\s*\(",  # Missing CORS
        r"(?!.*rate.*limit).*@app\.(get|post|put|delete)",  # No rate limiting
    ]
}

FLASK_PATTERNS = {
    "security_issues": [
        r"app\.config\s*\[\s*[\"']SECRET_KEY[\"']\s*\]\s*=\s*[\"'][^\"']{1,15}[\"']",  # Weak secret
        r"@app\.route\s*\([^)]*\)\s*\n\s*def\s+\w+\s*\([^)]*\):\s*(?!.*login_required)",
        r"session\s*\[\s*[\"'][^\"']+[\"']\s*\]\s*=.*(?!.*secure)",
    ],
    "missing_features": [
        r"(?!.*csrf).*Flask\s*\(",  # Missing CSRF protection
        r"(?!.*SECRET_KEY).*Flask\s*\(",  # Missing secret key
    ]
}

# === Configuration Security Patterns ===

CONFIG_PATTERNS = {
    "debug_enabled": [
        r"DEBUG\s*=\s*True",
        r"debug\s*=\s*True",
        r"app\.debug\s*=\s*True",
        r"--debug",
        r"development.*mode"
    ],
    "insecure_cors": [
        r"Access-Control-Allow-Origin:\s*\*",
        r"allow_origins\s*=\s*\[\s*[\"']\*[\"']\s*\]",
        r"cors.*origin.*\*"
    ],
    "exposed_info": [
        r"server.*banner",
        r"X-Powered-By",
        r"expose.*header",
        r"traceback.*show"
    ]
}


class PatternMatcher:
    """Main pattern matching engine"""
    
    def __init__(self):
        self.compiled_patterns = self._compile_patterns()
    
    def _compile_patterns(self) -> Dict[str, Dict[str, List[Pattern]]]:
        """Compile all regex patterns for performance"""
        compiled = {}
        
        all_pattern_groups = {
            'authentication': AUTHENTICATION_PATTERNS,
            'injection': INJECTION_PATTERNS,
            'secrets': SECRET_PATTERNS,
            'crypto': CRYPTO_PATTERNS,
            'fastapi': FASTAPI_PATTERNS,
            'flask': FLASK_PATTERNS,
            'config': CONFIG_PATTERNS,
            'framework': FRAMEWORK_PATTERNS
        }
        
        for group_name, pattern_group in all_pattern_groups.items():
            compiled[group_name] = {}
            for category, patterns in pattern_group.items():
                if isinstance(patterns, dict):
                    compiled[group_name][category] = {}
                    for subcategory, pattern_list in patterns.items():
                        compiled[group_name][category][subcategory] = [
                            re.compile(pattern, re.IGNORECASE | re.MULTILINE)
                            for pattern in pattern_list
                        ]
                else:
                    compiled[group_name][category] = [
                        re.compile(pattern, re.IGNORECASE | re.MULTILINE)
                        for pattern in patterns
                    ]
        
        return compiled
    
    def find_matches(self, content: str, file_path: str) -> List[PatternMatch]:
        """Find all pattern matches in content"""
        matches = []
        lines = content.split('\n')
        
        # Check each pattern group
        for group_name, group_patterns in self.compiled_patterns.items():
            group_matches = self._find_group_matches(
                lines, group_patterns, group_name, file_path
            )
            matches.extend(group_matches)
        
        return matches
    
    def _find_group_matches(self, lines: List[str], patterns: Dict, 
                           group_name: str, file_path: str) -> List[PatternMatch]:
        """Find matches for a specific pattern group"""
        matches = []
        
        for line_num, line in enumerate(lines, 1):
            for category, pattern_set in patterns.items():
                if isinstance(pattern_set, dict):
                    # Handle nested pattern structure
                    for subcategory, compiled_patterns in pattern_set.items():
                        for pattern in compiled_patterns:
                            if pattern.search(line):
                                confidence = self._determine_confidence(
                                    group_name, category, subcategory, line
                                )
                                matches.append(PatternMatch(
                                    pattern_name=f"{group_name}.{category}.{subcategory}",
                                    line_number=line_num,
                                    code_snippet=line.strip(),
                                    full_line=line,
                                    confidence=confidence
                                ))
                else:
                    # Handle flat pattern structure
                    for pattern in pattern_set:
                        if pattern.search(line):
                            confidence = self._determine_confidence(
                                group_name, category, None, line
                            )
                            matches.append(PatternMatch(
                                pattern_name=f"{group_name}.{category}",
                                line_number=line_num,
                                code_snippet=line.strip(),
                                full_line=line,
                                confidence=confidence
                            ))
        
        return matches
    
    def _determine_confidence(self, group: str, category: str, 
                            subcategory: Optional[str], line: str) -> str:
        """Determine confidence level for a match"""
        # High confidence patterns
        high_confidence = [
            'hardcoded_secrets', 'weak_algorithms', 'sql_injection.vulnerable',
            'debug_enabled', 'command_injection.vulnerable'
        ]
        
        # Low confidence patterns (might be false positives)
        low_confidence = [
            'unprotected_endpoints', 'missing_features', 'framework'
        ]
        
        pattern_key = f"{category}.{subcategory}" if subcategory else category
        
        if any(hc in pattern_key for hc in high_confidence):
            return "HIGH"
        elif any(lc in pattern_key for lc in low_confidence):
            return "LOW"
        else:
            return "MEDIUM"
    
    def detect_framework(self, content: str) -> Optional[str]:
        """Detect the primary framework used in the codebase"""
        framework_scores = {}
        
        for framework, patterns in FRAMEWORK_PATTERNS['web_framework'].items():
            score = 0
            for pattern_str in patterns:
                pattern = re.compile(pattern_str, re.IGNORECASE)
                matches = len(pattern.findall(content))
                score += matches
            
            if score > 0:
                framework_scores[framework] = score
        
        if framework_scores:
            return max(framework_scores, key=framework_scores.get)
        
        return None
    
    def detect_database(self, content: str) -> Optional[str]:
        """Detect the primary database technology used"""
        db_scores = {}
        
        for db_type, patterns in FRAMEWORK_PATTERNS['database'].items():
            score = 0
            for pattern_str in patterns:
                pattern = re.compile(pattern_str, re.IGNORECASE)
                matches = len(pattern.findall(content))
                score += matches
            
            if score > 0:
                db_scores[db_type] = score
        
        if db_scores:
            return max(db_scores, key=db_scores.get)
        
        return None