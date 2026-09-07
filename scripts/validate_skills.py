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
SKILL_NAME = re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*$')


def validate_skill_resources(path: Path, text: str) -> list[str]:
    """Check concrete relative Markdown links without requiring workflow boilerplate."""
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


def load_registry(root: Path) -> tuple[dict[str, Any] | None, list[str]]:
    path = root / 'skills.registry.json'
    if not path.is_file():
        return None, []
    text, err = read_text(path)
    if err:
        return None, [f'skills.registry.json {err}']
    try:
        data = json.loads(text or '{}')
    except json.JSONDecodeError as exc:
        return None, [f'skills.registry.json invalid JSON: {exc}']
    return data, []


def validate_string_list(value: Any, field: str, skill: str) -> list[str]:
    if not isinstance(value, list):
        return [f'registry {skill}: {field} must be a list']
    if not value:
        return [f'registry {skill}: {field} should not be empty']
    if not all(isinstance(item, str) and item.strip() for item in value):
        return [f'registry {skill}: {field} must contain only non-empty strings']
    return []


def validate_registry(
    registry: dict[str, Any] | None,
    skill_names: set[str],
    package_names: set[str],
    selected_names: set[str] | None = None,
) -> tuple[list[dict[str, Any]], list[str]]:
    if not registry:
        return [], ['skills.registry.json missing; AI routing hints are unavailable']

    warnings: list[str] = []
    registry_items: list[dict[str, Any]] = []
    entries = registry.get('skills')
    if not isinstance(entries, list) or not entries:
        return registry_items, ['skills.registry.json: skills must be a non-empty list']

    seen: set[str] = set()
    for entry in entries:
        if not isinstance(entry, dict):
            warnings.append('skills.registry.json: each skill entry must be an object')
            continue
        skill = entry.get('skill')
        item_warnings: list[str] = []
        if not isinstance(skill, str) or not skill.strip():
            warnings.append('skills.registry.json: entry missing skill')
            continue
        if skill in seen:
            item_warnings.append(f'registry {skill}: duplicate entry')
        seen.add(skill)
        if skill not in skill_names:
            item_warnings.append(f'registry {skill}: unknown skill')

        package = entry.get('package')
        if not isinstance(package, str) or not package.strip():
            item_warnings.append(f'registry {skill}: package must be a non-empty string')
        elif package != 'unpackaged' and package not in package_names:
            item_warnings.append(f'registry {skill}: unknown package {package}')

        phase = entry.get('phase')
        if not isinstance(phase, str) or not phase.strip():
            item_warnings.append(f'registry {skill}: phase must be a non-empty string')

        for field in ['level_range', 'triggers', 'anti_triggers']:
            item_warnings.extend(validate_string_list(entry.get(field), field, skill))

        handoffs = entry.get('handoff_to', [])
        if not isinstance(handoffs, list) or not all(isinstance(name, str) for name in handoffs):
            item_warnings.append(f'registry {skill}: handoff_to must be a list of strings')
        else:
            for name in handoffs:
                if name not in skill_names:
                    item_warnings.append(f'registry {skill}: unknown handoff skill {name}')

        conflicts = entry.get('conflicts_with', [])
        if not isinstance(conflicts, list) or not all(isinstance(item, str) for item in conflicts):
            item_warnings.append(f'registry {skill}: conflicts_with must be a list of strings')

        if selected_names is None or skill in selected_names:
            registry_items.append({
                'skill': skill,
                'package': package,
                'phase': phase,
                'status': 'warning' if item_warnings else 'passed',
                'warnings': item_warnings,
            })
        warnings.extend(item_warnings)

    missing = sorted(skill_names - seen)
    if selected_names is not None:
        missing = [name for name in missing if name in selected_names]
    for skill in missing:
        warnings.append(f'registry missing skill: {skill}')

    return registry_items, warnings


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
            name = meta.get('name', '')
            if not SKILL_NAME.fullmatch(name) or len(name) > 64:
                item_errors.append('invalid skill name')
            if name != path.parent.name:
                item_errors.append('skill name must match directory name')
            item_errors.extend(validate_skill_resources(path, text or ''))
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

    package_names = {x.get('name') for x in package_items if x.get('name')}
    selected_names: set[str] | None = None
    if pack:
        selected = [x for x in package_items if x.get('name') == pack]
        if not selected:
            errors.append(f'pack not found: {pack}')
        else:
            selected_names = set(selected[0].get('skills', []))
            skill_items = [x for x in skill_items if x.get('name') in selected_names]
            package_items = selected

    registry, registry_errors = load_registry(root)
    errors.extend(registry_errors)
    registry_items, registry_warnings = validate_registry(
        registry,
        skill_names,
        package_names,
        selected_names,
    )
    warnings.extend(registry_warnings)

    return {
        'generated_at': datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        'summary': {
            'status': 'failed' if errors else 'passed',
            'skill_count': len(skill_items),
            'package_count': len(package_items),
            'registry_count': len(registry_items),
            'text_file_count': text_files,
            'error_count': len(errors),
            'warning_count': len(warnings),
        },
        'skills': skill_items,
        'packages': package_items,
        'registry': registry_items,
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
    for key in ['status', 'skill_count', 'package_count', 'registry_count', 'text_file_count', 'error_count', 'warning_count']:
        lines.append(f"| `{key}` | `{summary[key]}` |")
    lines.extend(['', '## Packages', '', '| Package | Skills | Status |', '| --- | ---: | --- |'])
    for item in result['packages']:
        lines.append(f"| `{item.get('name')}` | {item.get('skill_count')} | `{item.get('status')}` |")
    lines.extend(['', '## Skills', '', '| Skill | Path | Status |', '| --- | --- | --- |'])
    for item in result['skills']:
        lines.append(f"| `{item.get('name')}` | `{item.get('path')}` | `{item.get('status')}` |")
    lines.extend(['', '## Registry', '', '| Skill | Package | Phase | Status |', '| --- | --- | --- | --- |'])
    for item in result['registry']:
        lines.append(f"| `{item.get('skill')}` | `{item.get('package')}` | `{item.get('phase')}` | `{item.get('status')}` |")
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
