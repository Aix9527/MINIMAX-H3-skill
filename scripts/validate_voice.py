"""Check declared voice routing, not perceptual speaker similarity."""
import argparse
import json
import re
from pathlib import Path
from validate_plan import validate

def validate_voices(plan, review, input_root=None, theodore_root=None):
    report=validate(plan,input_root,theodore_root,review)
    findings=report['findings']
    def add(level,code,shot,detail):
        findings.append(dict(level=level,code=code,shot=shot,detail=detail))
    voices=review.get('voices',{})
    if not isinstance(voices,dict):
        raise ValueError('voices must map character IDs to voice profiles')
    assets={a['alias']:a for a in plan.get('assets',[])}
    speakers={};shared={}
    for char,v in voices.items():
        sid=v.get('speakerId','');alias=v.get('voiceAlias','')
        if not re.fullmatch(r'S[1-9]\d*',sid):add('error','INVALID_SPEAKER_ID',None,char)
        if sid in speakers:add('error','DUPLICATE_SPEAKER_ID',None,char)
        speakers[sid]=char
        if alias in shared and not v.get('sharedVoiceReason'):
            add('warning','SHARED_VOICE_REFERENCE',None,f'{char} and {shared[alias]} share {alias}')
        shared[alias]=char
        a=assets.get(alias.removesuffix('.audio'))
        valid=a and ((alias.endswith('.audio') and a.get('kind')=='video' and a.get('includeVideoAudio')) or (not alias.endswith('.audio') and a.get('kind')=='audio'))
        if not valid:add('error','INVALID_VOICE_ASSET',None,f'{char}: {alias}')
    rows={s['id']:s for s in report['shots']}
    for s in plan['shots']:
        if not s.get('enabled',True):continue
        sid=s['id'];exp=review.get('shots',{}).get(sid,{})
        active=exp.get('activeSpeakerIds')
        text='\n'.join([plan.get('promptPrefix',''),s.get('prompt',''),plan.get('promptSuffix','')])
        if '<d>' in text and not active:add('warning','SPEAKER_OWNERSHIP_UNDECLARED',sid,'Declare current speaking character IDs')
        aliases=rows.get(sid,{}).get('activeAliases',[])
        for char in active or []:
            if char not in voices:
                add('error','UNREGISTERED_SPEAKER',sid,char);continue
            v=voices[char];alias=v['voiceAlias'];base=alias.removesuffix('.audio')
            # Native resolver reports paired-video aliases by base name; static mode does too.
            if base not in aliases:add('error','VOICE_REFERENCE_NOT_ACTIVE',sid,alias)
            if f"({v['speakerId']})" not in text:add('error','SPEAKER_TAG_MISSING',sid,v['speakerId'])
        for char,v in voices.items():
            if v.get('voiceAlias','').removesuffix('.audio') in aliases and char not in (active or []):
                add('warning','INACTIVE_SPEAKER_VOICE',sid,char)
    report['status']='FAIL' if any(f['level']=='error' for f in findings) else 'REVIEW' if findings else 'PASS'
    report['audioListening']='NOT_TESTED'
    return report

def main():
    p=argparse.ArgumentParser();p.add_argument('plan',type=Path);p.add_argument('--review',required=True,type=Path);p.add_argument('--input-root',type=Path);p.add_argument('--theodore-root',type=Path);p.add_argument('--output',type=Path)
    a=p.parse_args()
    try:
        report=validate_voices(json.loads(a.plan.read_text(encoding='utf-8-sig')),json.loads(a.review.read_text(encoding='utf-8-sig')),a.input_root,a.theodore_root)
    except (ValueError,TypeError,KeyError,ImportError,OSError) as e:
        report=dict(status='FAIL',findings=[dict(level='error',code='VALIDATION_ABORTED',detail=str(e))],audioListening='NOT_TESTED')
    text=json.dumps(report,ensure_ascii=False,indent=2)
    if a.output:a.output.write_text(text,encoding='utf-8')
    print(text);return int(report['status']=='FAIL')

if __name__=='__main__':raise SystemExit(main())
