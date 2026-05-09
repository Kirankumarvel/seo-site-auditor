"""
Core SEO Auditor - Website crawling and SEO issue detection
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import defaultdict
from datetime import datetime
import logging
from typing import List, Dict, Set, Tuple, Optional
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SEOAuditor:
    """
    Automated SEO Site Auditor
    Crawls websites and detects SEO issues
    """

    def __init__(self, base_url: str, max_pages: int = 50, timeout: int = 10):
        """
        Initialize the SEO Auditor

        Args:
            base_url: Website URL to audit
            max_pages: Maximum pages to crawl
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip("/")
        self.max_pages = max_pages
        self.timeout = timeout
        self.visited_urls: Set[str] = set()
        self.issues = defaultdict(list)
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
        )
        self.domain = urlparse(self.base_url).netloc
        self.audit_timestamp = datetime.now()

    def is_same_domain(self, url: str) -> bool:
        """Check if URL belongs to same domain"""
        try:
            url_domain = urlparse(url).netloc
            # Normalize domains - remove www prefix for comparison
            base_domain = self.domain.replace("www.", "")
            url_domain_normalized = url_domain.replace("www.", "")
            return url_domain_normalized == base_domain
        except:
            return False

    def fetch_page(self, url: str) -> Optional[Tuple[str, str]]:
        """
        Fetch page content and status code

        Returns:
            Tuple of (html_content, status_code) or None if failed
        """
        try:
            response = self.session.get(url, timeout=self.timeout, allow_redirects=True)
            return response.text, response.status_code
        except requests.RequestException as e:
            logger.warning(f"Failed to fetch {url}: {str(e)}")
            return None

    def extract_links(self, html: str, current_url: str) -> Set[str]:
        """Extract all links from page"""
        try:
            soup = BeautifulSoup(html, "html.parser")
            links = set()

            for link in soup.find_all("a", href=True):
                href = link["href"].strip()
                if href:
                    full_url = urljoin(current_url, href)
                    # Remove fragments and parameters for cleaner URLs
                    full_url = full_url.split("#")[0]

                    if self.is_same_domain(full_url):
                        links.add(full_url)

            return links
        except Exception as e:
            logger.error(f"Error extracting links from {current_url}: {str(e)}")
            return set()

    def audit_page(self, url: str, html: str, status_code: int) -> Dict:
        """
        Audit individual page for SEO issues

        Returns:
            Dictionary containing detected issues
        """
        page_issues = {}
        soup = BeautifulSoup(html, "html.parser")

        # 1. Check Meta Titles
        title = soup.find("title")
        if not title or not title.string or len(title.string.strip()) == 0:
            page_issues["missing_meta_title"] = True
        elif len(title.string.strip()) < 30:
            page_issues["short_meta_title"] = (
                f"Title is {len(title.string.strip())} chars (recommended: 30-60)"
            )
        elif len(title.string.strip()) > 60:
            page_issues["long_meta_title"] = (
                f"Title is {len(title.string.strip())} chars (recommended: 30-60)"
            )

        # 2. Check Meta Descriptions
        meta_desc = soup.find("meta", attrs={"name": "description"})
        if not meta_desc or not meta_desc.get("content"):
            page_issues["missing_meta_description"] = True
        else:
            desc_content = meta_desc.get("content", "")
            if len(desc_content) < 120:
                page_issues["short_meta_description"] = (
                    f"Description is {len(desc_content)} chars (recommended: 120-160)"
                )
            elif len(desc_content) > 160:
                page_issues["long_meta_description"] = (
                    f"Description is {len(desc_content)} chars (recommended: 120-160)"
                )

        # 3. Check H1 Tags
        h1_tags = soup.find_all("h1")
        if len(h1_tags) == 0:
            page_issues["missing_h1"] = True
        elif len(h1_tags) > 1:
            page_issues["multiple_h1s"] = f"Found {len(h1_tags)} H1 tags (recommended: 1)"

        # 4. Check H1 Content
        if h1_tags:
            h1_text = h1_tags[0].get_text(strip=True)
            if len(h1_text) == 0:
                page_issues["empty_h1"] = True
            elif len(h1_text) > 70:
                page_issues["long_h1"] = f"H1 is {len(h1_text)} chars (recommended: <70)"

        # 5. Check Image Alt Attributes
        images = soup.find_all("img")
        images_without_alt = []
        for idx, img in enumerate(images):
            alt = img.get("alt", "").strip()
            if not alt:
                src = img.get("src", "Unknown")
                images_without_alt.append(src)

        if images_without_alt:
            page_issues["missing_image_alts"] = f"Found {len(images_without_alt)} images without alt text"

        # 6. Check Canonical Tags
        canonical = soup.find("link", attrs={"rel": "canonical"})
        if not canonical:
            page_issues["missing_canonical"] = True

        # 7. Check Open Graph Tags
        og_title = soup.find("meta", attrs={"property": "og:title"})
        og_description = soup.find("meta", attrs={"property": "og:description"})
        if not og_title or not og_description:
            page_issues["missing_og_tags"] = (
                "Missing Open Graph tags for social sharing"
            )

        # 8. Check Schema Markup (JSON-LD)
        schema_found = False
        for script in soup.find_all("script", attrs={"type": "application/ld+json"}):
            if script.string:
                schema_found = True
                break
        if not schema_found:
            page_issues["missing_schema_markup"] = (
                "No JSON-LD structured data found"
            )

        # 9. Check Broken Links
        broken_links = []
        for link in soup.find_all("a", href=True):
            href = link.get("href", "").strip()
            if href and href.startswith(("http://", "https://")):
                if self.is_same_domain(href):
                    # Will be checked separately in crawl
                    pass

        # 10. Check Page Load Performance (basic check)
        # In real implementation, use Lighthouse API or similar
        page_issues["_status_code"] = status_code
        page_issues["_word_count"] = len(soup.get_text().split())
        page_issues["_has_mobile_viewport"] = bool(
            soup.find("meta", attrs={"name": "viewport"})
        )

        return page_issues

    def crawl(self) -> Dict:
        """
        Crawl website and audit all pages

        Returns:
            Dictionary with all audit results
        """
        logger.info(f"Starting audit of {self.base_url}")

        # Start with base URL
        to_visit = [self.base_url]
        all_issues = {}
        broken_links = set()

        while to_visit and len(self.visited_urls) < self.max_pages:
            url = to_visit.pop(0)

            if url in self.visited_urls:
                continue

            self.visited_urls.add(url)
            logger.info(f"Auditing: {url} ({len(self.visited_urls)}/{self.max_pages})")

            # Fetch page
            result = self.fetch_page(url)
            if not result:
                broken_links.add(url)
                continue

            html, status_code = result

            # Check if successful response
            if status_code != 200:
                self.issues["slow_or_error_pages"].append(
                    {"url": url, "status_code": status_code}
                )
                continue

            # Audit page
            page_issues = self.audit_page(url, html, status_code)
            all_issues[url] = page_issues

            # Extract links for next crawl
            new_links = self.extract_links(html, url)
            for link in new_links:
                if link not in self.visited_urls:
                    to_visit.append(link)

            # Be respectful to server
            time.sleep(0.5)

        # Process all issues into categories
        self._process_issues(all_issues)
        self.issues["broken_links"] = list(broken_links)

        logger.info(
            f"Audit complete. Visited {len(self.visited_urls)} pages, found {sum(len(v) for v in self.issues.values())} issues"
        )

        return {
            "audited_pages": len(self.visited_urls),
            "issues": dict(self.issues),
            "timestamp": self.audit_timestamp.isoformat(),
        }

    def _process_issues(self, all_issues: Dict) -> None:
        """Process individual page issues into summary categories"""

        for url, issues in all_issues.items():
            # Missing Meta Titles
            if issues.get("missing_meta_title"):
                self.issues["missing_meta_titles"].append(url)

            # Short/Long Meta Titles
            if issues.get("short_meta_title"):
                self.issues["short_meta_titles"].append(
                    {"url": url, "issue": issues["short_meta_title"]}
                )
            if issues.get("long_meta_title"):
                self.issues["long_meta_titles"].append(
                    {"url": url, "issue": issues["long_meta_title"]}
                )

            # Missing Meta Descriptions
            if issues.get("missing_meta_description"):
                self.issues["missing_meta_descriptions"].append(url)

            # Short/Long Meta Descriptions
            if issues.get("short_meta_description"):
                self.issues["short_meta_descriptions"].append(
                    {"url": url, "issue": issues["short_meta_description"]}
                )
            if issues.get("long_meta_description"):
                self.issues["long_meta_descriptions"].append(
                    {"url": url, "issue": issues["long_meta_description"]}
                )

            # Missing H1 Tags
            if issues.get("missing_h1"):
                self.issues["missing_h1_tags"].append(url)

            # Multiple H1 Tags
            if issues.get("multiple_h1s"):
                self.issues["multiple_h1_tags"].append(
                    {"url": url, "issue": issues["multiple_h1s"]}
                )

            # Empty H1
            if issues.get("empty_h1"):
                self.issues["empty_h1_tags"].append(url)

            # Long H1
            if issues.get("long_h1"):
                self.issues["long_h1_tags"].append(
                    {"url": url, "issue": issues["long_h1"]}
                )

            # Missing Image Alts
            if issues.get("missing_image_alts"):
                self.issues["missing_image_alts"].append(
                    {"url": url, "issue": issues["missing_image_alts"]}
                )

            # Missing Canonical Tags
            if issues.get("missing_canonical"):
                self.issues["missing_canonical_tags"].append(url)

            # Missing Open Graph
            if issues.get("missing_og_tags"):
                self.issues["missing_og_tags"].append(url)

            # Missing Schema Markup
            if issues.get("missing_schema_markup"):
                self.issues["missing_schema_markup"].append(url)

            # Mobile Viewport
            if not issues.get("_has_mobile_viewport"):
                self.issues["missing_mobile_viewport"].append(url)

    def get_summary(self) -> Dict:
        """Get audit summary with issue counts"""
        summary = {
            "total_pages_audited": len(self.visited_urls),
            "total_issues_found": sum(
                len(v) if isinstance(v, (list, set)) else 1
                for v in self.issues.values()
            ),
            "issues_by_category": {},
        }

        for category, issues in self.issues.items():
            if isinstance(issues, (list, set)):
                summary["issues_by_category"][category] = len(issues)
            else:
                summary["issues_by_category"][category] = 1

        return summary
