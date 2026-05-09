"""
Report Generation Module
Generates audit reports in JSON, HTML, and text formats
"""

import json
from datetime import datetime
from typing import Dict, Any
import os


class AuditReport:
    """Generate and export audit reports"""

    def __init__(self, audit_results: Dict[str, Any]):
        """
        Initialize report generator

        Args:
            audit_results: Dictionary with audit results from SEOAuditor.crawl()
        """
        self.results = audit_results
        self.timestamp = datetime.now()

    def to_json(self, filepath: str = None) -> str:
        """
        Export report as JSON

        Args:
            filepath: Optional path to save JSON file

        Returns:
            JSON string
        """
        report = {
            "audit_timestamp": self.timestamp.isoformat(),
            "audited_pages": self.results.get("audited_pages"),
            "issues": self.results.get("issues", {}),
            "summary": self._generate_summary(),
        }

        json_str = json.dumps(report, indent=2)

        if filepath:
            os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(json_str)
            print(f"JSON report saved to {filepath}")

        return json_str

    def to_html(self, filepath: str = None) -> str:
        """
        Export report as HTML

        Args:
            filepath: Optional path to save HTML file

        Returns:
            HTML string
        """
        issues = self.results.get("issues", {})
        summary = self._generate_summary()

        # Generate issue rows
        issue_rows = ""
        priority_levels = self._categorize_severity()

        for category, priority in priority_levels.items():
            issue_data = issues.get(category, [])
            if not issue_data:
                continue

            count = (
                len(issue_data) if isinstance(issue_data, (list, set)) else 1
            )
            icon = "🔴" if priority == "critical" else "🟡" if priority == "warning" else "🟢"

            issue_rows += f"""
            <tr class="issue-{priority}">
                <td class="category">{category.replace('_', ' ').title()}</td>
                <td class="count">{count}</td>
                <td class="severity">{icon} {priority.upper()}</td>
            </tr>
            """

        html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>SEO Audit Report</title>
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
            <style>
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }}
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    padding: 40px 20px;
                }}
                .container {{
                    max-width: 1000px;
                    margin: 0 auto;
                    background: white;
                    border-radius: 10px;
                    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
                    overflow: hidden;
                }}
                header {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 40px 30px;
                    text-align: center;
                }}
                header h1 {{
                    font-size: 2.5em;
                    margin-bottom: 10px;
                }}
                header p {{
                    font-size: 1.1em;
                    opacity: 0.9;
                }}
                .summary {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 20px;
                    padding: 30px;
                    border-bottom: 1px solid #e0e0e0;
                }}
                .summary-card {{
                    text-align: center;
                    padding: 20px;
                    border-radius: 8px;
                    background: #f5f5f5;
                }}
                .summary-card h3 {{
                    color: #667eea;
                    font-size: 2em;
                    margin-bottom: 5px;
                }}
                .summary-card p {{
                    color: #666;
                    font-size: 0.95em;
                }}
                .issues-section {{
                    padding: 30px;
                }}
                .issues-section h2 {{
                    color: #333;
                    margin-bottom: 20px;
                    font-size: 1.5em;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-bottom: 30px;
                }}
                th {{
                    background: #f5f5f5;
                    padding: 12px;
                    text-align: left;
                    font-weight: 600;
                    color: #333;
                    border-bottom: 2px solid #ddd;
                }}
                td {{
                    padding: 12px;
                    border-bottom: 1px solid #eee;
                }}
                tr:hover {{
                    background: #f9f9f9;
                }}
                .issue-critical {{
                    background: #fff3f3;
                }}
                .issue-warning {{
                    background: #fffbf3;
                }}
                .issue-info {{
                    background: #f3fbff;
                }}
                .category {{
                    font-weight: 500;
                    color: #333;
                }}
                .count {{
                    color: #667eea;
                    font-weight: 600;
                }}
                .severity {{
                    font-size: 0.9em;
                    font-weight: 500;
                }}
                footer {{
                    background: #f5f5f5;
                    padding: 20px 30px;
                    text-align: center;
                    color: #999;
                    font-size: 0.9em;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <header>
                    <h1>🔍 SEO Audit Report</h1>
                    <p>Comprehensive website SEO analysis</p>
                </header>

                <div class="summary">
                    <div class="summary-card">
                        <h3>{summary['total_pages']}</h3>
                        <p>Pages Audited</p>
                    </div>
                    <div class="summary-card">
                        <h3>{summary['total_issues']}</h3>
                        <p>Total Issues Found</p>
                    </div>
                    <div class="summary-card">
                        <h3>{summary['critical_issues']}</h3>
                        <p>Critical Issues</p>
                    </div>
                </div>

                <div class="issues-section">
                    <h2>Issues by Category</h2>
                    <table>
                        <thead>
                            <tr>
                                <th>Issue Category</th>
                                <th>Count</th>
                                <th>Severity</th>
                            </tr>
                        </thead>
                        <tbody>
                            {issue_rows}
                        </tbody>
                    </table>
                </div>

                <footer>
                    <p>Generated on {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}</p>
                    <p>Automated SEO Site Auditor</p>
                </footer>
            </div>
        </body>
        </html>
        """

        if filepath:
            os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(html)
            print(f"HTML report saved to {filepath}")

        return html

    def to_text(self, filepath: str = None) -> str:
        """
        Export report as plain text

        Args:
            filepath: Optional path to save text file

        Returns:
            Text string
        """
        issues = self.results.get("issues", {})
        summary = self._generate_summary()
        priority_levels = self._categorize_severity()

        text = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                         SEO AUDIT REPORT                                     ║
╚══════════════════════════════════════════════════════════════════════════════╝

Audit Timestamp: {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Total Pages Audited:    {summary['total_pages']}
Total Issues Found:     {summary['total_issues']}
Critical Issues:        {summary['critical_issues']}
Warning Issues:         {summary['warning_issues']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ISSUES BY CATEGORY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""

        for category, priority in priority_levels.items():
            issue_data = issues.get(category, [])
            if not issue_data:
                continue

            count = (
                len(issue_data) if isinstance(issue_data, (list, set)) else 1
            )
            icon = "🔴" if priority == "critical" else "🟡" if priority == "warning" else "🟢"

            text += f"\n{icon} {category.replace('_', ' ').upper()} [{count}]\n"
            text += f"   Severity: {priority.upper()}\n"

            # Show first 5 affected URLs
            if isinstance(issue_data, list) and issue_data:
                text += "   Affected pages (first 5):\n"
                for item in issue_data[:5]:
                    if isinstance(item, dict):
                        text += f"   - {item.get('url', str(item))}\n"
                    else:
                        text += f"   - {item}\n"
                if len(issue_data) > 5:
                    text += f"   ... and {len(issue_data) - 5} more\n"

        text += f"\n{'━' * 80}\n"
        text += f"\n✅ Report generated on {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n"
        text += f"Automated SEO Site Auditor v1.0.0\n\n"

        if filepath:
            os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(text)
            print(f"Text report saved to {filepath}")

        return text

    def _generate_summary(self) -> Dict[str, int]:
        """Generate summary statistics"""
        issues = self.results.get("issues", {})
        priority_levels = self._categorize_severity()

        critical = sum(
            len(issues.get(cat, []))
            for cat, priority in priority_levels.items()
            if priority == "critical"
        )
        warning = sum(
            len(issues.get(cat, []))
            for cat, priority in priority_levels.items()
            if priority == "warning"
        )

        return {
            "total_pages": self.results.get("audited_pages", 0),
            "total_issues": sum(
                len(v) if isinstance(v, (list, set)) else 1
                for v in issues.values()
            ),
            "critical_issues": critical,
            "warning_issues": warning,
        }

    def _categorize_severity(self) -> Dict[str, str]:
        """Categorize issues by severity"""
        return {
            # Critical
            "missing_meta_titles": "critical",
            "missing_h1_tags": "critical",
            "missing_meta_descriptions": "critical",
            "missing_canonical_tags": "critical",
            "missing_schema_markup": "critical",
            # Warning
            "short_meta_titles": "warning",
            "long_meta_titles": "warning",
            "short_meta_descriptions": "warning",
            "long_meta_descriptions": "warning",
            "multiple_h1_tags": "warning",
            "long_h1_tags": "warning",
            "missing_image_alts": "warning",
            "missing_og_tags": "warning",
            "missing_mobile_viewport": "warning",
            # Info
            "broken_links": "info",
            "empty_h1_tags": "info",
            "slow_or_error_pages": "info",
        }
