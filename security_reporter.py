# security_reporter.py
"""
Security Report Generation for Wolfkit Security Analysis
Professional report formatting with executive summaries and technical details
"""
import os
from datetime import datetime
from typing import List, Dict, Tuple, Optional
from collections import defaultdict, Counter
from dataclasses import asdict

from security_analyzer import SecurityReport, SecurityFinding


class SecurityReporter:
    """
    Generate professional security reports in multiple formats
    """
    
    def __init__(self, report: SecurityReport):
        """
        Initialize reporter with security report data
        
        Args:
            report: SecurityReport containing analysis results
        """
        self.report = report
        self.reports_dir = self._ensure_reports_directory()
    
    def _ensure_reports_directory(self) -> str:
        """
        Ensure reports directory exists and return path
        
        Returns:
            Absolute path to reports directory
        """
        reports_dir = os.path.abspath("./reports")
        os.makedirs(reports_dir, exist_ok=True)
        return reports_dir
    
    def generate_full_report(self, format_type: str = "markdown") -> Tuple[bool, str, str]:
        """
        Generate complete security report
        
        Args:
            format_type: Output format ('markdown', 'html', 'json')
            
        Returns:
            Tuple of (success, file_path, message)
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"wolfkit_security_analysis_{timestamp}.{format_type}"
            file_path = os.path.join(self.reports_dir, filename)
            
            if format_type == "markdown":
                content = self._generate_markdown_report()
            elif format_type == "html":
                content = self._generate_html_report()
            elif format_type == "json":
                content = self._generate_json_report()
            else:
                return False, "", f"Unsupported format: {format_type}"
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return True, file_path, f"Security report generated successfully: {filename}"
            
        except Exception as e:
            return False, "", f"Failed to generate report: {str(e)}"
    
    def _generate_markdown_report(self) -> str:
        """Generate comprehensive markdown report"""
        sections = []
        
        # Header
        sections.append(self._generate_header())
        
        # Executive Summary
        sections.append(self._generate_executive_summary())
        
        # Risk Assessment
        sections.append(self._generate_risk_assessment())
        
        # Findings by Category
        sections.append(self._generate_findings_by_category())
        
        # Detailed Findings
        sections.append(self._generate_detailed_findings())
        
        # Recommendations
        sections.append(self._generate_recommendations())
        
        # Appendix
        sections.append(self._generate_appendix())
        
        return "\n\n".join(sections)
    
    def _generate_header(self) -> str:
        """Generate report header with metadata"""
        risk_level = self._get_risk_level(self.report.risk_score)
        
        return f"""# 🛡️ Wolfkit Security Analysis Report

**Generated:** {self.report.scan_date.strftime("%Y-%m-%d %H:%M:%S")}  
**Codebase:** `{os.path.basename(self.report.codebase_path)}`  
**Framework:** {self.report.framework_detected or 'Not detected'}  
**Database:** {self.report.database_type or 'Not detected'}  
**Files Scanned:** {self.report.total_files_scanned}  

---

## 🚨 Security Status: **{risk_level}** (Score: {self.report.risk_score}/100)

| Severity | Count |
|----------|--------|
| 🔴 **Critical** | {self.report.summary_stats.get('CRITICAL', 0)} |
| 🟠 **High** | {self.report.summary_stats.get('HIGH', 0)} |
| 🟡 **Medium** | {self.report.summary_stats.get('MEDIUM', 0)} |
| 🔵 **Low** | {self.report.summary_stats.get('LOW', 0)} |
| ℹ️ **Info** | {self.report.summary_stats.get('INFO', 0)} |
| **Total** | {self.report.summary_stats.get('total', 0)} |"""
    
    def _generate_executive_summary(self) -> str:
        """Generate executive summary for management"""
        critical_count = self.report.summary_stats.get('CRITICAL', 0)
        high_count = self.report.summary_stats.get('HIGH', 0)
        total_count = self.report.summary_stats.get('total', 0)
        
        risk_level = self._get_risk_level(self.report.risk_score)
        
        # Get top categories
        category_counts = self._get_category_breakdown()
        top_categories = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        
        summary = f"""## 📋 Executive Summary

### Overall Assessment
The security analysis of `{os.path.basename(self.report.codebase_path)}` reveals a **{risk_level}** risk level with {total_count} total security findings across {self.report.total_files_scanned} files.

### Key Metrics
- **Critical Issues:** {critical_count} (require immediate attention)
- **High-Priority Issues:** {high_count} (should be addressed soon)
- **Framework Detected:** {self.report.framework_detected or 'Generic codebase'}
- **Primary Concerns:** {', '.join([cat for cat, _ in top_categories[:2]]) if top_categories else 'None identified'}

