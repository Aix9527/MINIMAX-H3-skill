import copy
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from validate_voice import validate_voices

class VoiceTests(unittest.TestCase):
    def setUp(self):
        self.plan=json.loads((ROOT/'examples/voice-consistency.director.json').read_text(encoding='utf-8'))
        self.review=json.loads((ROOT/'examples/voice-consistency.review.json').read_text(encoding='utf-8'))
    def report(self):return validate_voices(self.plan,self.review)
    def codes(self):return {f['code'] for f in self.report()['findings']}
    def test_valid_routing(self):
        self.assertFalse(any(f['level']=='error' for f in self.report()['findings']))
    def test_unused_voice(self):
        s=self.plan['shots'][0];s['prompt']=s['prompt'].replace('{{ref:WANG_VOICE}}','the voice reference')
        self.assertIn('VOICE_REFERENCE_NOT_ACTIVE',self.codes())
    def test_duplicate_id(self):
        self.review['voices']['OTHER']=copy.deepcopy(self.review['voices']['WANG'])
        self.assertIn('DUPLICATE_SPEAKER_ID',self.codes())
        self.assertIn('SHARED_VOICE_REFERENCE',self.codes())
    def test_wrong_kind(self):
        self.plan['assets'][1]['kind']='image'
        self.assertIn('INVALID_VOICE_ASSET',self.codes())
    def test_unknown_speaker(self):
        self.review['shots']['shot_001']['activeSpeakerIds']=['UNKNOWN']
        self.assertIn('UNREGISTERED_SPEAKER',self.codes())
    def test_missing_tag(self):
        s=self.plan['shots'][0];s['prompt']=s['prompt'].replace('(S1)','')
        self.assertIn('SPEAKER_TAG_MISSING',self.codes())
    def test_inactive_voice(self):
        self.review['shots']['shot_001']['activeSpeakerIds']=[]
        self.assertIn('INACTIVE_SPEAKER_VOICE',self.codes())
    def test_no_perceptual_claim(self):
        self.assertEqual(self.report()['audioListening'],'NOT_TESTED')

if __name__=='__main__':unittest.main()
