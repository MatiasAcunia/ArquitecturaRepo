"""Independent fixture-only verification: never contact, launch or install Codex."""
import hashlib
import importlib.util
import json
import stat
import subprocess
import sys
import zipfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('agent_continuity_bridge', ROOT / 'bridge.py')
acb = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = acb
spec.loader.exec_module(acb)


def fixture(tmp_path, *, version='3.1.0-desktop-handoff-quota-continuity-rc', slots=None,
            tamper=False, extra=None):
    slotkeys = slots if slots is not None else ['AR_ALPHA', 'AR_BETA']
    files = {name: b'fixture non-executable source' for name in acb.REQUIRED - {'SOURCE_SHA256SUMS.txt', 'VERSION.txt', 'release.json', 'config/slots.json'}}
    files.update({
        'VERSION.txt': version.encode(),
        'release.json': json.dumps({'version': version, 'goal_slots': slotkeys,
                                    'native_windows_execution': 'NOT_PERFORMED_IN_THIS_ENVIRONMENT'}).encode(),
        'config/slots.json': json.dumps({'slots': [{'key': k} for k in slotkeys]}).encode(),
    })
    if extra:
        files.update(extra)
    manifest = ''.join(f'{hashlib.sha256(value).hexdigest()}  {name}\n' for name, value in files.items())
    files['SOURCE_SHA256SUMS.txt'] = manifest.encode()
    if tamper:
        files['bin/install.ps1'] = b'tampered executable bytes'
    package = tmp_path / 'controller.zip'
    with zipfile.ZipFile(package, 'w') as z:
        for name, content in files.items():
            z.writestr('Codex_Daily_Control_3_1/' + name, content)
    return package


def project(tmp_path):
    p = tmp_path / 'repo'
    (p / '.agentic-sdlc').mkdir(parents=True)
    (p / 'USER_CODE.py').write_text('do not edit me\n')
    return p


def test_inspect_verifies_but_refuses_native(tmp_path):
    path = fixture(tmp_path)
    obj = acb.inspect(path)
    assert obj['status'] == 'PACKAGE_VERIFIED_HOST_UNVERIFIED'
    assert obj['native_host_verified'] is False
    assert obj['external_effects_enabled'] is False
    assert obj['configured_slot_count'] == 2
    assert 'AR_ALPHA' not in json.dumps(obj)
    assert obj['manifest_files'] == len(acb.REQUIRED) - 1


def test_expected_package_sha256(tmp_path):
    p = fixture(tmp_path)
    h = hashlib.sha256(p.read_bytes()).hexdigest()
    assert acb.inspect(p, h)['controller_package_sha256'] == h
    with pytest.raises(acb.BridgeHold, match='EXPECTED_PACKAGE_SHA256_MISMATCH'):
        acb.inspect(p, '0' * 64)


def test_corrupt_manifest_holds(tmp_path):
    with pytest.raises(acb.BridgeHold, match='MANIFEST_CONTENT_MISMATCH'):
        acb.inspect(fixture(tmp_path, tamper=True))


def test_unapproved_version_holds(tmp_path):
    with pytest.raises(acb.BridgeHold, match='UNSUPPORTED_OR_MISMATCHED_CONTROLLER_VERSION'):
        acb.inspect(fixture(tmp_path, version='3.0.0'))


def test_slots_not_coupled_to_four_specific_projects(tmp_path):
    obj = acb.inspect(fixture(tmp_path, slots=['SOMETHING_ELSE', 'SECOND_PROJECT']))
    assert obj['configured_slot_count'] == 2
    assert 'SOMETHING_ELSE' not in json.dumps(obj)


@pytest.mark.parametrize('name', ['../secrets.txt', 'CON', 'FOLDER/../wrong', 'C:\\evil.ps1'])
def test_path_traversal_and_windows_device_rejected(tmp_path, name):
    p = tmp_path / 'bad.zip'
    with zipfile.ZipFile(p,'w') as z:
        z.writestr('Codex_Daily_Control_3_1/' + name, b'data')
    with pytest.raises(acb.BridgeHold):
        acb.inspect(p)


