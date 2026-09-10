import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from validate_dialogue import validate_dialogue

class OwnershipTests(unittest.TestCase):
    def setUp(self):
        self.plan=json.loads((ROOT/'examples/dialogue-ownership.director.json').read_text(encoding='utf-8'))
        self.review=json.loads((ROOT/'examples/dialogue-ownership.review.json').read_text(encoding='utf-8'))
    def report(self):return validate_dialogue(self.plan,self.review)
    def codes(self):return {f['code'] for f in self.report()['findings']}
    def test_correct_dream_and_inner_ownership(self):
        self.assertFalse(any(f['level']=='error' for f in self.report()['findings']))
    def test_wrong_speaker(self):
        s=self.plan['shots'][0];s['prompt']=s['prompt'].replace('(S1) says:', '(S2) says:')
        self.assertIn('DIALOGUE_SPEAKER_MISMATCH',self.codes())
    def test_changed_words(self):
        s=self.plan['shots'][0];s['prompt']=s['prompt'].replace('别开门。','快开门。')
        self.assertIn('DIALOGUE_TEXT_CHANGED',self.codes())
    def test_missing_line(self):
        s=self.plan['shots'][0];s['prompt']=s['prompt'].replace('<d>[Chinese]别开门。</d>','')
        self.assertIn('DIALOGUE_COUNT_MISMATCH',self.codes())
    def test_inner_not_spoken_aloud(self):
        s=self.plan['shots'][1];s['prompt']=s['prompt'].replace('says in an off-screen voiceover','says')
        self.assertIn('VOICEOVER_DELIVERY_MISSING',self.codes())
    def test_onscreen_requires_visible_owner(self):
        self.review['shots']['shot_001']['visibleCharacterIds']=[]
        self.assertIn('ONSCREEN_SPEAKER_NOT_VISIBLE',self.codes())
    def test_missing_ledger_is_not_success(self):
        del self.review['shots']['shot_001']['dialogueLines']
        self.assertIn('DIALOGUE_LEDGER_MISSING',self.codes())
    def test_lipsync_not_claimed(self):
        self.assertEqual(self.report()['lipSyncReview'],'NOT_TESTED')

if __name__=='__main__':unittest.main()
