from pathlib import Path
import tempfile
import unittest

from scripts.validate_skills import collect, parse_frontmatter, validate_skill_resources

ROOT = Path(__file__).resolve().parents[1]


class SkillValidationTests(unittest.TestCase):
    def test_minimal_skill_with_reference_is_valid(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'reference.md').write_text('Useful detail', encoding='utf-8')
            text = '---\nname: sample\ndescription: A focused task.\n---\n[Detail](reference.md)\n'
            meta, error = parse_frontmatter(text)
            self.assertIsNone(error)
            self.assertEqual(meta['name'], 'sample')
            self.assertEqual(validate_skill_resources(root / 'SKILL.md', text), [])

    def test_missing_resource_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            errors = validate_skill_resources(Path(tmp) / 'SKILL.md', '[Detail](missing.md)')
            self.assertEqual(errors, ['missing linked resource: missing.md'])

    def test_name_must_match_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            skill = Path(tmp) / 'skills' / 'sample'
            skill.mkdir(parents=True)
            (skill / 'SKILL.md').write_text(
                '---\nname: other\ndescription: A focused task.\n---\n', encoding='utf-8'
            )
            result = collect(Path(tmp))
            self.assertEqual(result['summary']['status'], 'failed')
            self.assertTrue(any('skill name must match directory name' in e for e in result['errors']))

    def test_bom_is_reported_and_hidden_directories_are_skipped(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / '.venv').mkdir()
            (root / '.venv' / 'ignored.md').write_bytes(b'\xef\xbb\xbfignored')
            self.assertEqual(collect(root)['summary']['status'], 'passed')
            (root / 'notes.md').write_bytes(b'\xef\xbb\xbfreported')
            result = collect(root)
            self.assertEqual(result['errors'], ['notes.md: has UTF-8 BOM'])

    def test_repository_skills_are_valid(self):
        result = collect(ROOT)
        self.assertEqual(result['summary']['status'], 'passed', result['errors'])
        self.assertGreater(result['summary']['skill_count'], 0)


if __name__ == '__main__':
    unittest.main()
