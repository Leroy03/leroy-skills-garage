"""Verify the synchronized personal skill files against an explicit global source."""
import argparse
import ast
import hashlib
import json
from pathlib import Path


def inventory(root):
    return {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in root.rglob('*') if p.is_file()
            and '__pycache__' not in p.parts and p.suffix not in {'.pyc', '.pyo'}}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    source = args.source.resolve()
    names = {p.parent.name for p in (source / 'skills').glob('*/SKILL.md')}
    actual_names = {p.parent.name for p in (root / 'skills').glob('*/SKILL.md')}
    errors = []
    if names != actual_names:
        errors.append(f'Skill set mismatch: {names ^ actual_names}')
    manifest = {}
    for name in sorted(names):
        expected = inventory(source / 'skills' / name)
        actual = inventory(root / 'skills' / name)
        if expected != actual:
            errors.append(f'File mismatch: {name}')
        manifest[name] = actual
    for target, origin in [('AGENTS.md','AGENTS.md'), ('CLAUDE.md','AGENTS.md'),
                           ('skills/collaboration-protocol.yaml','skills/collaboration-protocol.yaml'),
                           ('skills/CONTRACT_TEMPLATE.md','skills/CONTRACT_TEMPLATE.md'),
                           ('inject/devflow-marshal-context.md','inject/devflow-marshal-context.md')]:
        if (root / target).read_bytes() != (source / origin).read_bytes():
            errors.append(f'Rule mismatch: {target}')
    if (root / 'PUA').exists():
        errors.append('Retired duplicate PUA directory still exists')
    compiled = 0
    for path in (root / 'skills').rglob('*.py'):
        ast.parse(path.read_text(encoding='utf-8'), filename=str(path))
        compiled += 1
    report = dict(status='failed' if errors else 'passed', skill_count=len(names),
                  file_count=sum(map(len, manifest.values())), python_syntax_checked=compiled,
                  errors=errors, sha256=manifest)
    (Path(__file__).parent / 'source_manifest.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k != 'sha256'}, ensure_ascii=False))
    return bool(errors)


if __name__ == '__main__':
    raise SystemExit(main())
