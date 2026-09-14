"""Report the user's 90% milestone without relaxing full photographic release gates."""
import json, math
from pathlib import Path
from validate_references import inspect
ROOT=Path(__file__).resolve().parents[1]
BASELINE_IDS=tuple([f'G{i:02}' for i in range(1,10)]+[f'M{i:02}' for i in range(1,12)]+['S01'])

def progress(audit,result):
    items=audit.get('items',[]);ids=[i.get('id') for i in items]
    scope_ok=len(ids)==len(set(ids)) and set(BASELINE_IDS)<=set(ids)
    denominator=len(set(BASELINE_IDS)|set(ids))
    invalid={p['id'] for p in result['unproven_matches']}
    proved={i['id'] for i in items if i.get('status')=='MATCHED' and i['id'] not in invalid}
    if not result['checks']['asset_hashes_current']:proved=set()
    required=math.ceil(denominator*.90)
    prerequisites={k:v for k,v in result['checks'].items() if k!='zero_unresolved_differences'}
    return {'baseline_ids':list(BASELINE_IDS),'scope_intact':scope_ok,
            'denominator':denominator,'proven_matches':sorted(proved),'numerator':len(proved),
            'percent':round(100*len(proved)/denominator,2),'required_matches':required,
            'remaining_to_90':max(0,required-len(proved)),
            'prerequisites':prerequisites,
            'milestone_90_pass':scope_ok and len(proved)>=required and all(prerequisites.values()),
            'full_release_accuracy_gate':result['accuracy_gate'],
            'note':'Missing/NA items remain in the baseline denominator. New independent items expand it. Runtime checks are never photographic matches.'}

def main():
    folder=ROOT/'references/sop_reaudit';audit=json.loads((folder/'audit.json').read_text())
    result=inspect(ROOT,json.loads((folder/'sources.json').read_text()),audit)
    out=progress(audit,result);dest=ROOT/'verification/sop90/progress.json';dest.parent.mkdir(exist_ok=True)
    dest.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps(out,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