### Immediate Actions Required
"""
        
        if critical_count > 0:
            summary += f"- 🚨 **{critical_count} CRITICAL** issues need immediate remediation\n"
        if high_count > 0:
            summary += f"- ⚠️ **{high_count} HIGH** priority issues should be addressed within 1-2 weeks\n"
        
        if critical_count == 0 and high_count == 0:
            summary += "- ✅ No critical or high-priority issues identified\n"
        
        summary += f"""
### Business Impact
- **Security Risk:** {self._get_risk_description(risk_level)}
- **Compliance:** Review findings against regulatory requirements
- **Development:** Integrate security practices into development workflow"""
        
        return summary
    
    def _generate_risk_assessment(self) -> str:
        """Generate detailed risk assessment"""
        risk_level = self._get_risk_level(self.report.risk_score)
        category_breakdown = self._get_category_breakdown()
        
        assessment = f"""## 🎯 Risk Assessment

### Overall Risk Score: {self.report.risk_score}/100 ({risk_level})

{self._get_risk_description(risk_level)}

### Risk Breakdown by Category

| Category | Issues | Risk Contribution |
|----------|--------|-------------------|"""
        
        for category, count in sorted(category_breakdown.items(), key=lambda x: x[1], reverse=True):
            risk_contrib = self._calculate_category_risk(category)
            assessment += f"\n| {category} | {count} | {risk_contrib:.1f}% |"
        
        assessment += f"""

### Confidence Levels
- **High Confidence:** {self._count_by_confidence('HIGH')} findings (likely true positives)
- **Medium Confidence:** {self._count_by_confidence('MEDIUM')} findings (review recommended)
- **Low Confidence:** {self._count_by_confidence('LOW')} findings (may be false positives)"""
        
        return assessment
    
    def _generate_findings_by_category(self) -> str:
        """Generate findings grouped by OWASP category"""
        category_groups = defaultdict(list)
        
        for finding in self.report.findings:
            category_groups[finding.category].append(finding)
        
        if not category_groups:
            return "## 📊 Findings by Category\n\nNo security findings identified."
        
        section = "## 📊 Findings by Category\n"
        
        for category, findings in sorted(category_groups.items(), key=lambda x: len(x[1]), reverse=True):
            section += f"\n### {category} ({len(findings)} issues)\n"
            
            # Count by severity within category
            severity_counts = Counter(f.severity for f in findings)
            severity_list = []
            for severity in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'INFO']:
                count = severity_counts.get(severity, 0)
                if count > 0:
                    severity_list.append(f"{severity}: {count}")
            
            section += f"**Severity Distribution:** {', '.join(severity_list)}\n\n"
            
            # Show top issues in this category
            high_severity_findings = [f for f in findings if f.severity in ['CRITICAL', 'HIGH']]
            if high_severity_findings:
                section += "**Key Issues:**\n"
                for finding in high_severity_findings[:3]:  # Show top 3
                    section += f"- `{finding.file_path}`: {finding.issue}\n"
            section += "\n"
        
        return section
    
    def _generate_detailed_findings(self) -> str:
        """Generate detailed findings section"""
        if not self.report.findings:
            return "## 📝 Detailed Findings\n\nNo security findings to report."
        
        section = "## 📝 Detailed Findings\n"
        
        # Group by severity
        severity_groups = defaultdict(list)
        for finding in self.report.findings:
            severity_groups[finding.severity].append(finding)
        
        # Process in order of severity
        for severity in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'INFO']:
            findings = severity_groups.get(severity, [])
            if not findings:
                continue
            
            section += f"\n### {severity} Priority Issues ({len(findings)})\n"
            
            for i, finding in enumerate(findings, 1):
                section += f"\n#### {severity}-{i:02d}: {finding.issue}\n"
                section += f"**File:** `{finding.file_path}`"
                if finding.line_number:
                    section += f" (Line {finding.line_number})"
                section += "\n"
                section += f"**Category:** {finding.category}\n"
                section += f"**Confidence:** {finding.confidence}\n"
                if finding.cwe_id:
                    section += f"**CWE:** [{finding.cwe_id}](https://cwe.mitre.org/data/definitions/{finding.cwe_id.replace('CWE-', '')}.html)\n"
                
                if finding.code_snippet:
                    section += f"\n**Code:**\n```\n{finding.code_snippet}\n```\n"
                
                section += f"\n**Recommendation:** {finding.recommendation}\n"
                section += "\n---\n"
        
        return section
    
    def _generate_recommendations(self) -> str:
        """Generate actionable recommendations"""
        recommendations = f"""## 🔧 Recommendations

