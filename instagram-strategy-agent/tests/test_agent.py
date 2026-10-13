import unittest
from agent.server import validate
from agent.prompt import fallback_strategy

class AgentTests(unittest.TestCase):
    def test_validation_requires_core_fields(self):
        with self.assertRaises(ValueError): validate({'brand': 'Only brand'})
    def test_fallback_has_twelve_calendar_entries(self):
        data = {'brand': 'Acme', 'niche': 'designers', 'audience': 'founders', 'offer': 'consulting', 'goal': 'leads'}
        plan = fallback_strategy(data)
        self.assertEqual(len(plan['calendar']), 12)
        self.assertEqual(len(plan['content_pillars']), 4)
    def test_validation_trims_values(self):
        data = {'brand': ' Acme ', 'niche': 'design', 'audience': 'founders', 'offer': 'audit', 'goal': 'leads'}
        self.assertEqual(validate(data)['brand'], 'Acme')

if __name__ == '__main__': unittest.main()
