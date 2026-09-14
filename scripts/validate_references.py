"""Evidence gate: fail on missing files, incomplete coverage, stale assets or open defects.
This validates the evidence record; it cannot turn a human visual assertion into truth.
"""
import argparse
import datetime as dt
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUSES = {'MATCHED', 'MISMATCH', 'UNVERIFIED', 'NOT_APPLICABLE'}

def sha(path):
    with path.open('rb') as f:
        h = hashlib.sha256()
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
        return h.hexdigest()

def local_file(root, value):
    if not isinstance(value, str) or not value:
        return None
    p = (root / value).resolve()
    return p if p.is_relative_to(root.resolve()) and p.is_file() else None

def bound_file(root, record):
    if not isinstance(record, dict):
        return False
    p = local_file(root, record.get('file'))
    return bool(p and record.get('sha256') == sha(p))

def capture_start(photo):
    date = photo.get('capture_date')
    if not isinstance(date, str):
        return None
    try:
        if len(date) == 4:
            return dt.date.fromisoformat(date + '-01-01')
        if len(date) == 7:
            return dt.date.fromisoformat(date + '-01')
        return dt.date.fromisoformat(date)
    except ValueError:
        return None

def inspect(root, photos, audit, today=None):
    today = today or dt.date.today()
    try:
        cutoff = today.replace(year=today.year - 2)
    except ValueError:
        cutoff = today.replace(year=today.year - 2, day=28)
    eligible, rejected, integrity, groups = [], [], [], set()
    seen_ids, seen_hashes, seen_originals = set(), set(), set()
    photo_by_id = {}
    for p in photos:
        reasons = []
        pid = p.get('id')
        if not pid or pid in seen_ids:
            reasons.append('missing or duplicate photo id')
        seen_ids.add(pid)
        photo_by_id[pid] = p
        path = local_file(root, p.get('file'))
        digest = p.get('sha256')
        if not path:
            integrity.append({'id': pid, 'reason': 'original reference file missing'})
            reasons.append('original reference file missing')
        elif not digest or sha(path) != digest:
            integrity.append({'id': pid, 'reason': 'reference hash mismatch'})
            reasons.append('reference hash mismatch')
        if digest in seen_hashes:
            reasons.append('duplicate image bytes')
        seen_hashes.add(digest)
        original = p.get('original_photo_id')
        if not original or original in seen_originals:
            reasons.append('missing or duplicate original-photo identity')
        seen_originals.add(original)
        if p.get('dedup_review') != 'DISTINCT':
            reasons.append('crop/repost duplication review incomplete')
        start = capture_start(p)
        if start is None:
            reasons.append('capture date unconfirmed')
        elif not cutoff <= start <= today:
            reasons.append('outside recent 24-month window')
        basis = p.get('date_evidence', {})
        if not isinstance(basis, dict) or basis.get('kind') not in {'capture_caption', 'exif_original', 'dated_visit'} or not basis.get('detail') or not bound_file(root, basis):
            reasons.append('capture-date evidence missing or unbound')
        if p.get('reviewed') is not True or p.get('usable_for_architecture') is not True:
            reasons.append('not reviewed or outside architecture scope')
        for key in ['source_url', 'image_url', 'author', 'source_group', 'download_date', 'position_orientation', 'coverage', 'observations', 'license']:
            if not p.get(key):
                reasons.append('missing metadata: ' + key)
        dims = p.get('dimensions')
        if not isinstance(dims, list) or len(dims) != 2 or any(not isinstance(x, int) or x <= 0 for x in dims):
            reasons.append('invalid source dimensions')
        elif path:
            try:
                from PIL import Image
                with Image.open(path) as im:
                    if list(im.size) != dims:
                        reasons.append('source dimensions mismatch')
            except Exception:
                reasons.append('source image cannot be decoded')
        if reasons:
            rejected.append({'id': pid, 'reasons': reasons})
        else:
            eligible.append(pid)
            groups.add(p['source_group'])
    eligible_set = set(eligible)
    coverage = audit.get('coverage', [])
    coverage_gaps = []
    for c in coverage:
        refs = c.get('photo_ids', [])
        if not refs or not any(pid in eligible_set and c.get('id') in photo_by_id[pid].get('coverage', []) for pid in refs):
            coverage_gaps.append(c.get('id', 'unnamed coverage'))
    items = audit.get('items', [])
    open_items, unproven = [], []
    assets = audit.get('assets', {})
    assets_ok = bool(assets) and all(local_file(root, f) and sha(root / f) == h for f, h in assets.items())
    for item in items:
        iid, status = item.get('id'), item.get('status')
        if status not in STATUSES or status in {'UNVERIFIED', 'MISMATCH'}:
            open_items.append(iid)
        if status == 'NOT_APPLICABLE' and not item.get('scope_reason'):
            unproven.append({'id': iid, 'reason': 'no exclusion rationale'})
        if status != 'MATCHED':
            continue
        comparisons = item.get('comparisons', [])
        if not item.get('photo_ids') or not comparisons:
            unproven.append({'id': iid, 'reason': 'missing photo-linked comparisons'})
        for comp in comparisons:
            valid = (comp.get('photo_id') in eligible_set and comp.get('photo_id') in item.get('photo_ids', [])
                     and comp.get('visual_result') == 'MATCHED' and bool(comp.get('visible_features'))
                     and all(bound_file(root, comp.get(k)) for k in ['render', 'camera', 'comparison']))
            if valid:
                try:
                    camera = json.loads((root / comp['camera']['file']).read_text())
                    valid = (camera.get('assets') == assets and assets_ok and
                             all(camera.get(k) is not None for k in ['position', 'rotation', 'lens_mm', 'resolution']))
                except (ValueError, OSError):
                    valid = False
            pts = comp.get('landmarks', [])
            # Corresponding visible feature locations are normalized to each whole image.
            if len(pts) < 6 or len({p.get('feature') for p in pts}) != len(pts):
                valid = False
            # Six labels at one point or on one line are not a camera calibration.
            for space in ['photo', 'render']:
                coords = [p.get(space) for p in pts]
                if all(isinstance(p, list) and len(p) == 2 and all(isinstance(v, (int, float)) and math.isfinite(v) for v in p) for p in coords):
                    areas = [abs((b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0]))
                             for a in coords for b in coords for c in coords]
                    if not areas or max(areas) < .01:
                        valid = False
                else:
                    valid = False
            for pair in pts:
                a, b = pair.get('photo'), pair.get('render')
                if not a or not b or len(a) != 2 or len(b) != 2 or any(not isinstance(v, (int, float)) or not math.isfinite(v) or not 0 <= v <= 1 for v in a + b):
                    valid = False
                    continue
                width, height = photo_by_id.get(comp.get('photo_id'), {}).get('dimensions', [1, 1])
                error = math.hypot((a[0]-b[0])*width, (a[1]-b[1])*height) / math.hypot(width,height)
                if error > .01:
                    valid = False
            if not valid:
                unproven.append({'id': iid, 'reason': 'invalid camera/render/landmark proof'})
    compared = {c.get('photo_id') for i in items if i.get('status') == 'MATCHED' for c in i.get('comparisons', [])}
    checks = {
        'schema_v2': audit.get('schema_version') == 2,
        'scope_locked': bool(audit.get('scope')) and bool(audit.get('target_epoch')),
        'ten_recent_distinct_photos': len(eligible) >= 10,
        'three_independent_sources': len(groups) >= 3,
        'source_integrity': not integrity,
        'coverage_complete': bool(coverage) and not coverage_gaps and audit.get('coverage_complete') is True,
        'nonempty_detail_inventory': bool(items),
        'zero_unresolved_differences': not open_items,
        'matches_have_evidence': not unproven,
        'every_eligible_photo_compared': bool(eligible) and eligible_set <= compared,
        'asset_hashes_current': assets_ok,
        'current_epoch_verified': audit.get('current_epoch_verified') is True,
        'no_time_conflicts': audit.get('time_conflicts') == [],
    }
    return {'review_date': str(today), 'recorded_review_date': audit.get('review_date'),
            'reviewed_photos': sum(p.get('reviewed') is True for p in photos),
            'eligible_recent_photos': eligible, 'rejected': rejected, 'source_groups': sorted(groups),
            'integrity_errors': integrity, 'coverage_gaps': coverage_gaps,
            'open_items': open_items, 'unproven_matches': unproven, 'checks': checks,
            'accuracy_gate': 'PASS' if all(checks.values()) else 'NOT_ACCEPTED',
            'note': 'Record integrity and stated observations are checked; passing is not a survey certificate.'}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--batch')
    parser.add_argument('--strict', action='store_true')
    args = parser.parse_args()
    batch = args.batch
    if batch is None:
        batch = json.loads((ROOT / 'ACTIVE_REVIEW.json').read_text())['batch']
    if Path(batch).name != batch:
        parser.error('batch must be a single directory name')
    folder = ROOT / 'references' / batch
    result = inspect(ROOT, json.loads((folder / 'sources.json').read_text()), json.loads((folder / 'audit.json').read_text()))
    out = ROOT / 'verification' / batch / 'reference_validation.json'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if args.strict and result['accuracy_gate'] != 'PASS':
        raise SystemExit(2)

if __name__ == '__main__':
    main()
