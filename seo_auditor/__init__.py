"""
SEO Site Auditor - Automated website SEO analysis tool
Detects common SEO issues and generates detailed audit reports
"""

__version__ = "1.0.0"
__author__ = "Kiran"
__description__ = "Automated SEO Site Auditor for comprehensive website analysis"

from .auditor import SEOAuditor
from .report import AuditReport

__all__ = ["SEOAuditor", "AuditReport"]
