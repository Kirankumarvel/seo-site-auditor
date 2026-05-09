#!/usr/bin/env python
"""
Example usage of SEO Auditor

This script demonstrates how to use the SEO Auditor
programmatically to audit a website and generate reports.
"""

from seo_auditor import SEOAuditor, AuditReport
import json


def main():
    # Target website URL
    website_url = "https://example.com"

    # Initialize auditor
    # Parameters:
    # - base_url: Website to audit
    # - max_pages: Maximum pages to crawl (default: 50)
    # - timeout: Request timeout in seconds (default: 10)
    auditor = SEOAuditor(
        base_url=website_url,
        max_pages=50,
        timeout=10
    )

    # Run the audit
    print("🔍 Starting SEO audit...")
    print(f"Target: {website_url}\n")

    results = auditor.crawl()

    # Get summary
    summary = auditor.get_summary()

    print("=" * 60)
    print("AUDIT SUMMARY")
    print("=" * 60)
    print(f"✅ Total pages audited: {summary['total_pages_audited']}")
    print(f"⚠️  Total issues found: {summary['total_issues_found']}\n")

    print("Issues by category:")
    for category, count in sorted(
        summary['issues_by_category'].items(),
        key=lambda x: x[1],
        reverse=True
    ):
        print(f"  • {category.replace('_', ' ').title()}: {count}")

    print("\n" + "=" * 60)

    # Generate reports in different formats
    report = AuditReport(results)

    # Save as JSON
    print("\n📊 Generating reports...\n")
    report.to_json("audit_reports/report.json")

    # Save as HTML
    report.to_html("audit_reports/report.html")

    # Save as Text
    report.to_text("audit_reports/report.txt")

    print("\n✨ Reports generated successfully!")
    print("📁 Check the 'audit_reports' directory for results")

    # Example: Access specific issue types
    print("\n" + "=" * 60)
    print("SPECIFIC ISSUES")
    print("=" * 60)

    issues = results['issues']

    if issues.get('missing_meta_titles'):
        print(f"\n🔴 Pages missing meta titles ({len(issues['missing_meta_titles'])}):")
        for url in issues['missing_meta_titles'][:3]:
            print(f"   - {url}")

    if issues.get('missing_h1_tags'):
        print(f"\n🔴 Pages missing H1 tags ({len(issues['missing_h1_tags'])}):")
        for url in issues['missing_h1_tags'][:3]:
            print(f"   - {url}")

    if issues.get('missing_meta_descriptions'):
        print(f"\n🔴 Pages missing meta descriptions ({len(issues['missing_meta_descriptions'])}):")
        for url in issues['missing_meta_descriptions'][:3]:
            print(f"   - {url}")

    if issues.get('missing_image_alts'):
        print(f"\n🟡 Pages with missing image alts ({len(issues['missing_image_alts'])}):")
        for item in issues['missing_image_alts'][:3]:
            if isinstance(item, dict):
                print(f"   - {item.get('url')}")
                print(f"     Issue: {item.get('issue')}")

    if issues.get('missing_schema_markup'):
        print(f"\n🟡 Pages without schema markup ({len(issues['missing_schema_markup'])}):")
        for url in issues['missing_schema_markup'][:3]:
            print(f"   - {url}")


if __name__ == "__main__":
    main()
