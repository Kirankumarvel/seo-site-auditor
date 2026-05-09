# Quick Start Guide

Get up and running with SEO Auditor in 5 minutes! 🚀

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/seo-auditor.git
cd seo-auditor
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Install the Package

```bash
pip install -e .
```

## First Audit

### Using the CLI

Audit your first website:

```bash
seo-auditor audit https://example.com
```

This will:
- Crawl up to 50 pages (default)
- Detect SEO issues
- Generate reports in `audit_reports/`

### Custom Settings

```bash
seo-auditor audit https://example.com \
  --max-pages 100 \
  --timeout 15 \
  --output json html text \
  --output-dir ./my_reports
```

### Options

- `--max-pages N`: Crawl up to N pages (default: 50)
- `--timeout S`: Request timeout in seconds (default: 10)
- `--output FORMAT`: Output formats - json, html, text (default: text)
- `--output-dir PATH`: Where to save reports (default: audit_reports)

## Using in Python

### Basic Usage

```python
from seo_auditor import SEOAuditor, AuditReport

# Create auditor
auditor = SEOAuditor("https://example.com", max_pages=50)

# Run audit
results = auditor.crawl()

# Get summary
summary = auditor.get_summary()
print(f"Issues found: {summary['total_issues_found']}")

# Generate reports
report = AuditReport(results)
report.to_html("report.html")
```

### Access Specific Issues

```python
issues = results['issues']

# Get pages missing meta titles
missing_titles = issues['missing_meta_titles']
print(f"Missing titles: {len(missing_titles)} pages")

# Get pages missing H1 tags
missing_h1 = issues['missing_h1_tags']
print(f"Missing H1: {len(missing_h1)} pages")
```

## Output Examples

### CLI Output

```
🔍 Starting SEO Site Audit...

Target: https://example.com
Max Pages: 50
Timeout: 10s

============================================================
AUDIT COMPLETE
============================================================
✅ Audited 45 pages
⚠️  Found 127 issues

📊 Generating reports...

✨ All reports generated successfully!
📁 Reports saved to: audit_reports/
```

### Generated Reports

Three report formats are created:

1. **report.html** - Beautiful visual dashboard
2. **report.json** - Machine-readable data
3. **report.txt** - Plain text summary

## Common Tasks

### Audit Multiple Sites

```python
sites = ["https://site1.com", "https://site2.com"]

for site in sites:
    auditor = SEOAuditor(site)
    results = auditor.crawl()
    report = AuditReport(results)
    
    # Save with site name
    domain = site.replace("https://", "").replace("/", "")
    report.to_html(f"{domain}_report.html")
```

### Get Critical Issues Only

```python
auditor = SEOAuditor("https://example.com")
results = auditor.crawl()

critical = {
    'missing_meta_titles': results['issues'].get('missing_meta_titles', []),
    'missing_h1_tags': results['issues'].get('missing_h1_tags', []),
    'missing_schema': results['issues'].get('missing_schema_markup', []),
}

for issue_type, pages in critical.items():
    print(f"{issue_type}: {len(pages)} pages")
```

### Export Issues to CSV

```python
import csv
from seo_auditor import SEOAuditor

auditor = SEOAuditor("https://example.com")
results = auditor.crawl()

with open('issues.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['URL', 'Issue Type', 'Details'])
    
    for issue_type, pages in results['issues'].items():
        for item in pages:
            url = item if isinstance(item, str) else item.get('url')
            details = '' if isinstance(item, str) else item.get('issue')
            writer.writerow([url, issue_type, details])
```

## Troubleshooting

### SSL Certificate Errors

```python
import requests
from urllib3.exceptions import InsecureRequestWarning

# Disable warning (not recommended for production)
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

auditor = SEOAuditor("https://example.com")
auditor.session.verify = False
results = auditor.crawl()
```

### Timeout Issues

Increase the timeout:

```bash
seo-auditor audit https://example.com --timeout 30
```

Or in code:

```python
auditor = SEOAuditor("https://example.com", timeout=30)
```

### Large Sites (100+ pages)

For large sites, increase max_pages:

```bash
seo-auditor audit https://example.com --max-pages 500
```

Note: This will take longer and use more resources.

## Next Steps

1. **Read the README** for comprehensive documentation
2. **Check example.py** for more code examples
3. **Explore the CLI help**:
   ```bash
   seo-auditor --help
   seo-auditor audit --help
   ```
4. **Run tests**:
   ```bash
   pytest tests/ -v
   ```
5. **Contribute** - We welcome pull requests!

## Need Help?

- 📖 Check the [README.md](README.md)
- 💬 Open an issue on GitHub
- 🤝 Join discussions
- 📧 Contact the maintainer

## What's Detected?

✅ **Meta Tags**
- Missing/short/long meta titles
- Missing/short/long meta descriptions

✅ **Headings**
- Missing H1 tags
- Multiple H1 tags
- Empty/long H1 content

✅ **Images**
- Missing alt attributes

✅ **Technical**
- Missing canonical tags
- Missing Open Graph tags
- Missing schema markup
- Missing mobile viewport

✅ **Performance**
- Broken links
- Error status codes

## Tips for Best Results

1. **Start small**: Test with 10-20 pages first
2. **Use reasonable timeouts**: 10-15 seconds is typical
3. **Respect server resources**: Default 0.5s delay between requests
4. **Check reports carefully**: Review HTML report for detailed insights
5. **Fix critical issues first**: Meta tags, H1, descriptions

---

**Ready to audit? Let's go!** 🚀

```bash
seo-auditor audit https://yoursite.com
```
