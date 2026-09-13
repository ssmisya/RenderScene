"""Install pinned official Godot and macOS export template under this project only."""
from pathlib import Path
import argparse
import hashlib
import io
import json
import subprocess
import sys
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / '.tools/godot'
LOCK = json.loads((ROOT / 'demo/engine_lock.json').read_text())


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def valid(path, expected):
    return path.is_file() and digest(path) == expected


def request(url, headers=None):
    return urllib.request.urlopen(urllib.request.Request(url, headers={
        'User-Agent': 'SophiaWalk-local-setup', **(headers or {})}), timeout=60)


class RemoteZip(io.RawIOBase):
    """Read the macOS member without downloading other platform templates."""
    def __init__(self, url):
        self.url, self.pos = url, 0
        with request(url, {'Range': 'bytes=0-0'}) as response:
            if response.status != 206:
                raise RuntimeError('Template host must support HTTP byte ranges.')
            self.size = int(response.headers['Content-Range'].split('/')[-1])

    def seek(self, offset, whence=0):
        self.pos = offset if whence == 0 else self.pos + offset if whence == 1 else self.size + offset
        return self.pos

    def tell(self):
        return self.pos

    def read(self, count=-1):
        end = self.size if count < 0 else min(self.size, self.pos + count)
        if end <= self.pos:
            return b''
        with request(self.url, {'Range': f'bytes={self.pos}-{end - 1}'}) as response:
            if response.status != 206:
                raise RuntimeError('Server stopped supporting partial downloads.')
            data = response.read(end - self.pos)
        if len(data) != end - self.pos:
            raise IOError('Incomplete template range; rerun setup.')
        self.pos = end
        return data


def install():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify-only', action='store_true')
    args = parser.parse_args()
    if sys.platform != 'darwin':
        raise SystemExit('This installer targets macOS. Import demo/project.godot in Godot 4.7.2 on other platforms.')
    DEST.mkdir(parents=True, exist_ok=True)
    archive, template = DEST / 'godot.zip', DEST / 'macos.zip'
    engine = DEST / 'Godot.app/Contents/MacOS/Godot'
    if args.verify_only:
        assert valid(archive, LOCK['editor_zip_sha256']), 'Editor archive hash mismatch/missing'
        assert valid(template, LOCK['macos_template_zip_sha256']), 'macOS template hash mismatch/missing'
        assert engine.is_file(), 'Editor executable missing'
    else:
        if not valid(archive, LOCK['editor_zip_sha256']):
            print('Downloading pinned official Godot editor…', flush=True)
            partial = archive.with_suffix('.partial')
            with request(LOCK['editor_source']) as source, partial.open('wb') as output:
                while chunk := source.read(1024 * 1024):
                    output.write(chunk)
            assert valid(partial, LOCK['editor_zip_sha256']), 'Editor download SHA-256 mismatch'
            partial.replace(archive)
            subprocess.run(['ditto', '-x', '-k', str(archive), str(DEST)], cwd=ROOT, check=True)
        elif not engine.is_file():
            subprocess.run(['ditto', '-x', '-k', str(archive), str(DEST)], cwd=ROOT, check=True)
        if not valid(template, LOCK['macos_template_zip_sha256']):
            print('Downloading macOS template only; verifying ZIP CRC and SHA-256…', flush=True)
            with zipfile.ZipFile(RemoteZip(LOCK['template_source'])) as bundle:
                data = bundle.read('templates/macos.zip')
            assert hashlib.sha256(data).hexdigest() == LOCK['macos_template_zip_sha256'], 'Template SHA-256 mismatch'
            partial = template.with_suffix('.partial')
            partial.write_bytes(data)
            partial.replace(template)
    version = subprocess.check_output([str(engine), '--version'], cwd=ROOT, text=True).strip()
    assert version.startswith(LOCK['version'].replace('-', '.', 1)), version
    print('GODOT_LOCAL_SETUP_VERIFIED', version, flush=True)


if __name__ == '__main__':
    install()
