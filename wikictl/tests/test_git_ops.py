"""Tests para el módulo core/git_ops.py."""

import tempfile
import unittest
from pathlib import Path
import subprocess

from wikictl.core.git_ops import (
    generate_diff,
    format_knowledge_commit_message,
    is_git_repo,
    stage_and_commit,
)


class TestGitOps(unittest.TestCase):
    def test_generate_diff(self):
        old = "linea 1\nlinea 2\n"
        new = "linea 1\nlinea modificada\n"
        diff = generate_diff(old, new, "test.md")
        self.assertIn("--- a/test.md", diff)
        self.assertIn("+++ b/test.md", diff)
        self.assertIn("-linea 2", diff)
        self.assertIn("+linea modificada", diff)

    def test_format_commit_message(self):
        msg = format_knowledge_commit_message(
            "promote",
            "cognitive-offloading",
            ["created wiki/concepts/cognitive-offloading.md", "linked references"],
        )
        self.assertIn("knowledge: promote cognitive-offloading", msg)
        self.assertIn("- created wiki/concepts/cognitive-offloading.md", msg)
        self.assertIn("- linked references", msg)

    def test_git_operations_in_temp_repo(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_path = Path(temp_dir)
            # Inicializar repo temporal
            subprocess.run(["git", "init"], cwd=repo_path, capture_output=True, check=True)
            subprocess.run(
                ["git", "config", "user.email", "test@example.com"],
                cwd=repo_path,
                capture_output=True,
                check=True,
            )
            subprocess.run(
                ["git", "config", "user.name", "Test User"],
                cwd=repo_path,
                capture_output=True,
                check=True,
            )

            self.assertTrue(is_git_repo(repo_path))

            # Crear archivo y hacer commit
            test_file = repo_path / "nota.md"
            test_file.write_text("# Contenido", encoding="utf-8")

            success, log = stage_and_commit(repo_path, "knowledge: initial test")
            self.assertTrue(success)
            self.assertIn("knowledge: initial test", log)


if __name__ == "__main__":
    unittest.main()
