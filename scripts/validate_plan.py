"""Read-only director preflight. Uses the installed Theodore parser when supplied."""
import argparse
import json
import re
import sys
from pathlib import Path

TOKEN = re.compile(r'\{\{ref:([^{}]+)}}')
META = re.compile(r'把动作写成|准备姿态\s*[→]|ACTIVE_SPEAKER\s*=|MUTE_LISTENER\s*[:=]|SCENE_LOCK\s*=')

def validate(data, input_root=None, theodore_root=None, review=None):
    findings = []
    rows = []
    def add(level, code, shot, detail):
        findings.append(dict(level=level, code=code, shot=shot, detail=detail))
    if not isinstance(data, dict) or not isinstance(data.get('shots'), list):
        return {'status':'FAIL', 'findings':[{'level':'error','code':'INVALID_PLAN','detail':'shots must be a list'}], 'shots':[], 'video_quality':'NOT_TESTED'}
    assets = data.get('assets', [])
    if not isinstance(assets,list) or any(not isinstance(a,dict) for a in assets):
        return {'status':'FAIL','findings':[{'level':'error','code':'INVALID_ASSETS'}],'shots':[],'video_quality':'NOT_TESTED'}
    aliases = [a.get('alias') for a in assets]
    asset_by_alias = {a.get('alias'): a for a in assets if a.get('alias')}
    if len(aliases)!=len(set(aliases)):
        add('error','DUPLICATE_ALIAS',None,'Asset aliases must be unique')
    native = None
    if theodore_root:
        sys.path.insert(0,str(Path(theodore_root)))
        from theodore_director.schema import load_plan
        from theodore_director.references import resolve_references
        native = load_plan(json.dumps(data,ensure_ascii=False))
    else:
        add('warning','NATIVE_RUNTIME_NOT_CHECKED',None,'Supply --theodore-root for actual installed reference resolution')
    if input_root is None:
        add('warning','ASSET_FILES_NOT_CHECKED',None,'Supply --input-root for file existence checks')
    seen = set()
    previous_scene = None
    expectations = (review or {}).get('shots',{})
    for index, s in enumerate(data['shots']):
        if not isinstance(s,dict):
            add('error','INVALID_SHOT',index,'Shot must be an object'); continue
        sid=s.get('id')
        if not isinstance(sid,str) or not sid or sid in seen:
            add('error','INVALID_SHOT_ID',sid,'Missing or duplicate id')
        seen.add(sid)
        if not s.get('enabled',True): continue
        duration=s.get('durationSeconds')
        if type(duration) not in (int,float) or not 0 < duration < float('inf'):
            add('error','INVALID_DURATION',sid,'Duration must be finite and positive');duration=0
        text='\n'.join(str(x) for x in (data.get('promptPrefix',''),s.get('prompt',''),data.get('promptSuffix','')) if x)
        if META.search(text):add('error','META_INSTRUCTION_LEAK',sid,'Internal planning instruction in runtime prompt')
        if re.search(r'<d>\[\w+\]\s*[\[(]S\d',text):add('error','SPEAKER_INSIDE_DIALOGUE',sid,'Keep speaker IDs outside <d>')
        if text.count('<d>')!=text.count('</d>'):add('error','DIALOGUE_TAGS',sid,'Unbalanced dialogue tags')
        required=['subject_definitions:','summary:','retention_analysis:','detailed_description:','overall_soundscape:','non_diegetic_music:'] if 'subject_definitions:' in text else ['integrated_multimodal_description:','overall_soundscape:','non_diegetic_music:']
        positions=[text.find(k) for k in required]
        if -1 in positions or positions!=sorted(positions):add('error','PROMPT_SECTIONS',sid,'Missing or unordered H3 sections')
        eligible={a.get('alias'):a for a in assets if a.get('enabled',True) and (not a.get('shotIds') or sid in a['shotIds']) and a.get('id') not in s.get('disabledAssetIds',[])}
        used={a.get('alias'):a for a in eligible.values() if a.get('fixed',False)}
        for alias in TOKEN.findall(text):
            key=alias.removesuffix('.audio')
            if key not in eligible:add('error','UNRESOLVED_REFERENCE',sid,alias)
            else:used[key]=eligible[key]
        if native:
            resolved=resolve_references(native,native.shots[index])
            used={}
            for a in (*resolved.pictures,*resolved.videos,*resolved.standalone_audio,*resolved.paired_audio):
                row=dict(alias=a.alias,path=a.path,kind=a.kind.value)
                source=asset_by_alias.get(a.alias,{})
                for key in ('durationSeconds','audioDurationSeconds','includeVideoAudio'):
                    if key in source:
                        row[key]=source[key]
                used[a.alias]=row

        # H3 Ref2VA public input limits. These checks use the active request,
        # not the whole imported asset catalog.
        active=list(used.values())
        image_count=sum(a.get('kind')=='image' for a in active)
        video_count=sum(a.get('kind')=='video' for a in active)
        audio_count=sum(a.get('kind')=='audio' for a in active)
        if image_count>9:add('error','TOO_MANY_IMAGE_REFERENCES',sid,f'{image_count} active images; H3 Ref2VA supports at most 9')
        if video_count>3:add('error','TOO_MANY_VIDEO_REFERENCES',sid,f'{video_count} active videos; H3 Ref2VA supports at most 3')
        if audio_count>3:add('error','TOO_MANY_AUDIO_REFERENCES',sid,f'{audio_count} active audio clips; H3 Ref2VA supports at most 3')
        if len(active)>12:add('error','TOO_MANY_REFERENCE_FILES',sid,f'{len(active)} active reference files; H3 Ref2VA supports at most 12 mixed files')
        if audio_count and not (image_count or video_count):
            add('error','AUDIO_REFERENCE_REQUIRES_VISUAL_REFERENCE',sid,'Standalone audio reference requires at least one image or video reference')

        video_durations=[a.get('durationSeconds') for a in active if a.get('kind')=='video' and isinstance(a.get('durationSeconds'),(int,float))]
        audio_durations=[a.get('audioDurationSeconds',a.get('durationSeconds')) for a in active if a.get('kind')=='audio' and isinstance(a.get('audioDurationSeconds',a.get('durationSeconds')),(int,float))]
        for duration_value in video_durations:
            if not 2<=duration_value<=15:add('error','REFERENCE_MEDIA_DURATION',sid,f'video reference duration {duration_value}s must be 2-15s')
        for duration_value in audio_durations:
            if not 2<=duration_value<=15:add('error','REFERENCE_MEDIA_DURATION',sid,f'audio reference duration {duration_value}s must be 2-15s')
        if sum(video_durations)>15:add('error','REFERENCE_MEDIA_TOTAL_DURATION',sid,f'active video references total {sum(video_durations):g}s; maximum is 15s')
        if sum(audio_durations)>15:add('error','REFERENCE_MEDIA_TOTAL_DURATION',sid,f'active audio references total {sum(audio_durations):g}s; maximum is 15s')

        exp=expectations.get(sid,{})
        for alias in exp.get('requiredAliases',[]):
            if alias not in used:add('error','EXPECTED_REFERENCE_NOT_ACTIVE',sid,alias)
        if assets and not used:add('warning','CATALOG_WITH_ZERO_ACTIVE_REFERENCES',sid,'Library is populated but this shot uses no references; verify intended mode')
        scene=exp.get('sceneId')
        if s.get('latentRelay',False) and (index==0 or (scene and previous_scene and scene!=previous_scene)):
            add('error','SCENE_RELAY_CONFLICT',sid,'First shot or scene change inherits previous context')
        previous_scene=scene
        if s.get('latentRelay',False) and not scene:add('warning','RELAY_SCENE_UNVERIFIED',sid,'Provide review sceneId and inspect accepted prior clip')
        if input_root:
            for a in used.values():
                p=Path(a.get('path',''));p=p if p.is_absolute() else Path(input_root)/p
                if not a.get('path') or not p.is_file():add('error','MISSING_ASSET_FILE',sid,str(p))
        words=''.join(re.findall(r'<d>(.*?)</d>',text,re.S))
        count=len(re.findall(r'[\u4e00-\u9fff]',words))
        speech_seconds=exp.get('speechSeconds',duration)
        if type(speech_seconds) not in (int,float) or not 0 < speech_seconds <= duration:
            add('error','INVALID_SPEECH_WINDOW',sid,'speechSeconds must be positive and within clip duration');speech_seconds=duration
        density=count/speech_seconds if speech_seconds else 0
        if density>5:add('warning','DIALOGUE_DENSITY',sid,f'{density:.2f} Han chars/s; read aloud and allow pauses, heuristic only')
        rows.append(dict(id=sid,activeAliases=list(used),imageCount=image_count,videoCount=video_count,audioCount=audio_count,referenceFileCount=len(active),hanCharsPerSecond=round(density,2)))
    return dict(status='FAIL' if any(f['level']=='error' for f in findings) else 'REVIEW' if findings else 'PASS',findings=findings,shots=rows,reference_check='native' if native else 'static',video_quality='NOT_TESTED')

def main():
    p=argparse.ArgumentParser();p.add_argument('plan',type=Path);p.add_argument('--input-root',type=Path);p.add_argument('--theodore-root',type=Path);p.add_argument('--review',type=Path);p.add_argument('--output',type=Path)
    args=p.parse_args()
    try:
        report=validate(json.loads(args.plan.read_text(encoding='utf-8-sig')),args.input_root,args.theodore_root,json.loads(args.review.read_text(encoding='utf-8-sig')) if args.review else None)
    except (ValueError,TypeError,KeyError,ImportError,OSError) as e:
        report=dict(status='FAIL',findings=[dict(level='error',code='VALIDATION_ABORTED',detail=str(e))],video_quality='NOT_TESTED')
    result=json.dumps(report,ensure_ascii=False,indent=2)
    if args.output:args.output.write_text(result,encoding='utf-8')
    print(result);return 1 if report['status']=='FAIL' else 0

if __name__=='__main__':sys.exit(main())
