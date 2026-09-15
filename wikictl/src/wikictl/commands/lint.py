"""Comando 'wikictl lint' para auditoría determinística del baúl."""

from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

from wikictl.core.vault import Vault
from wikictl.core.validator import lint_vault


def execute_lint(args: argparse.Namespace) -> int:
    vault = Vault(args.vault_dir).scan()
    issues = lint_vault(vault, path_filter=args.path)

    if args.json:
        payload = [
            {
                "level": i.level,
                "category": i.category,
                "file": i.file,
                "message": i.message,
                "line": i.line,
            }
            for i in issues
        ]
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        has_errors = any(i.level == "ERROR" for i in issues)
        has_warnings = any(i.level == "WARNING" for i in issues)
        if has_errors or (args.strict and has_warnings):
            return 1
        return 0

    # Formato legible para terminal
    print(f"\n🔍 Auditando Baúl: {vault.root}")
    print(f"Total de notas indexadas: {len(vault.notes)}\n" + "-" * 60)

    if not issues:
        print("✅ Baúl en perfecto estado. No se detectaron problemas de integridad ni esquema.\n")
        return 0

    errors = [i for i in issues if i.level == "ERROR"]
    warnings = [i for i in issues if i.level == "WARNING"]
    infos = [i for i in issues if i.level == "INFO"]

    for issue in issues:
        prefix = {
            "ERROR": "❌ [ERROR]",
            "WARNING": "⚠️  [WARN] ",
            "INFO": "ℹ️  [INFO] ",
        }.get(issue.level, issue.level)
        print(f"{prefix} ({issue.category}) {issue.file}: {issue.message}")

    print("-" * 60)
    print(f"Resumen: {len(errors)} errores, {len(warnings)} advertencias, {len(infos)} avisos.\n")

    if errors or (args.strict and warnings):
        return 1
    return 0
