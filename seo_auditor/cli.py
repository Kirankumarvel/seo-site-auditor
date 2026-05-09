"""
Command-line interface for SEO Auditor
"""

import click
import sys
from .auditor import SEOAuditor
from .report import AuditReport


@click.group()
def cli():
    """Automated SEO Site Auditor CLI"""
    pass


@cli.command()
@click.argument("url")
@click.option(
    "--max-pages",
    default=50,
    help="Maximum number of pages to crawl",
    type=int,
)
@click.option(
    "--timeout",
    default=10,
    help="Request timeout in seconds",
    type=int,
)
@click.option(
    "--output",
    "-o",
    multiple=True,
    type=click.Choice(["json", "html", "text"]),
    default=["text"],
    help="Output format(s)",
)
@click.option(
    "--output-dir",
    "-d",
    default="audit_reports",
    help="Directory to save reports",
)
def audit(url: str, max_pages: int, timeout: int, output: tuple, output_dir: str):
    """
    Audit a website for SEO issues

    Example:
        seo-auditor audit https://example.com --max-pages 100 --output json html text
    """
    click.echo("🔍 Starting SEO Site Audit...\n")
    click.echo(f"Target: {url}")
    click.echo(f"Max Pages: {max_pages}")
    click.echo(f"Timeout: {timeout}s\n")

    try:
        # Run audit
        auditor = SEOAuditor(url, max_pages=max_pages, timeout=timeout)
        results = auditor.crawl()

        # Get summary
        summary = auditor.get_summary()
        click.echo("\n" + "=" * 60)
        click.echo("AUDIT COMPLETE")
        click.echo("=" * 60)
        click.echo(f"✅ Audited {summary['total_pages_audited']} pages")
        click.echo(
            f"⚠️  Found {summary['total_issues_found']} issues\n"
        )

        # Generate reports
        report = AuditReport(results)

        click.echo("📊 Generating reports...\n")

        if "json" in output:
            json_path = f"{output_dir}/audit_report.json"
            report.to_json(json_path)

        if "html" in output:
            html_path = f"{output_dir}/audit_report.html"
            report.to_html(html_path)

        if "text" in output:
            text_path = f"{output_dir}/audit_report.txt"
            report.to_text(text_path)

        click.echo("\n✨ All reports generated successfully!")
        click.echo(f"📁 Reports saved to: {output_dir}/")

    except Exception as e:
        click.echo(f"❌ Error: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
def version():
    """Show version"""
    from . import __version__

    click.echo(f"SEO Auditor v{__version__}")


if __name__ == "__main__":
    cli()