### Immediate Actions (Next 7 Days)
"""
        
        critical_findings = [f for f in self.report.findings if f.severity == 'CRITICAL']
        if critical_findings:
            recommendations += f"1. **Address {len(critical_findings)} critical security issues:**\n"
            for finding in critical_findings[:5]:  # Top 5
                recommendations += f"   - {finding.file_path}: {finding.issue}\n"
            if len(critical_findings) > 5:
                recommendations += f"   - ... and {len(critical_findings) - 5} more\n"
        else:
            recommendations += "1. ✅ No critical issues identified\n"
        
        recommendations += f"""
### Short-term Actions (Next 30 Days)
"""
        
        high_findings = [f for f in self.report.findings if f.severity == 'HIGH']
        if high_findings:
            recommendations += f"1. **Resolve {len(high_findings)} high-priority issues**\n"
            recommendations += "2. **Implement security testing in CI/CD pipeline**\n"
            recommendations += "3. **Conduct security code review training**\n"
        else:
            recommendations += "1. ✅ No high-priority issues identified\n"
        
        recommendations += f"""
### Long-term Strategy
1. **Security-First Development:**
   - Integrate security analysis into development workflow
   - Implement secure coding standards
   - Regular security training for development team

2. **Automated Security:**
   - Set up automated security scanning
   - Implement dependency vulnerability checking
   - Configure security monitoring and alerting

3. **Framework-Specific Recommendations:**"""
        
        if self.report.framework_detected == "fastapi":
            recommendations += """
   - Implement rate limiting with slowapi
   - Configure proper CORS policies
   - Use dependency injection for authentication
   - Enable API documentation security"""
        elif self.report.framework_detected == "flask":
            recommendations += """
   - Configure strong SECRET_KEY
   - Implement CSRF protection
   - Use Flask-Security for authentication
   - Enable secure session configuration"""
        else:
            recommendations += """
   - Follow OWASP guidelines for your framework
   - Implement framework-specific security middleware
   - Regular security updates and patches"""
        
        return recommendations
    
    def _generate_appendix(self) -> str:
        """Generate technical appendix"""
        return f"""## 📚 Appendix

### Analysis Methodology
This report was generated using Wolfkit's security analysis engine, which employs:
- **Static Code Analysis:** Pattern-based vulnerability detection
- **Framework Detection:** Automatic identification of web frameworks and databases
- **OWASP Alignment:** Findings categorized according to OWASP Top 10
- **Risk Scoring:** Weighted scoring based on severity, category, and confidence

### Report Metadata
- **Analysis Duration:** Full static analysis
- **Pattern Database:** {datetime.now().year} security patterns
- **False Positive Rate:** Estimated 5-15% (review low-confidence findings)
- **Coverage:** Source code, configuration files, dependencies

