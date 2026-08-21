from django.test import TestCase
from pathlib import Path
import os
import stat

class Phase36CleanupTests(TestCase):
    def test_gitignore_contains_required_patterns(self):
        """.gitignore contains __pycache__/, staticfiles/, and media/"""
        gitignore = Path(".gitignore")
        self.assertTrue(gitignore.exists(), ".gitignore should exist")
        content = gitignore.read_text(encoding="utf-8")
        self.assertIn("__pycache__/", content, ".gitignore should ignore __pycache__/")
        self.assertIn("staticfiles/", content, ".gitignore should ignore staticfiles/")
        self.assertIn("media/", content, ".gitignore should ignore media/")

    def test_cleanup_script_exists_and_executable(self):
        """deploy/cleanup.sh exists and is executable"""
        cleanup = Path("deploy/cleanup.sh")
        self.assertTrue(cleanup.exists(), "deploy/cleanup.sh should exist")
        
        # Check if file has executable bit (via git ls-files --stage)
        import subprocess
        result = subprocess.run(
            ["git", "ls-files", "--stage", "deploy/cleanup.sh"],
            capture_output=True,
            text=True
        )
        # Mode 100755 means executable
        self.assertIn("100755", result.stdout, "cleanup.sh should be executable (100755)")

    def test_nginx_not_tracked(self):
        """deploy/nginx/ should not be tracked in git"""
        import subprocess
        result = subprocess.run(
            ["git", "ls-files", "deploy/nginx/"],
            capture_output=True,
            text=True
        )
        self.assertEqual(result.stdout.strip(), "", "deploy/nginx/ should not be tracked in git")