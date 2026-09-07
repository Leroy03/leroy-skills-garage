from pathlib import Path
import tempfile
import unittest

from scripts.validate_skills import parse_frontmatter, validate_registry, validate_skill_resources


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

    def test_retired_handoff_is_reported_but_no_handoff_is_allowed(self):
        entry = dict(skill='sample', package='core', phase='task', level_range=['L1'],
                     triggers=['task'], anti_triggers=['unrelated'], handoff_to=[])
        _, warnings = validate_registry({'skills': [entry]}, {'sample'}, {'core'})
        self.assertEqual(warnings, [])
        entry['handoff_to'] = ['retired']
        _, warnings = validate_registry({'skills': [entry]}, {'sample'}, {'core'})
        self.assertTrue(any('unknown handoff skill retired' in warning for warning in warnings))


if __name__ == '__main__':
    unittest.main()