def test_casefold_collision_rejected(tmp_path):
    p = tmp_path / 'bad.zip'
    with zipfile.ZipFile(p,'w') as z:
        z.writestr('Codex_Daily_Control_3_1/README.md',b'one')
        z.writestr('Codex_Daily_Control_3_1/readme.md',b'two')
    with pytest.raises(acb.BridgeHold, match='DUPLICATE_ARCHIVE_PATH'):
        acb.inspect(p)


def test_symlink_in_archive_rejected(tmp_path):
    p = tmp_path / 'bad.zip'
    info = zipfile.ZipInfo('Codex_Daily_Control_3_1/symlink')
    info.create_system=3
    info.external_attr=(stat.S_IFLNK | 0o777) << 16
    with zipfile.ZipFile(p,'w') as z:
        z.writestr(info, 'secret')
    with pytest.raises(acb.BridgeHold):acb.inspect(p)


def test_registration_does_not_touch_product_state_or_user_files(tmp_path):
    p=project(tmp_path)
    original=(p/'USER_CODE.py').read_bytes()
    z=fixture(tmp_path)
    assert acb.install(p,z)['status']=='REGISTERED_READ_ONLY'
    marker=p/'.agentic-sdlc/plugins/agent-continuity-bridge/acb-registration.json'
    obj=json.loads(marker.read_text())
    assert obj['enabled_native_effects'] is False
    assert not (p/'.agentic-sdlc/state/PRODUCT_STATE_CURRENT.json').exists()
    assert (p/'USER_CODE.py').read_bytes()==original
    assert str(p) not in marker.read_text()
    assert acb.status(p,z)['controller_package_current'] is True
    assert acb.uninstall(p)['status']=='UNREGISTERED'
    assert (p/'USER_CODE.py').read_bytes()==original
    assert z.is_file()


def test_duplicate_registration_refused(tmp_path):
    p=project(tmp_path);z=fixture(tmp_path)
    acb.install(p,z)
    with pytest.raises(acb.BridgeHold,match='PLUGIN_ALREADY_REGISTERED_OR_CONFLICT'):
        acb.install(p,z)


def test_modification_prevents_uninstall(tmp_path):
    p=project(tmp_path);z=fixture(tmp_path)
    acb.install(p,z)
    marker=p/'.agentic-sdlc/plugins/agent-continuity-bridge/acb-registration.json'
    record=json.loads(marker.read_text());record['attacker']='other';marker.write_text(json.dumps(record))
    with pytest.raises(acb.BridgeHold,match='PLUGIN_REGISTRATION_MODIFIED'):
        acb.uninstall(p)
    assert marker.exists()


def test_additional_user_file_prevents_uninstall(tmp_path):
    p=project(tmp_path);z=fixture(tmp_path)
    acb.install(p,z)
    marker=p/'.agentic-sdlc/plugins/agent-continuity-bridge/USER_PRIVATE.txt';marker.write_text('stay')
    with pytest.raises(acb.BridgeHold,match='PLUGIN_CONTENT_CHANGED_REFUSE_REMOVE'):
        acb.uninstall(p)
    assert marker.exists()


def test_uncontrolled_environment_not_prerequisite(tmp_path):
    assert acb.PLUGIN_ID == 'agent-continuity-bridge'
    assert acb.inspect(fixture(tmp_path))['capabilities']['desktop_handoff']=='UNVERIFIED_DISABLED'


def test_cli_error_returns_hold_without_sensitive_paths(tmp_path):
    p=subprocess.run([sys.executable,str(ROOT/'bridge.py'),'inspect','--package',str(tmp_path/'SECRET_USER_FILE.zip')],text=True,capture_output=True)
    assert p.returncode==2
    assert json.loads(p.stdout)['status']=='HOLD'
    assert 'SECRET_USER_FILE.zip' not in p.stdout