### Resources
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CWE Database](https://cwe.mitre.org/)
- [Wolfkit Documentation](https://github.com/your-repo/wolfkit)

### Next Steps
1. **Prioritize** critical and high-severity findings
2. **Validate** medium and low-confidence findings
3. **Implement** recommended security measures
4. **Re-scan** after remediation to track progress
5. **Schedule** regular security analysis

---
*Report generated by Wolfkit Security Analysis v1.3.1*  
*For questions or support, please refer to the Wolfkit documentation.*"""
    
    def _generate_html_report(self) -> str:
        """Generate HTML version of the report"""
        markdown_content = self._generate_markdown_report()
        
        # Basic HTML wrapper (could be enhanced with CSS)
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Wolfkit Security Analysis Report</title>
    <meta charset="utf-8">
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif; margin: 40px; }}
        h1, h2, h3 {{ color: #2c3e50; }}
        .critical {{ color: #e74c3c; }}
        .high {{ color: #f39c12; }}
        .medium {{ color: #f1c40f; }}
        .low {{ color: #3498db; }}
        code {{ background: #f8f9fa; padding: 2px 4px; border-radius: 3px; }}
        pre {{ background: #f8f9fa; padding: 15px; border-radius: 5px; overflow-x: auto; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
    </style>
</head>
<body>
{self._markdown_to_basic_html(markdown_content)}
</body>
</html>"""
        return html
    
    def _get_risk_level(self, score: int) -> str:
        """Convert risk score to human-readable level"""
        if score >= 70:
            return "CRITICAL"
        elif score >= 50:
            return "HIGH"
        elif score >= 30:
            return "MEDIUM"
        else:
            return "LOW"
    
    def _get_risk_description(self, risk_level: str) -> str:
        """Get detailed risk description"""
        descriptions = {
            "CRITICAL": "🚨 **Immediate action required.** Critical vulnerabilities pose severe security risks and should be addressed within 24-48 hours.",
            "HIGH": "⚠️ **High priority remediation needed.** Significant security issues that should be resolved within 1-2 weeks.",
            "MEDIUM": "🔍 **Moderate risk identified.** Security concerns that should be addressed in the next sprint or release cycle.",
            "LOW": "✅ **Low risk profile.** Minor security considerations or best practice improvements recommended."
        }
        return descriptions.get(risk_level, "Risk level assessment unavailable.")
    
    def _get_category_breakdown(self) -> Dict[str, int]:
        """Get count of findings by category"""
        category_counts = defaultdict(int)
        for finding in self.report.findings:
            category_counts[finding.category] += 1
        return dict(category_counts)
    
    def _calculate_category_risk(self, category: str) -> float:
        """Calculate risk contribution percentage for a category"""
        if not self.report.findings:
            return 0.0
        
        category_findings = [f for f in self.report.findings if f.category == category]
        if not category_findings:
            return 0.0
        
        severity_weights = {"CRITICAL": 25, "HIGH": 15, "MEDIUM": 8, "LOW": 3, "INFO": 1}
        
        category_score = sum(severity_weights.get(f.severity, 1) for f in category_findings)
        total_score = sum(severity_weights.get(f.severity, 1) for f in self.report.findings)
        
        return (category_score / total_score * 100) if total_score > 0 else 0.0
    
    def _count_by_confidence(self, confidence_level: str) -> int:
        """Count findings by confidence level"""
        return len([f for f in self.report.findings if f.confidence == confidence_level])


def generate_executive_summary(report: SecurityReport) -> str:
    """
    Generate standalone executive summary
    
    Args:
        report: SecurityReport to summarize
        
    Returns:
        Executive summary as string
    """
    reporter = SecurityReporter(report)
    return reporter._generate_executive_summary()


def generate_technical_report(report: SecurityReport) -> str:
    """
    Generate technical markdown report
    
    Args:
        report: SecurityReport to format
        
    Returns:
        Technical report as markdown string
    """
    reporter = SecurityReporter(report)
    return reporter._generate_markdown_report()


def calculate_risk_score(findings: List[SecurityFinding]) -> int:
    """
    Calculate risk score from findings list
    
    Args:
        findings: List of security findings
        
    Returns:
        Risk score from 0-100
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
    for finding in findings:
        base_score = severity_weights.get(finding.severity, 1)
        multiplier = category_multipliers.get(finding.category, 1.0)
        confidence_factor = {"HIGH": 1.0, "MEDIUM": 0.7, "LOW": 0.4}.get(finding.confidence, 0.5)
        
        total_score += base_score * multiplier * confidence_factor
    
    # Normalize to 0-100 scale with diminishing returns
    normalized_score = min(100, int(total_score * 0.8))
    return normalized_score
    
    def _generate_json_report(self) -> str:
        """Generate JSON version of the report"""
        import json
        
        # Convert dataclasses to dict for JSON serialization
        report_dict = asdict(self.report)
        
        # Handle datetime serialization
        report_dict['scan_date'] = self.report.scan_date.isoformat()
        
        return json.dumps(report_dict, indent=2, ensure_ascii=False)
    
    def _markdown_to_basic_html(self, markdown: str) -> str:
        """Basic markdown to HTML conversion"""
        html = markdown
        
        # Headers
        html = html.replace('### ', '<h3>').replace('\n', '</h3>\n', 1) if '### ' in html else html
        html = html.replace('## ', '<h2>').replace('\n', '</h2>\n', 1) if '## ' in html else html  
        html = html.replace('# ', '<h1>').replace('\n', '</h1>\n', 1) if '# ' in html else html
        
        # Code blocks
        lines = html.split('\n')
        in_code_block = False
        result_lines = []
        
        for line in lines:
            if line.strip() == '```':
                if in_code_block:
                    result_lines.append('</pre>')
                    in_code_block = False
                else:
                    result_lines.append('<pre>')
                    in_code_block = True
            else:
                result_lines.append(line)
        
        html = '\n'.join(result_lines)
        
        # Convert newlines to <br> outside of code blocks
        html = html.replace('\n', '<br>\n')
        
        return html