#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Validate leroy-skills-garage skill structure and generated status."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

TEXT_SUFFIXES = {'.md', '.py', '.yaml', '.yml', '.json', '.toml', '.txt'}
REQUIRED_SECTIONS = ('## Contract', '## Fallback', '## Handoff')


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
    for line in lines[1:end]:
        if ':' not in line:
            continue
        key, value = line.split(':', 1)
        meta[key.strip()] = value.strip().strip('"').strip("'")
    if not meta.get('name'):
        return meta, 'missing name in frontmatter'
    if not meta.get('description'):
        return meta, 'missing description in frontmatter'
    return meta, None


def load_packages(root: Path) -> tuple[dict[str, Any] | None, list[str]]:
    path = root / 'skills.packages.json'
    if not path.is_file():
        return None, ['skills.packages.json missing']
    text, err = read_text(path)
    if err:
        return None, [f'skills.packages.json {err}']
    try:
        data = json.loads(text or '{}')
    except json.JSONDecodeError as exc:
        return None, [f'skills.packages.json invalid JSON: {exc}']
    return data, []


def collect(root: Path, pack: str | None = None) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    skill_items: list[dict[str, Any]] = []
    text_files = 0
    bom_or_invalid: list[str] = []

    for path in sorted(root.rglob('*')):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        rel = path.relative_to(root).as_posix()
        if rel.startswith('devflow/') or '/__pycache__/' in rel:
            continue
        text_files += 1
        _, err = read_text(path)
        if err:
            bom_or_invalid.append(f'{rel}: {err}')

    if bom_or_invalid:
        errors.extend(bom_or_invalid)

    for path in sorted((root / 'skills').glob('*/SKILL.md')):
        rel = path.relative_to(root).as_posix()
        text, err = read_text(path)
        item: dict[str, Any] = {'path': rel, 'status': 'passed'}
        item_errors: list[str] = []
        if err:
            item_errors.append(err)
            meta = {}
        else:
            meta, fm_err = parse_frontmatter(text or '')
            if fm_err:
                item_errors.append(fm_err)
            missing_sections = [section for section in REQUIRED_SECTIONS if section not in (text or '')]
            if missing_sections:
                item_errors.append('missing sections: ' + ', '.join(missing_sections))
        item['name'] = meta.get('name') if 'meta' in locals() else None
        item['description'] = meta.get('description') if 'meta' in locals() else None
        item['errors'] = item_errors
        if item_errors:
            item['status'] = 'failed'
            errors.extend(f'{rel}: {e}' for e in item_errors)
        skill_items.append(item)

    skill_names = {x.get('name') for x in skill_items if x.get('name')}
    packages, package_errors = load_packages(root)
    errors.extend(package_errors)
    package_items: list[dict[str, Any]] = []
    if packages:
        seen_package_names: set[str] = set()
        for item in packages.get('packages', []):
            name = item.get('name')
            item_errors: list[str] = []
            if not name:
                item_errors.append('missing package name')
            elif name in seen_package_names:
                item_errors.append(f'duplicate package name: {name}')
            seen_package_names.add(name)
            skills = item.get('skills', [])
            if not isinstance(skills, list) or not skills:
                item_errors.append('skills must be a non-empty list')
                skills = []
            missing = sorted(set(skills) - skill_names)
            if missing:
                item_errors.append('unknown skills: ' + ', '.join(missing))
            if not item.get('verify'):
                item_errors.append('missing verify command')
            package_items.append({
                'name': name,
                'skill_count': len(skills),
                'skills': skills,
                'status': 'failed' if item_errors else 'passed',
                'errors': item_errors,
            })
            errors.extend(f'package {name}: {e}' for e in item_errors)

    if pack:
        selected = [x for x in package_items if x.get('name') == pack]
        if not selected:
            errors.append(f'pack not found: {pack}')
        else:
            selected_names = set(selected[0].get('skills', []))
            skill_items = [x for x in skill_items if x.get('name') in selected_names]
            package_items = selected

    return {
        'generated_at': datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        'summary': {
            'status': 'failed' if errors else 'passed',
            'skill_count': len(skill_items),
            'package_count': len(package_items),
            'text_file_count': text_files,
            'error_count': len(errors),
            'warning_count': len(warnings),
        },
        'skills': skill_items,
        'packages': package_items,
        'errors': errors,
        'warnings': warnings,
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
    summary = result['summary']
    for key in ['status', 'skill_count', 'package_count', 'text_file_count', 'error_count', 'warning_count']:
        lines.append(f"| `{key}` | `{summary[key]}` |")
    lines.extend(['', '## Packages', '', '| Package | Skills | Status |', '| --- | ---: | --- |'])
    for item in result['packages']:
        lines.append(f"| `{item.get('name')}` | {item.get('skill_count')} | `{item.get('status')}` |")
    lines.extend(['', '## Skills', '', '| Skill | Path | Status |', '| --- | --- | --- |'])
    for item in result['skills']:
        lines.append(f"| `{item.get('name')}` | `{item.get('path')}` | `{item.get('status')}` |")
    if result['errors']:
        lines.extend(['', '## Errors', ''])
        for err in result['errors']:
            lines.append(f'- {err}')
    if result['warnings']:
        lines.extend(['', '## Warnings', ''])
        for warn in result['warnings']:
            lines.append(f'- {warn}')
    lines.append('')
    return '\n'.join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description='Validate skill structure and status assets.')
    parser.add_argument('--root', default='.', help='Repository root')
    parser.add_argument('--pack', help='Validate a single package from skills.packages.json')
    parser.add_argument('--write-status', help='Write markdown status report to this path')
    parser.add_argument('--format', choices=('json', 'markdown'), default='json')
    args = parser.parse_args()

    root = Path(args.root).resolve()
    result = collect(root, args.pack)
    if args.write_status:
        out = Path(args.write_status)
        if not out.is_absolute():
            out = root / out
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render_status(result), encoding='utf-8')

    if args.format == 'markdown':
        print(render_status(result), end='')
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if result['summary']['status'] != 'passed' else 0


if __name__ == '__main__':
    raise SystemExit(main())
