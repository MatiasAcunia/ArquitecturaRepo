#!/usr/bin/env python3
"""ArquitecturaRepo <-> Codex Daily Control 2.0.2/2.1 read-only preflight adapter.

Read-only physical-byte inspection. No native Codex API calls, network,
PowerShell invocation, Goal mutation, journal repair, or package installation.
A passing package inspection NEVER grants Goal execution or release authority.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import stat
import sys
import zipfile
import zlib
from pathlib import Path, PurePosixPath
from typing import Protocol

SCHEMA = 'codex-daily-control-package-preflight-v1'
MANIFEST = 'SOURCE_SHA256SUMS.txt'
REQUIRED = (
    'VERSION.txt', 'release.json', 'config/slots.json', MANIFEST,
    'bin/codex-daily-control.ps1', 'bin/install.ps1',
    'src/CodexDailyControl/CodexDailyControl.psd1',
    'src/CodexDailyControl/Private/91-V2Close.ps1',
    'src/CodexDailyControl/Private/60-Goals.ps1',
    'src/CodexDailyControl/Private/50-AppServer.ps1',
)
MAX_FILES = 1000
MAX_TOTAL_BYTES = 60 * 1024 * 1024
MAX_ENTRY_BYTES = 12 * 1024 * 1024
SHA_RE = re.compile(r'^[0-9a-f]{64}$')
MANIFEST_LINE = re.compile(r'^([0-9a-f]{64})  ([^\r\n]+)$')


class Hold(ValueError):
    pass


class Source(Protocol):
    def names(self) -> set[str]: ...
    def read(self, relative: str) -> bytes: ...


def relative(name: str) -> str:
    if not name or '\\' in name or '\x00' in name or ':' in name:
        raise Hold('UNSAFE_PACKAGE_PATH')
    p = PurePosixPath(name)
    parts = name.split('/')
    reserved = {'CON', 'PRN', 'AUX', 'NUL',
                *(f'COM{i}' for i in range(1, 10)),
                *(f'LPT{i}' for i in range(1, 10))}
    if (p.is_absolute() or any(x in ('.', '..', '') for x in parts) or
        any(x.rstrip(' .') != x or x.split('.', 1)[0].upper() in reserved for x in parts)):
        raise Hold('UNSAFE_PACKAGE_PATH')
    return name


class ZipSource:
    def __init__(self, source: Path):
        self.z = zipfile.ZipFile(source)
        try:
            objects = self.z.infolist()
            if len(objects) > MAX_FILES or sum(x.file_size for x in objects) > MAX_TOTAL_BYTES:
                raise Hold('PACKAGE_SIZE_LIMIT')
            names = [x.filename for x in objects if not x.is_dir()]
            for x in objects:
                mode = (x.external_attr >> 16) & 0xffff
                kind = stat.S_IFMT(mode)
                if (x.file_size > MAX_ENTRY_BYTES or
                    kind not in {0, stat.S_IFREG, stat.S_IFDIR}):
                    raise Hold('PACKAGE_ENTRY_UNTRUSTED')
                if not x.is_dir():
                    relative(x.filename)
            parts = {x.split('/')[0] for x in names}
            if len(parts) != 1 or not names or any(len(x.split('/')) < 2 for x in names):
                raise Hold('PACKAGE_ROOT_INVALID')
            if len({x.casefold() for x in names}) != len(names):
                raise Hold('PACKAGE_PATH_CASE_COLLISION')
            prefix = next(iter(parts)) + '/'
            self._map = {x[len(prefix):]: x for x in names}
            if (len(self._map) != len(names) or
                len({x.casefold() for x in self._map}) != len(self._map)):
                raise Hold('PACKAGE_DUPLICATE_PATHS')
        except BaseException:
            self.z.close()
            raise

    def names(self) -> set[str]:
        return set(self._map)

    def read(self, name: str) -> bytes:
        name = relative(name)
        if name not in self._map:
            raise Hold('REQUIRED_PACKAGE_FILE_MISSING')
        b = self.z.read(self._map[name])
        if len(b) > MAX_ENTRY_BYTES:
            raise Hold('PACKAGE_ENTRY_OVERSIZE')
        return b

    def close(self) -> None:
        self.z.close()


class DirectorySource:
    def __init__(self, root: Path):
        if root.is_symlink() or not root.is_dir():
            raise Hold('INSTALLED_DIRECTORY_UNTRUSTED')
        self.root = root.resolve()

    def names(self) -> set[str]:
        # Read only manifest referenced names; do not recursively browse user files.
        try:
            lines = self.read(MANIFEST).decode('utf-8-sig').splitlines()
        except UnicodeDecodeError as exc:
            raise Hold('MANIFEST_BAD_ENCODING') from exc
        return {MANIFEST, *(_manifest_paths(lines))}

    def read(self, name: str) -> bytes:
        current = self.root
        for segment in relative(name).split('/'):
            current /= segment
            if current.is_symlink():
                raise Hold('INSTALLED_PATH_SYMLINK')
        if not current.is_file() or not current.resolve().is_relative_to(self.root):
            raise Hold('REQUIRED_PACKAGE_FILE_MISSING')
        metadata = current.stat()
        if metadata.st_nlink != 1:
            raise Hold('INSTALLED_PATH_MULTILINK')
        if metadata.st_size > MAX_ENTRY_BYTES:
            raise Hold('PACKAGE_ENTRY_OVERSIZE')
        return current.read_bytes()


def _manifest_paths(lines: list[str]) -> list[str]:
    if len(lines) > MAX_FILES:
        raise Hold('MANIFEST_TOO_LARGE')
    out = []
    for line in lines:
        if not line.strip():
            continue
        m = MANIFEST_LINE.fullmatch(line)
        if not m:
            raise Hold('MANIFEST_FORMAT_INVALID')
        out.append(relative(m.group(2)))
    if len(out) != len(set(out)):
        raise Hold('MANIFEST_DUPLICATE_PATHS')
    if len({x.casefold() for x in out}) != len(out):
        raise Hold('MANIFEST_PATH_CASE_COLLISION')
    return out


def _json(raw: bytes) -> dict:
    try:
        obj = json.loads(raw.decode('utf-8-sig'))
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise Hold('PACKAGE_JSON_INVALID') from exc
    if not isinstance(obj, dict):
        raise Hold('PACKAGE_JSON_OBJECT_REQUIRED')
    return obj


def inspect(source: Source, *, physical_package_sha256: str | None = None,
            expected_package_sha256: str | None = None) -> dict:
    failures: list[str] = []
    evidence: dict = {'schema_version': SCHEMA, 'status': 'HOLD',
        'scope': 'PACKAGE_BYTE_INSPECTION_ONLY', 'host_execution_verified': False,
        'native_goal_control_verified': False, 'release_accepted': False,
        'package_sha256': physical_package_sha256}
    if expected_package_sha256 is not None:
        if not SHA_RE.fullmatch(expected_package_sha256):
            raise Hold('EXPECTED_SHA256_INVALID')
        if physical_package_sha256 != expected_package_sha256:
            failures.append('PACKAGE_SHA256_EXPECTATION_MISMATCH')
    names = source.names()
    if any(x not in names for x in REQUIRED):
        failures.append('REQUIRED_PACKAGE_FILE_MISSING')
        evidence['failure_codes'] = sorted(set(failures))
        return evidence
    try:
        lines = source.read(MANIFEST).decode('utf-8-sig').splitlines()
        paths = _manifest_paths(lines)
        mismatches = []
        for line in lines:
            if not line.strip():
                continue
            m = MANIFEST_LINE.fullmatch(line)
            assert m is not None
            old, name = m.groups()
            try:
                current = hashlib.sha256(source.read(name)).hexdigest()
            except Hold:
                mismatches.append(name)
                continue
            if current != old:
                mismatches.append(name)
        if any(x not in paths for x in REQUIRED if x != MANIFEST):
            failures.append('SECURITY_CRITICAL_FILE_NOT_MANIFESTED')
        if mismatches:
            failures.append('PACKAGE_SOURCE_MANIFEST_MISMATCH')
        v = source.read('VERSION.txt').decode('utf-8-sig').strip()
        release = _json(source.read('release.json'))
        slots = _json(source.read('config/slots.json')).get('slots')
        if v != release.get('version'):
            failures.append('PACKAGE_RELEASE_VERSION_INCONSISTENT')
        if not (v.startswith('2.0.2') or v.startswith('2.1.0')):
            failures.append('CODEX_DAILY_CONTROL_VERSION_UNSUPPORTED')
        # Package-scoped project slots are not a property of this open-source
        # starter. Validate declared metadata, not the maintainer's own Goals.
        declared = release.get('goal_slots')
        def valid_keys(items):
            return (isinstance(items, list) and 1 <= len(items) <= 256 and
                    all(isinstance(v, str) and re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,79}', v)
                        for v in items) and len({v.casefold() for v in items}) == len(items))
        configured = ([x.get('key') for x in slots]
                      if isinstance(slots, list) and all(isinstance(x, dict) for x in slots)
                      else None)
        if not valid_keys(configured):
            failures.append('CONFIGURED_GOAL_SLOTS_INVALID')
        if not valid_keys(declared):
            failures.append('RELEASE_GOAL_SLOTS_INVALID')
        if valid_keys(configured) and valid_keys(declared) and set(configured) != set(declared):
            failures.append('PACKAGE_GOAL_SLOTS_INCONSISTENT')
        if release.get('native_windows_execution') != 'PERFORMED_AND_ATTESTED':
            failures.append('NATIVE_WINDOWS_ACCEPTANCE_NOT_ATTESTED')
        evidence.update({'version': v, 'release_state': release.get('release_state'),
            'manifest_checked': len(paths), 'manifest_mismatch_count': len(mismatches),
            'mismatched_paths': sorted(mismatches),
            'configured_goal_slots': configured if valid_keys(configured) else [],
            'native_windows_declared': release.get('native_windows_execution')})
    except (Hold, UnicodeError, KeyError, TypeError) as exc:
        failures.append('PACKAGE_INSPECTION_FAILED_' + type(exc).__name__)
    # Native acceptance can never be granted solely by user-editable release.json.
    failures.append('INSTALLED_HOST_AND_THREAD_READBACK_REQUIRED')
    evidence['failure_codes'] = sorted(set(failures))
    return evidence


def main() -> int:
    p = argparse.ArgumentParser(description='Read-only 2.0.2/2.1 package and installed-byte preflight')
    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument('--package-zip', type=Path)
    group.add_argument('--installed-root', type=Path)
    p.add_argument('--expected-sha256')
    a = p.parse_args()
    try:
        if a.package_zip:
            if not a.package_zip.is_file() or a.package_zip.is_symlink():
                raise Hold('PACKAGE_ZIP_UNAVAILABLE')
            physical_digest = hashlib.sha256()
            with a.package_zip.open('rb') as handle:
                for block in iter(lambda: handle.read(1024 * 1024), b''):
                    physical_digest.update(block)
            physical_sha = physical_digest.hexdigest()
            source = ZipSource(a.package_zip)
            try:
                result = inspect(source, physical_package_sha256=physical_sha,
                                 expected_package_sha256=a.expected_sha256)
            finally:
                source.close()
        else:
            if a.expected_sha256:
                raise Hold('ZIP_SHA256_INAPPLICABLE_TO_INSTALLED_DIRECTORY')
            result = inspect(DirectorySource(a.installed_root))
    except (Hold, OSError, ValueError, RuntimeError, EOFError,
            zlib.error, zipfile.BadZipFile) as error:
        result = {'schema_version': SCHEMA, 'status': 'HOLD',
                  'host_execution_verified': False, 'native_goal_control_verified': False,
                  'release_accepted': False,
                  'failure_codes': [str(error) if isinstance(error, Hold) else 'PACKAGE_IO_UNAVAILABLE']}
    print(json.dumps(result, indent=2, sort_keys=True))
    return 2 if result['status'] == 'HOLD' else 0


if __name__ == '__main__':
    sys.exit(main())
