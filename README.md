<!-- markdownlint-disable MD033 -->
<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue?logo=python" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green" alt="License">
  <img src="https://img.shields.io/badge/PRs-welcome-brightgreen" alt="PRs Welcome">
  <img src="https://img.shields.io/badge/SEO-Automation-red" alt="SEO Automation">
</p>

<h1 align="center">🔍 SEO Site Auditor</h1>
<p align="center">
  <strong>Automated, comprehensive SEO auditing – for developers and SEO professionals.</strong><br>
  Crawl any website, detect common SEO issues, and generate beautiful reports in JSON, HTML, or plain text.
</p>

<br>

## 📖 Table of Contents

- [✨ Features](#-features)
- [🚀 Quick Start](#-quick-start)
- [📦 Installation](#-installation)
- [💻 Usage](#-usage)
  - [Command Line](#command-line)
  - [Programmatic (Python)](#programmatic-python)
- [⚙️ Configuration](#️-configuration)
- [📊 Output Examples](#-output-examples)
- [🔬 Issue Severity Levels](#-issue-severity-levels)
- [🧠 How It Works](#-how-it-works)
- [📈 Performance & Limitations](#-performance--limitations)
- [🛣️ Roadmap](#️-roadmap)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)
- [🙏 Acknowledgements](#-acknowledgements)

---

## ✨ Features

### SEO Issue Detection – What We Check

| Category | Issues Detected |
|----------|----------------|
| **Meta Tags**             | Missing titles, title length (30‑60 chars), missing descriptions, description length (120‑160 chars) |
| **Heading Tags**          | Missing H1, multiple H1s, empty H1, H1 length |
| **Images & Media**        | Missing `alt` attributes, image optimisation hints |
| **Technical SEO**         | Missing canonical tags, missing Open Graph tags, missing JSON‑LD schema, missing mobile viewport |
| **Performance & Accessibility** | Broken internal links, HTTP error status codes, mobile responsiveness checks |

### Output Formats

- 📊 **JSON** – Machine‑readable, perfect for CI/CD pipelines  
- 📄 **HTML** – Interactive, styled report (great for sharing with clients)  
- 📝 **Text** – Plain‑text summary for quick terminal viewing  

---

## 🚀 Quick Start

```bash
# 1. Install (from source)
git clone https://github.com/Kirankumarvel/seo-site-auditor.git
cd seo-site-auditor
pip install -r requirements.txt

# 2. Run your first audit
seo-auditor audit https://example.com

# 3. Generate all report types
seo-auditor audit https://example.com --output json html text --output-dir ./reports
```

> **Try it now** – replace `https://example.com` with your own website.

---

## 📦 Installation

### From Source (Recommended for development)

```bash
git clone https://github.com/Kirankumarvel/seo-site-auditor.git
cd seo-site-auditor
python -m venv venv               # Create virtual environment
source venv/bin/activate          # (Windows: venv\Scripts\activate)
pip install -r requirements.txt
pip install -e .                  # Install as editable package
```

### From PyPI (once published)

```bash
pip install seo-site-auditor
```

### Dependencies

- Python 3.8+
- `requests`, `beautifulsoup4`, `click`, `lxml`

---

## 💻 Usage

### Command Line

```bash
# Basic audit
seo-auditor audit https://example.com

# Custom limits & timeouts
seo-auditor audit https://example.com --max-pages 200 --timeout 15

# Multiple output formats
seo-auditor audit https://example.com --output json html text --output-dir my_reports

# Show version
seo-auditor version
```

### Programmatic (Python)

```python
from seo_auditor import SEOAuditor, AuditReport

# Configure the crawler
auditor = SEOAuditor(
    base_url="https://example.com",
    max_pages=100,
    timeout=10
)

# Run the audit
results = auditor.crawl()

# Get a quick summary
summary = auditor.get_summary()
print(f"Pages audited: {summary['total_pages_audited']}")
print(f"Issues found: {summary['total_issues_found']}")

# Generate all reports
report = AuditReport(results)
report.to_json("report.json")
report.to_html("report.html")
report.to_text("report.txt")
```

> See [`example.py`](example.py) for more advanced usage (multiple sites, severity filtering, etc.).

---

## ⚙️ Configuration

### Environment Variables

```bash
export SEO_AUDITOR_MAX_PAGES=200
export SEO_AUDITOR_TIMEOUT=20
```

### Custom Headers / Session

```python
auditor = SEOAuditor("https://example.com")
auditor.session.headers.update({
    "Authorization": "Bearer YOUR_TOKEN",
    "X-Custom-Header": "value"
})
```

---

## 📊 Output Examples

### Console Output

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

📊 Reports saved to: audit_reports/
```

### HTML Report Preview

- Interactive dashboard with issue counts, severity badges, and per‑page details.  
- Fully responsive – works on desktop and mobile.  
- Dark/light theme adaptable (CSS included).

### JSON Report Structure (excerpt)

```json
{
  "audit_timestamp": "2025-02-03T14:22:10.123456",
  "audited_pages": 45,
  "issues": {
    "missing_meta_titles": ["https://example.com/page1", ...],
    "missing_h1_tags": ["https://example.com/page2", ...],
    "missing_image_alts": [
      {"url": "https://example.com/page3", "issue": "Found 3 images without alt text"}
    ]
  },
  "summary": {
    "total_pages": 45,
    "total_issues": 127,
    "critical_issues": 45,
    "warning_issues": 82
  }
}
```

---

## 🔬 Issue Severity Levels

| Severity | Examples |
|----------|----------|
| 🔴 **Critical** | Missing meta title / H1 / meta description / canonical / schema markup |
| 🟡 **Warning** | Title/description length issues, multiple H1s, missing `alt` attributes, missing OG tags, no viewport |
| 🟢 **Info** | Broken internal links, error status codes, empty H1 content |

---

## 🧠 How It Works

1. **Crawl** – Starts from the `base_url`, discovers internal links (same domain only).  
2. **Fetch** – Retrieves each page’s HTML and status code (respects `robots.txt` by following standard rules).  
3. **Parse** – Uses BeautifulSoup to extract meta tags, headings, images, links, and schema markup.  
4. **Validate** – Compares extracted data against SEO best practices (length rules, existence checks).  
5. **Report** – Aggregates all issues and generates the requested output formats.

```text
[Start] → [Queue seed URL] → [Fetch page] → [Parse HTML] → [Audit elements] → [Store issues]
                ↑                                                           ↓
                └─────────────── [Add new internal links] ←────────────────┘
                                                                             ↓
                                                              [Generate reports] → [JSON/HTML/TXT]
```

---

## 📈 Performance & Limitations

### Current Strengths

- **Lightweight** – No heavy browser automation (pure HTTP + parsing).  
- **Respectful crawling** – Built‑in 0.5s delay between requests.  
- **Memory‑efficient** – Works for sites up to several thousand pages (tested up to 2k pages).  

### Known Limitations

- ❌ **No JavaScript rendering** – single‑page apps (React/Vue) may not be fully audited.  
- ❌ **Single‑threaded** – slower on very large sites (async version planned).  
- ❌ **Basic performance metrics** – no Lighthouse or Core Web Vitals (coming in v2).  

---

## 🛣️ Roadmap

- [ ] **Async crawling** – faster audits with `asyncio` / `aiohttp`
- [ ] **JavaScript rendering** – optional Playwright integration
- [ ] **Lighthouse integration** – performance, accessibility, best practices
- [ ] **Core Web Vitals** – real user metrics (CrUX)
- [ ] **Sitemap & robots.txt analysis**
- [ ] **Historical tracking** – SQLite backend to monitor changes over time
- [ ] **Web dashboard** – visualise trends and export shareable links

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-idea`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-idea`)
5. Open a Pull Request

Please ensure your code passes the test suite:

```bash
pip install pytest pytest-cov
pytest tests/ --cov=seo_auditor
```

> See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines (to be added).

---

## 📄 License

Distributed under the **MIT License**. See `LICENSE` for more information.

---

## 🙏 Acknowledgements

- Built with `requests`, `beautifulsoup4`, `click` – huge thanks to their maintainers.
- Inspired by professional tools like Screaming Frog, Semrush, and Ahrefs.
- Created by **Kiran** (7+ years in SEO & digital marketing).

---

<p align="center">
  <b>Made with ❤️ for the SEO & developer community</b><br>
  <sub>⭐ Star this repo if you find it useful – it helps others discover it!</sub>
</p>
