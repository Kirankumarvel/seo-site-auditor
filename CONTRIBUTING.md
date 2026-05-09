# Contributing to SEO Auditor

Thank you for your interest in contributing! We welcome all types of contributions - bug reports, feature requests, documentation improvements, and code contributions.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/yourusername/seo-auditor.git
   cd seo-auditor
   ```

3. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install pytest pytest-cov black flake8
   ```

## Development Workflow

### Making Changes

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** and test thoroughly

3. **Run tests**:
   ```bash
   pytest tests/ -v
   ```

4. **Format code** with Black:
   ```bash
   black seo_auditor/ tests/
   ```

5. **Lint with flake8**:
   ```bash
   flake8 seo_auditor/
   ```

### Commit Guidelines

- Use clear, descriptive commit messages
- Prefix commits with: `feat:`, `fix:`, `docs:`, `test:`, `refactor:`
- Example: `feat: add concurrent crawling support`

### Pull Request Process

1. **Update your branch** with latest main:
   ```bash
   git pull origin main
   ```

2. **Push your changes**:
   ```bash
   git push origin feature/your-feature-name
   ```

3. **Open a Pull Request** with:
   - Clear title describing the change
   - Description of what changed and why
   - Reference to any related issues (e.g., "Fixes #123")
   - Test results/coverage

4. **Address review feedback** promptly

## Code Standards

### Style Guide

- Follow PEP 8
- Use Black for formatting
- Maximum line length: 100 characters
- Use type hints where appropriate

### Example:

```python
def audit_page(self, url: str, html: str, status_code: int) -> Dict:
    """
    Audit individual page for SEO issues.

    Args:
        url: The page URL
        html: Page HTML content
        status_code: HTTP status code

    Returns:
        Dictionary containing detected issues
    """
    # Implementation
```

## Testing

- Add tests for new features
- Maintain >80% code coverage
- Run full test suite before submitting PR:
  ```bash
  pytest tests/ -v --cov=seo_auditor
  ```

## Documentation

- Update README.md for new features
- Add docstrings to all functions/classes
- Update CHANGELOG.md for significant changes

## Areas for Contribution

### High Priority
- [ ] Concurrent/async crawling
- [ ] JavaScript rendering support
- [ ] Lighthouse integration
- [ ] Core Web Vitals monitoring

### Medium Priority
- [ ] Sitemap validation
- [ ] Robots.txt analysis
- [ ] Historical tracking
- [ ] Web dashboard

### Community Help Needed
- Documentation improvements
- Example use cases
- Language translations
- Bug reports and fixes

## Reporting Issues

When reporting bugs, please include:

1. **Description**: What happened and what was expected
2. **Steps to reproduce**: Exact steps to trigger the issue
3. **Environment**: 
   - Python version
   - OS
   - Package versions
4. **Code example**:
   ```python
   # Your code that triggers the issue
   ```
5. **Error message**: Full stack trace if applicable

## Feature Requests

For feature requests:

1. **Title**: Clear, concise description
2. **Motivation**: Why this feature is needed
3. **Implementation**: Suggested approach (optional)
4. **Example usage**: How users would use it

## Community Guidelines

- Be respectful and inclusive
- Focus on the code, not the person
- Help others learn and grow
- Ask questions if unclear
- Share knowledge generously

## Getting Help

- **Questions**: Open a Discussion
- **Bugs**: Open an Issue with detailed info
- **Ideas**: Start a Discussion first
- **Chat**: Join our community Slack (coming soon)

## Recognition

Contributors will be:
- Added to CONTRIBUTORS.md
- Mentioned in release notes
- Credited in README

Thank you for making SEO Auditor better! 🙌
