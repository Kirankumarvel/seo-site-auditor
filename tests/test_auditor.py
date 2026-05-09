"""
Unit tests for SEO Auditor
"""

import pytest
from seo_auditor.auditor import SEOAuditor
from seo_auditor.report import AuditReport


class TestSEOAuditor:
    """Tests for SEOAuditor class"""

    def test_initialization(self):
        """Test auditor initialization"""
        auditor = SEOAuditor("https://example.com", max_pages=50, timeout=10)
        assert auditor.base_url == "https://example.com"
        assert auditor.max_pages == 50
        assert auditor.timeout == 10
        assert auditor.domain == "example.com"

    def test_is_same_domain(self):
        """Test domain matching"""
        auditor = SEOAuditor("https://example.com")

        # Same domain
        assert auditor.is_same_domain("https://example.com/page")
        assert auditor.is_same_domain("https://www.example.com/page")

        # Different domain
        assert not auditor.is_same_domain("https://other.com/page")
        
    def test_is_same_domain_with_www(self):
        """Test domain matching with www prefix"""
        auditor = SEOAuditor("https://www.example.com")

        # Should match both with and without www
        assert auditor.is_same_domain("https://example.com/page")
        assert auditor.is_same_domain("https://www.example.com/page")

        # Different domain
        assert not auditor.is_same_domain("https://other.com/page")

    def test_url_normalization(self):
        """Test URL normalization"""
        auditor1 = SEOAuditor("https://example.com/")
        auditor2 = SEOAuditor("https://example.com")

        assert auditor1.base_url == auditor2.base_url

    def test_audit_page_missing_title(self):
        """Test detection of missing meta title"""
        auditor = SEOAuditor("https://example.com")

        html = "<html><head></head><body></body></html>"
        issues = auditor.audit_page("https://example.com", html, 200)

        assert issues.get("missing_meta_title") is True

    def test_audit_page_with_title(self):
        """Test proper meta title"""
        auditor = SEOAuditor("https://example.com")

        html = "<html><head><title>My Page Title</title></head><body></body></html>"
        issues = auditor.audit_page("https://example.com", html, 200)

        assert "missing_meta_title" not in issues

    def test_audit_page_short_title(self):
        """Test detection of short meta title"""
        auditor = SEOAuditor("https://example.com")

        html = "<html><head><title>Short</title></head><body></body></html>"
        issues = auditor.audit_page("https://example.com", html, 200)

        assert "short_meta_title" in issues

    def test_audit_page_missing_h1(self):
        """Test detection of missing H1"""
        auditor = SEOAuditor("https://example.com")

        html = "<html><body><p>Content</p></body></html>"
        issues = auditor.audit_page("https://example.com", html, 200)

        assert issues.get("missing_h1") is True

    def test_audit_page_multiple_h1s(self):
        """Test detection of multiple H1s"""
        auditor = SEOAuditor("https://example.com")

        html = "<html><body><h1>Title 1</h1><h1>Title 2</h1></body></html>"
        issues = auditor.audit_page("https://example.com", html, 200)

        assert "multiple_h1s" in issues

    def test_audit_page_missing_description(self):
        """Test detection of missing meta description"""
        auditor = SEOAuditor("https://example.com")

        html = "<html><head></head><body></body></html>"
        issues = auditor.audit_page("https://example.com", html, 200)

        assert issues.get("missing_meta_description") is True

    def test_audit_page_missing_image_alts(self):
        """Test detection of missing image alt attributes"""
        auditor = SEOAuditor("https://example.com")

        html = '<html><body><img src="test.jpg"></body></html>'
        issues = auditor.audit_page("https://example.com", html, 200)

        assert "missing_image_alts" in issues

    def test_audit_page_with_image_alts(self):
        """Test page with proper image alt attributes"""
        auditor = SEOAuditor("https://example.com")

        html = '<html><body><img src="test.jpg" alt="Test Image"></body></html>'
        issues = auditor.audit_page("https://example.com", html, 200)

        assert "missing_image_alts" not in issues

    def test_audit_page_missing_canonical(self):
        """Test detection of missing canonical tag"""
        auditor = SEOAuditor("https://example.com")

        html = "<html><head></head><body></body></html>"
        issues = auditor.audit_page("https://example.com", html, 200)

        assert issues.get("missing_canonical") is True

    def test_audit_page_missing_schema(self):
        """Test detection of missing schema markup"""
        auditor = SEOAuditor("https://example.com")

        html = "<html><body><p>Content</p></body></html>"
        issues = auditor.audit_page("https://example.com", html, 200)

        assert "missing_schema_markup" in issues

    def test_extract_links(self):
        """Test link extraction"""
        auditor = SEOAuditor("https://example.com")

        html = """
        <html>
            <body>
                <a href="/page1">Link 1</a>
                <a href="https://example.com/page2">Link 2</a>
                <a href="https://other.com">External</a>
            </body>
        </html>
        """

        links = auditor.extract_links(html, "https://example.com/")

        # Should include internal links
        assert any("page1" in link for link in links)
        assert any("page2" in link for link in links)

        # Should exclude external links
        assert not any("other.com" in link for link in links)


class TestAuditReport:
    """Tests for AuditReport class"""

    def test_initialization(self):
        """Test report initialization"""
        audit_results = {
            "audited_pages": 10,
            "issues": {"missing_meta_titles": ["url1", "url2"]},
        }

        report = AuditReport(audit_results)
        assert report.results == audit_results

    def test_summary_generation(self):
        """Test summary generation"""
        audit_results = {
            "audited_pages": 10,
            "issues": {
                "missing_meta_titles": ["url1", "url2"],
                "missing_h1_tags": ["url3"],
            },
        }

        report = AuditReport(audit_results)
        summary = report._generate_summary()

        assert summary["total_pages"] == 10
        assert summary["total_issues"] == 3

    def test_severity_categorization(self):
        """Test issue severity categorization"""
        audit_results = {"audited_pages": 0, "issues": {}}
        report = AuditReport(audit_results)

        severity = report._categorize_severity()

        # Check critical issues
        assert severity["missing_meta_titles"] == "critical"
        assert severity["missing_h1_tags"] == "critical"

        # Check warning issues
        assert severity["short_meta_titles"] == "warning"
        assert severity["missing_image_alts"] == "warning"

    def test_json_export(self):
        """Test JSON export"""
        audit_results = {
            "audited_pages": 5,
            "issues": {"missing_meta_titles": ["url1"]},
        }

        report = AuditReport(audit_results)
        json_output = report.to_json()

        assert "audit_timestamp" in json_output
        assert "audited_pages" in json_output
        assert "missing_meta_titles" in json_output

    def test_html_export(self):
        """Test HTML export"""
        audit_results = {
            "audited_pages": 5,
            "issues": {"missing_meta_titles": ["url1"]},
        }

        report = AuditReport(audit_results)
        html_output = report.to_html()

        assert "<html" in html_output
        assert "SEO Audit Report" in html_output
        assert "Pages Audited" in html_output

    def test_text_export(self):
        """Test text export"""
        audit_results = {
            "audited_pages": 5,
            "issues": {"missing_meta_titles": ["url1"]},
        }

        report = AuditReport(audit_results)
        text_output = report.to_text()

        assert "SEO AUDIT REPORT" in text_output
        assert "Pages Audited" in text_output


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
