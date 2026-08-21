from django.test import TestCase
from pathlib import Path

class Phase35DocumentationTests(TestCase):
    def test_readme_exists_and_content(self):
        """README.md exists and contains required sections"""
        readme = Path("README.md")
        self.assertTrue(readme.exists(), "README.md should exist")
        content = readme.read_text(encoding="utf-8")
        self.assertIn("امکانات", content, "README should contain 'امکانات'")
        self.assertIn("نصب و راه‌اندازی", content, "README should contain installation section")

    def test_contributing_exists_and_content(self):
        """CONTRIBUTING.md exists and contains required sections"""
        contributing = Path("CONTRIBUTING.md")
        self.assertTrue(contributing.exists(), "CONTRIBUTING.md should exist")
        content = contributing.read_text(encoding="utf-8")
        self.assertIn("نحوه مشارکت", content, "CONTRIBUTING should contain contribution guidelines")

    def test_changelog_exists_and_content(self):
        """CHANGELOG.md exists and contains version 1.0.0"""
        changelog = Path("CHANGELOG.md")
        self.assertTrue(changelog.exists(), "CHANGELOG.md should exist")
        content = changelog.read_text(encoding="utf-8")
        self.assertIn("[1.0.0]", content, "CHANGELOG should contain version 1.0.0")