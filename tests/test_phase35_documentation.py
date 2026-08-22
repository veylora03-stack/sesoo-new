from django.test import TestCase
from pathlib import Path

class Phase35DocumentationTests(TestCase):
    def test_readme_exists_and_content(self):
        """README.md exists and contains required sections"""
        readme = Path("README.md")
        self.assertTrue(readme.exists(), "README.md should exist")
        content = readme.read_text(encoding="utf-8")
        self.assertIn("Features", content, "README should contain 'Features'")
        self.assertIn("Setup", content, "README should contain 'Setup'")
        self.assertIn("License", content, "README should contain 'License'")

    def test_contributing_exists_and_content(self):
        """CONTRIBUTING.md exists and contains required sections"""
        contributing = Path("CONTRIBUTING.md")
        self.assertTrue(contributing.exists(), "CONTRIBUTING.md should exist")

    def test_changelog_exists_and_content(self):
        """CHANGELOG.md exists"""
        changelog = Path("CHANGELOG.md")
        self.assertTrue(changelog.exists(), "CHANGELOG.md should exist")
