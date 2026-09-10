import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from validate_plan import validate

class PreflightTests(unittest.TestCase):
    def setUp(self):
        self.plan=json.loads((ROOT/'examples/single-dialogue.director.json').read_text(encoding='utf-8'))
    def codes(self, p=None, review=None, input_root=None):
        return {f['code'] for f in validate(p or self.plan,input_root=input_root,review=review)['findings']}
    def asset(self):
        self.plan['assets']=[dict(id='face',alias='FACE',kind='image',path='face.png')]
    def test_valid_example(self):
        self.assertFalse(any(f['level']=='error' for f in validate(self.plan)['findings']))
    def test_imported_but_unused(self):
        self.asset()
        self.assertIn('CATALOG_WITH_ZERO_ACTIVE_REFERENCES',self.codes())
        self.assertIn('EXPECTED_REFERENCE_NOT_ACTIVE',self.codes(review={'shots':{'shot_001':{'requiredAliases':['FACE']}}}))
    def test_disabled_reference(self):
        self.asset();self.plan['assets'][0]['enabled']=False
        self.plan['shots'][0]['prompt']+=' {{ref:FACE}}'
        self.assertIn('UNRESOLVED_REFERENCE',self.codes())
    def test_fixed_reference(self):
        self.asset();self.plan['assets'][0]['fixed']=True
        self.assertEqual(validate(self.plan)['shots'][0]['imageCount'],1)
    def test_scope_exclusion(self):
        self.asset();self.plan['assets'][0].update(fixed=True,shotIds=['shot_002'])
        self.assertEqual(validate(self.plan)['shots'][0]['imageCount'],0)
    def test_scene_relay(self):
        p=json.loads((ROOT/'examples/scene-change.director.json').read_text(encoding='utf-8'))
        p['shots'][1]['latentRelay']=True
        review=json.loads((ROOT/'examples/scene-change.review.json').read_text(encoding='utf-8'))
        self.assertIn('SCENE_RELAY_CONFLICT',self.codes(p,review))
    def test_meta_leak(self):
        self.plan['shots'][0]['prompt']+=' 把动作写成连续时序'
        self.assertIn('META_INSTRUCTION_LEAK',self.codes())
    def test_speaker_markup(self):
        s=self.plan['shots'][0];s['prompt']=s['prompt'].replace('[Chinese]','[Chinese][S1]')
        self.assertIn('SPEAKER_INSIDE_DIALOGUE',self.codes())
    def test_density(self):
        self.plan['shots'][0]['durationSeconds']=0.2
        self.assertIn('DIALOGUE_DENSITY',self.codes())
    def test_missing_file(self):
        self.asset();self.plan['assets'][0]['fixed']=True
        with tempfile.TemporaryDirectory() as tmp:
            self.assertIn('MISSING_ASSET_FILE',self.codes(input_root=tmp))
            (Path(tmp)/'face.png').write_bytes(b'fixture')
            self.assertNotIn('MISSING_ASSET_FILE',self.codes(input_root=tmp))
    def test_quality_never_inferred(self):
        self.assertEqual(validate(self.plan)['video_quality'],'NOT_TESTED')
    def test_reference_template_not_claimed_ready(self):
        p=json.loads((ROOT/'examples/reference-template.director.json').read_text(encoding='utf-8'))
        with tempfile.TemporaryDirectory() as tmp:
            self.assertIn('MISSING_ASSET_FILE',self.codes(p,input_root=tmp))

if __name__=='__main__':unittest.main()
