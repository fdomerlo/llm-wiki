"""Operaciones Git y generación de diffs unificados para auditoría y seguridad."""

from __future__ import annotations
import difflib
from pathlib import Path
import subprocess


def generate_diff(old_content: str, new_content: str, filename: str = "note.md") -> str:
    """Genera un diff unificado legible entre el contenido anterior y el nuevo."""
    old_lines = old_content.splitlines(keepends=True)
    new_lines = new_content.splitlines(keepends=True)

    diff = difflib.unified_diff(
        old_lines,
        new_lines,
        fromfile=f"a/{filename}",
        tofile=f"b/{filename}",
    )
    return "".join(diff)


def is_git_repo(repo_dir: Path) -> bool:
    """Verifica si el directorio está bajo control de versiones Git."""
    try:
        res = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            cwd=repo_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
        return res.returncode == 0 and res.stdout.strip() == "true"
    except Exception:
        return False


def is_dirty(repo_dir: Path) -> bool:
    """Indica si existen cambios pendientes de commit."""
    if not is_git_repo(repo_dir):
        return False
    try:
        res = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=repo_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
        return bool(res.stdout.strip())
    except Exception:
        return False


def stage_and_commit(
    repo_dir: Path,
    message: str,
    files: list[str] | None = None,
) -> tuple[bool, str]:
    """Agrega archivos y crea un commit descriptivo en Git."""
    if not is_git_repo(repo_dir):
        return False, "No es un repositorio Git válido."

    try:
        # git add
        add_cmd = ["git", "add"]
        if files:
            add_cmd.extend(files)
        else:
            add_cmd.append(".")

        add_res = subprocess.run(
            add_cmd,
            cwd=repo_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
        if add_res.returncode != 0:
            return False, f"Error en git add: {add_res.stderr.strip()}"

        # git commit
        commit_res = subprocess.run(
            ["git", "commit", "-m", message],
            cwd=repo_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
        if commit_res.returncode != 0:
            return False, f"Error en git commit: {commit_res.stderr.strip()}"

        return True, commit_res.stdout.strip()
    except Exception as e:
        return False, f"Excepción durante commit: {e}"


def format_knowledge_commit_message(
    action: str,
    target: str,
    details: list[str] | None = None,
) -> str:
    """Construye un mensaje de commit estructurado según las directivas de AGENTS.md."""
    header = f"knowledge: {action} {target}"
    if not details:
        return header
    bullet_points = "\n".join(f"- {d}" for d in details)
    return f"{header}\n\n{bullet_points}"
