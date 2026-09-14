"""Single entry for validating the active reconstruction before a distributable build."""
import json
from pathlib import Path
from validate_references import inspect, local_file, sha
ROOT = Path(__file__).resolve().parents[1]

def check_release(root=ROOT):
    active = json.loads((root / 'ACTIVE_REVIEW.json').read_text())
    batch = active['batch']
    if Path(batch).name != batch:
        raise ValueError('Invalid active review batch')
    folder = root / 'references' / batch
    audit = json.loads((folder / 'audit.json').read_text())
    result = inspect(root, json.loads((folder / 'sources.json').read_text()), audit)
    failures = [key for key, ok in result['checks'].items() if not ok]
    if active.get('status') != 'ACCEPTED' or active.get('release_allowed') is not True:
        failures.append('active_review_not_accepted')
    for key in ['runtime_report', 'blender_report']:
        record = audit.get(key, {})
        path = local_file(root, record.get('file'))
        if not path or sha(path) != record.get('sha256'):
            failures.append(key + '_missing_or_changed')
            continue
        data = json.loads(path.read_text())
        individual = data.get('checks', {})
        checks_pass = bool(individual) and all(v is True for v in individual.values())
        if key == 'runtime_report':
            current = data.get('assets') == audit.get('assets')
            if not current or data.get('all_checks_pass') is not True or not checks_pass:
                failures.append(key + '_not_passed_for_current_assets')
            if data.get('exported_application') is not True:
                failures.append('independent_application_not_tested')
        else:
            # Native validator binds the source .blend, before engine export exists.
            source_hash = audit.get('assets', {}).get('Harbin_Sophia_Square.blend')
            current = bool(source_hash) and data.get('source_scene_sha256') == source_hash
            if not current or not checks_pass or data.get('scene_checks', {}).get('errors') != []:
                failures.append(key + '_not_passed_for_current_assets')
    return failures

def require_release(root=ROOT):
    failures = check_release(root)
    if failures:
        raise SystemExit('RELEASE BLOCKED: ' + ', '.join(failures))

if __name__ == '__main__':
    require_release()
    print('RELEASE_GATE_PASS')
