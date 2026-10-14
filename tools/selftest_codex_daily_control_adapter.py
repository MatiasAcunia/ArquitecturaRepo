import hashlib
import json
import stat
import sys
import zipfile
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from codex_daily_control_adapter import ZipSource, inspect, Hold

ROOT = 'Codex_Daily_Control_2_0/'


def package(tmp_path, *, tamper=False, version='2.0.2-hardening-candidate', slots=None):
    root = tmp_path/'candidate.zip'
    files = {
        'VERSION.txt': version.encode(),
        'release.json': json.dumps({'version': version,'goal_slots': ['ROBLOX','MUSIC','TRO','CTR5'],
                     'native_windows_execution':'NOT_PERFORMED_IN_THIS_ENVIRONMENT'}).encode(),
        'config/slots.json': json.dumps({'slots': [{'key': k} for k in (slots or ['ROBLOX','MUSIC','TRO','CTR5'])]}).encode(),
        'bin/codex-daily-control.ps1':b'safe sample',
        'bin/install.ps1':b'install fixture',
        'src/CodexDailyControl/CodexDailyControl.psd1':b'psd1',
        'src/CodexDailyControl/Private/91-V2Close.ps1':b'close fixture',
        'src/CodexDailyControl/Private/60-Goals.ps1':b'goals fixture',
        'src/CodexDailyControl/Private/50-AppServer.ps1':b'client fixture',
    }
    hashes = [hashlib.sha256(v).hexdigest() + '  ' + k for k, v in files.items()]
    if tamper:
        files['bin/install.ps1'] = b'changed after signing'
    files['SOURCE_SHA256SUMS.txt']='\n'.join(hashes).encode()
    with zipfile.ZipFile(root,'w') as z:
        for n, b in files.items():
            z.writestr(ROOT + n,b)
    return root


def read(zip_path,expected=None):
    s=ZipSource(zip_path)
    try:
        return inspect(s, physical_package_sha256=hashlib.sha256(zip_path.read_bytes()).hexdigest(),
                       expected_package_sha256=expected)
    finally:
        s.close()


def test_clean_package_still_not_native_host_accepted(tmp_path):
    z=package(tmp_path)
    r=read(z)
    assert r['manifest_mismatch_count']==0
    assert not r['release_accepted']
    assert 'INSTALLED_HOST_AND_THREAD_READBACK_REQUIRED' in r['failure_codes']


def test_modified_package_bytes_fail(tmp_path):
    r=read(package(tmp_path,tamper=True))
    assert r['manifest_mismatch_count']==1
    assert 'PACKAGE_SOURCE_MANIFEST_MISMATCH' in r['failure_codes']


def test_expected_full_archive_identity(tmp_path):
    z=package(tmp_path)
    assert 'PACKAGE_SHA256_EXPECTATION_MISMATCH' in read(z,expected='0'*64)['failure_codes']
    digest=hashlib.sha256(z.read_bytes()).hexdigest()
    assert 'PACKAGE_SHA256_EXPECTATION_MISMATCH' not in read(z,expected=digest)['failure_codes']


def test_reject_wrong_slot_set(tmp_path):
    z=package(tmp_path,slots=['ROBLOX','MUSIC','TRO','OTHER'])
    assert 'CONFIGURED_GOAL_SLOTS_NOT_EXPECTED_FOUR' in read(z)['failure_codes']


def test_reject_new_or_old_version(tmp_path):
    assert 'VERSION_NOT_2_0_2' in read(package(tmp_path,version='2.0.1'))['failure_codes']


def test_reject_archive_path_traversal(tmp_path):
    z=tmp_path/'bad.zip'
    with zipfile.ZipFile(z,'w') as archive:
        archive.writestr(ROOT+'../../evil.ps1',b'text')
    with pytest.raises(Hold): ZipSource(z)


def test_reject_repeated_paths(tmp_path):
    z=tmp_path/'bad.zip'
    with zipfile.ZipFile(z,'w') as archive:
        archive.writestr(ROOT+'README.md',b'text')
        archive.writestr(ROOT+'README.md',b'text2')
    with pytest.raises(Hold): ZipSource(z)


def test_reject_windows_casefold_path_collision(tmp_path):
    z=tmp_path/'casefold.zip'
    with zipfile.ZipFile(z,'w') as archive:
        archive.writestr(ROOT+'README.md',b'one')
        archive.writestr(ROOT+'readme.MD',b'two')
    with pytest.raises(Hold): ZipSource(z)


def test_reject_windows_device_filename(tmp_path):
    z=tmp_path/'device.zip'
    with zipfile.ZipFile(z,'w') as archive:
        archive.writestr(ROOT+'CON.txt',b'unsafe alias')
    with pytest.raises(Hold): ZipSource(z)


def test_reject_archive_symlink_entry(tmp_path):
    z=tmp_path/'symlink.zip'
    info=zipfile.ZipInfo(ROOT+'link.ps1')
    info.create_system=3
    info.external_attr=(stat.S_IFLNK | 0o777) << 16
    with zipfile.ZipFile(z,'w') as archive:
        archive.writestr(info,'target.ps1')
    with pytest.raises(Hold): ZipSource(z)


def test_missing_required_is_hold(tmp_path):
    z=tmp_path/'bad.zip'
    with zipfile.ZipFile(z,'w') as archive:
        archive.writestr(ROOT+'SOURCE_SHA256SUMS.txt',b'')
    r=read(z)
    assert r['status']=='HOLD'
    assert 'REQUIRED_PACKAGE_FILE_MISSING' in r['failure_codes']


def test_installed_directory_manifest_readonly(tmp_path):
    from codex_daily_control_adapter import DirectorySource
    z=package(tmp_path)
    folder=tmp_path/'installed'
    folder.mkdir()
    with zipfile.ZipFile(z) as arc:
        for file in arc.infolist():
            rel=file.filename.removeprefix(ROOT)
            if not rel:
                continue
            target=folder/rel
            target.parent.mkdir(parents=True,exist_ok=True)
            target.write_bytes(arc.read(file))
    before={str(f.relative_to(folder)): hashlib.sha256(f.read_bytes()).hexdigest()
            for f in folder.rglob('*') if f.is_file()}
    result=inspect(DirectorySource(folder))
    after={str(f.relative_to(folder)): hashlib.sha256(f.read_bytes()).hexdigest()
           for f in folder.rglob('*') if f.is_file()}
    assert result['manifest_mismatch_count']==0
    assert before==after
    assert result['host_execution_verified'] is False


def test_reject_installed_path_symlink(tmp_path):
    from codex_daily_control_adapter import DirectorySource
    source=tmp_path/'source';source.mkdir(); (source/'target').write_text('text')
    (source/'pointer').symlink_to(source/'target')
    with pytest.raises(Hold): DirectorySource(source).read('pointer')
