
import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from validate_plan import validate
from validate_dialogue import validate_dialogue


class V4SkillContractTests(unittest.TestCase):
    def test_skill_has_v4_discovery_and_operational_sections(self):
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("version: 4.0.0", text)
        self.assertRegex(text, r"description:\s*Use when")
        for heading in ("## 快速参考", "## 术语", "## 来源优先级", "## 交付", "## 兼容性"):
            self.assertIn(heading, text)
        for tier in ("### P0", "### P1", "### P2"):
            self.assertIn(tier, text)

    def _base_plan(self):
        return json.loads((ROOT / "examples" / "single-dialogue.director.json").read_text(encoding="utf-8"))

    def test_audio_reference_cannot_be_the_only_active_reference(self):
        p = self._base_plan()
        p["assets"] = [
            {"id":"voice","alias":"VOICE","kind":"audio","path":"voice.wav","fixed":True}
        ]
        p["shots"][0]["prompt"] = p["shots"][0]["prompt"].replace("{{ref:WOMAN_FACE}}", "")
        codes = {f["code"] for f in validate(p)["findings"]}
        self.assertIn("AUDIO_REFERENCE_REQUIRES_VISUAL_REFERENCE", codes)

    def test_ref2va_modality_limits_are_preflight_errors(self):
        p = self._base_plan()
        p["assets"] = [
            {"id":f"img{i}","alias":f"IMG{i}","kind":"image","path":f"{i}.png","fixed":True}
            for i in range(10)
        ]
        codes = {f["code"] for f in validate(p)["findings"]}
        self.assertIn("TOO_MANY_IMAGE_REFERENCES", codes)

    def test_total_reference_file_limit_is_preflight_error(self):
        p = self._base_plan()
        assets = [
            {"id":f"img{i}","alias":f"IMG{i}","kind":"image","path":f"{i}.png","fixed":True}
            for i in range(9)
        ] + [
            {"id":f"vid{i}","alias":f"VID{i}","kind":"video","path":f"{i}.mp4","fixed":True}
            for i in range(3)
        ] + [
            {"id":"aud0","alias":"AUD0","kind":"audio","path":"0.wav","fixed":True}
        ]
        p["assets"] = assets
        codes = {f["code"] for f in validate(p)["findings"]}
        self.assertIn("TOO_MANY_REFERENCE_FILES", codes)

    def test_reference_media_duration_bounds_are_errors(self):
        p = self._base_plan()
        p["assets"] = [
            {"id":"img","alias":"IMG","kind":"image","path":"a.png","fixed":True},
            {"id":"aud","alias":"AUD","kind":"audio","path":"a.wav","fixed":True,"durationSeconds":1.5}
        ]
        codes = {f["code"] for f in validate(p)["findings"]}
        self.assertIn("REFERENCE_MEDIA_DURATION", codes)

    def test_reference_media_total_duration_is_error(self):
        p = self._base_plan()
        p["assets"] = [
            {"id":"img","alias":"IMG","kind":"image","path":"a.png","fixed":True},
            {"id":"aud1","alias":"AUD1","kind":"audio","path":"1.wav","fixed":True,"durationSeconds":8},
            {"id":"aud2","alias":"AUD2","kind":"audio","path":"2.wav","fixed":True,"durationSeconds":8}
        ]
        codes = {f["code"] for f in validate(p)["findings"]}
        self.assertIn("REFERENCE_MEDIA_TOTAL_DURATION", codes)

    def test_review_schema_documents_voice_source_and_dream_speech(self):
        schema_path = ROOT / "schemas" / "review.schema.json"
        self.assertTrue(schema_path.is_file())
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        raw = json.dumps(schema, ensure_ascii=False)
        self.assertIn("voiceSourceCharacterId", raw)
        self.assertIn("dream_speech", raw)

    def test_dialogue_can_separate_owner_from_voice_source(self):
        plan = json.loads((ROOT / "examples" / "dialogue-ownership.director.json").read_text(encoding="utf-8"))
        review = json.loads((ROOT / "examples" / "dialogue-ownership.review.json").read_text(encoding="utf-8"))
        # A quoted/imitated line can be owned by CHEN but intentionally voiced by SHEN.
        line = review["shots"]["shot_001"]["dialogueLines"][0]
        line["voiceSourceCharacterId"] = "SHEN"
        review["shots"]["shot_001"]["activeSpeakerIds"] = ["SHEN"]
        review["shots"]["shot_001"]["requiredAliases"] = ["CHEN_FACE", "SHEN_VOICE"]
        shot = plan["shots"][0]
        shot["prompt"] = shot["prompt"].replace("{{ref:CHEN_VOICE}}", "{{ref:SHEN_VOICE}}")
        shot["prompt"] = shot["prompt"].replace("(S1)", "(S2)")
        report = validate_dialogue(plan, review)
        codes = {f["code"] for f in report["findings"]}
        self.assertNotIn("DIALOGUE_SPEAKER_MISMATCH", codes)
        self.assertNotIn("DIALOGUE_OWNER_NOT_ACTIVE", codes)

    def test_dream_speech_is_a_supported_delivery_mode(self):
        plan = json.loads((ROOT / "examples" / "dialogue-ownership.director.json").read_text(encoding="utf-8"))
        review = json.loads((ROOT / "examples" / "dialogue-ownership.review.json").read_text(encoding="utf-8"))
        review["shots"]["shot_003"]["dialogueLines"][0]["delivery"] = "dream_speech"
        report = validate_dialogue(plan, review)
        self.assertNotIn("UNKNOWN_DELIVERY", {f["code"] for f in report["findings"]})


if __name__ == "__main__":
    unittest.main()
