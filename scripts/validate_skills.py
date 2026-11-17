#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Validate skill structure: encoding, frontmatter, name, and linked resources."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

TEXT_SUFFIXES = {'.md', '.py', '.yaml', '.yml', '.json', '.toml', '.txt'}
SKILL_NAME = re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*$')


def validate_skill_resources(path: Path, text: str) -> list[str]:
    """Check that relative Markdown links point at existing files."""
    errors: list[str] = []
    for target in re.findall(r'\]\(([^)]+)\)', text):
        target = target.strip().strip('<>')
        if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', target) or target.startswith('#'):
            continue
        target = target.split('#', 1)[0]
        if target and not (path.parent / target).exists():
            errors.append(f'missing linked resource: {target}')
    return errors


def read_text(path: Path) -> tuple[str | None, str | None]:
    data = path.read_bytes()
    if data.startswith(b'\xef\xbb\xbf'):
        return None, 'has UTF-8 BOM'
    try:
        return data.decode('utf-8'), None
    except UnicodeDecodeError as exc:
        return None, f'invalid UTF-8: {exc}'


def parse_frontmatter(text: str) -> tuple[dict[str, str], str | None]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != '---':
        return {}, 'missing opening frontmatter delimiter'
    try:
        end = lines[1:].index('---') + 1
    except ValueError:
        return {}, 'missing closing frontmatter delimiter'
    meta: dict[str, str] = {}
    frontmatter_lines = lines[1:end]
    for index, line in enumerate(frontmatter_lines):
        if ':' not in line:
            continue
        key, value = line.split(':', 1)
        key = key.strip()
        value = value.strip()
        if value in {'>', '>-', '|', '|-'}:
            folded: list[str] = []
            for extra in frontmatter_lines[index + 1:]:
                if not extra.startswith('  '):
                    break
                folded.append(extra.strip())
            meta[key] = ' '.join(folded).strip()
        else:
            meta[key] = value.strip('"').strip("'")
    if not meta.get('name'):
        return meta, 'missing name in frontmatter'
    if not meta.get('description'):
        return meta, 'missing description in frontmatter'
    return meta, None


def is_scanned(root: Path, path: Path) -> bool:
    """Skip hidden directories (.git, .venv) and bytecode caches."""
    parts = path.relative_to(root).parts
    return not any(part.startswith('.') or part == '__pycache__' for part in parts[:-1])


def collect(root: Path) -> dict[str, Any]:
    errors: list[str] = []
    skill_items: list[dict[str, Any]] = []
    text_files = 0

    for path in sorted(root.rglob('*')):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES or not is_scanned(root, path):
            continue
        text_files += 1
        _, err = read_text(path)
        if err:
            errors.append(f'{path.relative_to(root).as_posix()}: {err}')

    for path in sorted((root / 'skills').glob('*/SKILL.md')):
        rel = path.relative_to(root).as_posix()
        item_errors: list[str] = []
        meta: dict[str, str] = {}
        text, err = read_text(path)
        if err:
            item_errors.append(err)
        else:
            meta, fm_err = parse_frontmatter(text or '')
            if fm_err:
                item_errors.append(fm_err)
            name = meta.get('name', '')
            if not SKILL_NAME.fullmatch(name) or len(name) > 64:
                item_errors.append('invalid skill name')
            if name != path.parent.name:
                item_errors.append('skill name must match directory name')
            item_errors.extend(validate_skill_resources(path, text or ''))
        skill_items.append({
            'path': rel,
            'name': meta.get('name'),
            'description': meta.get('description'),
            'status': 'failed' if item_errors else 'passed',
            'errors': item_errors,
        })
        errors.extend(f'{rel}: {e}' for e in item_errors)

    return {
        'generated_at': datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        'summary': {
            'status': 'failed' if errors else 'passed',
            'skill_count': len(skill_items),
            'text_file_count': text_files,
            'error_count': len(errors),
        },
        'skills': skill_items,
        'errors': errors,
    }


def render_status(result: dict[str, Any]) -> str:
    lines = [
        '# Skills Garage Status',
        '',
        f"Generated at: `{result['generated_at']}`",
        '',
        '## Summary',
        '',
        '| Metric | Value |',
        '| --- | ---: |',
    ]
    for key, value in result['summary'].items():
        lines.append(f'| `{key}` | `{value}` |')
    lines.extend(['', '## Skills', '', '| Skill | Path | Status |', '| --- | --- | --- |'])
    for item in result['skills']:
        lines.append(f"| `{item.get('name')}` | `{item.get('path')}` | `{item.get('status')}` |")
    if result['errors']:
        lines.extend(['', '## Errors', ''])
        lines.extend(f'- {err}' for err in result['errors'])
    lines.append('')
    return '\n'.join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description='Validate skill structure.')
    parser.add_argument('--root', default='.', help='Repository root')
    parser.add_argument('--format', choices=('json', 'markdown'), default='json')
    args = parser.parse_args()

    result = collect(Path(args.root).resolve())
    if args.format == 'markdown':
        print(render_status(result), end='')
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if result['summary']['status'] != 'passed' else 0


if __name__ == '__main__':
    raise SystemExit(main())
