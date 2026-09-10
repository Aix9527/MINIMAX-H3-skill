"""Compare runtime dialogue with a declared line ledger; does not inspect video."""
import argparse
import json
import re
from pathlib import Path
from validate_voice import validate_voices

LINE=re.compile(r'<d>\[([^\]]+)\](.*?)</d>',re.S)

def validate_dialogue(plan,review,input_root=None,theodore_root=None):
    report=validate_voices(plan,review,input_root,theodore_root)
    def add(level,code,sid,detail):
        report['findings'].append(dict(level=level,code=code,shot=sid,detail=detail))
    ids=set()
    for shot in plan['shots']:
        if not shot.get('enabled',True):continue
        sid=shot['id'];expect=review.get('shots',{}).get(sid,{})
        text='\n'.join([plan.get('promptPrefix',''),shot.get('prompt',''),plan.get('promptSuffix','')])
        actual=list(LINE.finditer(text));ledger=expect.get('dialogueLines')
        if ledger is None:
            if actual:add('warning','DIALOGUE_LEDGER_MISSING',sid,'Ownership and verbatim text not checked')
            continue
        if not isinstance(ledger,list):raise ValueError('dialogueLines must be a list')
        if len(actual)!=len(ledger):add('error','DIALOGUE_COUNT_MISMATCH',sid,f'expected {len(ledger)}, found {len(actual)}')
        for index,entry in enumerate(ledger):
            lineid=entry.get('lineId')
            if not lineid or lineid in ids:add('error','DIALOGUE_LINE_ID',sid,str(lineid))
            ids.add(lineid)
            char=entry.get('characterId')
            voice_char=entry.get('voiceSourceCharacterId') or char
            owner_voice=review.get('voices',{}).get(char)
            voice=review.get('voices',{}).get(voice_char)
            if not owner_voice and not entry.get('voiceSourceCharacterId'):
                add('error','DIALOGUE_OWNER_UNREGISTERED',sid,str(char));continue
            if not voice:
                add('error','DIALOGUE_VOICE_SOURCE_UNREGISTERED',sid,str(voice_char));continue
            if voice_char not in expect.get('activeSpeakerIds',[]):
                add('error','DIALOGUE_OWNER_NOT_ACTIVE',sid,voice_char)
            delivery=entry.get('delivery')
            if delivery not in ('onscreen','offscreen','inner','narration','dream_speech'):
                add('error','UNKNOWN_DELIVERY',sid,str(delivery))
            if delivery in ('onscreen','dream_speech') and voice_char not in expect.get('visibleCharacterIds',[]):
                add('error','ONSCREEN_SPEAKER_NOT_VISIBLE',sid,voice_char)
            if index>=len(actual):continue
            match=actual[index]
            if match[1]!=entry.get('language'):add('error','DIALOGUE_LANGUAGE_MISMATCH',sid,str(lineid))
            if match[2].strip()!=entry.get('text','').strip():add('error','DIALOGUE_TEXT_CHANGED',sid,str(lineid))
            start=actual[index-1].end() if index else 0
            prefix=text[start:match.start()]
            labels=list(re.finditer(r'\((S[1-9]\d*)\)',prefix))
            if not labels or labels[-1][1]!=voice['speakerId']:
                add('error','DIALOGUE_SPEAKER_MISMATCH',sid,str(lineid))
            local=prefix[labels[-1].start():] if labels else prefix
            if delivery in ('inner','narration') and 'says in an off-screen voiceover' not in local:
                add('error','VOICEOVER_DELIVERY_MISSING',sid,str(lineid))
    report['status']='FAIL' if any(x['level']=='error' for x in report['findings']) else 'REVIEW' if report['findings'] else 'PASS'
    report['lipSyncReview']='NOT_TESTED'
    return report

def main():
    parser=argparse.ArgumentParser();parser.add_argument('plan',type=Path);parser.add_argument('--review',required=True,type=Path);parser.add_argument('--input-root',type=Path);parser.add_argument('--theodore-root',type=Path);parser.add_argument('--output',type=Path)
    a=parser.parse_args()
    try:
        report=validate_dialogue(json.loads(a.plan.read_text(encoding='utf-8-sig')),json.loads(a.review.read_text(encoding='utf-8-sig')),a.input_root,a.theodore_root)
    except (ValueError,TypeError,KeyError,ImportError,OSError) as e:
        report=dict(status='FAIL',findings=[dict(level='error',code='VALIDATION_ABORTED',detail=str(e))],audioListening='NOT_TESTED',lipSyncReview='NOT_TESTED')
    text=json.dumps(report,ensure_ascii=False,indent=2)
    if a.output:a.output.write_text(text,encoding='utf-8')
    print(text);return int(report['status']=='FAIL')

if __name__=='__main__':raise SystemExit(main())
