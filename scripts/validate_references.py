"""Fail closed on missing evidence. Photo count is not a visual accuracy score."""
import json,datetime,hashlib,argparse
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--strict',action='store_true');args=p.parse_args()
R=Path(__file__).resolve().parents[1];D=R/'references/v2_2'
photos=json.loads((D/'sources.json').read_text());audit=json.loads((D/'audit.json').read_text())
now=datetime.date.fromisoformat(audit['review_date']);eligible=[];rejected=[];hashes=set();sources=set();integrity=[]
for x in photos:
 reasons=[];date=x.get('capture_date');oldest=None
 if date:
  try:oldest=datetime.date.fromisoformat(date if len(date)==10 else date+'-01-01')
  except ValueError:pass
 if oldest is None:reasons.append('capture date unconfirmed')
 elif not 0<=(now-oldest).days<=731:reasons.append('outside recent 24-month window')
 if not x.get('reviewed'):reasons.append('not visually reviewed')
 if not x.get('usable_for_architecture'):reasons.append('insufficient architectural detail / wrong scope')
 digest=x.get('sha256')
 if not digest:reasons.append('missing original hash')
 elif digest in hashes:reasons.append('duplicate source image')
 else:hashes.add(digest)
 local=R/x['file']
 if local.exists() and digest and hashlib.sha256(local.read_bytes()).hexdigest()!=digest:integrity.append(x['id'])
 if reasons:rejected.append({'id':x['id'],'reasons':reasons})
 else:eligible.append(x['id']);sources.add(x.get('source_group',x['author']))
open_items=[x['id'] for x in audit['items'] if x['status'] not in ['MATCHED','NOT_APPLICABLE']]
unproven=[x['id'] for x in audit['items'] if x['status']=='MATCHED' and not x.get('comparison_evidence')]
checks={'ten_recent_distinct_photos':len(eligible)>=10,'three_independent_sources':len(sources)>=3,'source_integrity':not integrity,'coverage_complete':audit['coverage_complete'],'zero_unresolved_differences':not open_items,'matches_have_evidence':not unproven,'current_epoch_verified':audit['current_epoch_verified']}
out={'review_date':str(now),'reviewed_photos':sum(bool(x.get('reviewed')) for x in photos),'eligible_recent_photos':eligible,'rejected':rejected,'source_groups':sorted(sources),'checks':checks,'open_items':open_items,'accuracy_gate':'PASS' if all(checks.values()) else 'NOT_ACCEPTED','note':'A count check does not certify pixel, dimensional or photogrammetric accuracy.'}
(R/'verification/v2_2/reference_validation.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps(out,ensure_ascii=False,indent=2))
if args.strict and not all(checks.values()):raise SystemExit(2)
