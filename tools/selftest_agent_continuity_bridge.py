#!/usr/bin/env python3
"""Stdlib-only boundary tests, runnable in ordinary ArquitecturaRepo CI."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / 'tools' / 'pluginctl.py'
BRIDGE = ROOT / 'plugins' / 'agent-continuity-bridge' / 'bridge.py'


def make_fixture(root: Path):
    import importlib.util
    spec = importlib.util.spec_from_file_location('acb', BRIDGE)
    acb = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(acb)
    files = {p:b'dummy fixture bytes' for p in acb.REQUIRED if p not in {'SOURCE_SHA256SUMS.txt','VERSION.txt','release.json','config/slots.json'}}
    version='3.1.0-test-fixture'
    files['VERSION.txt']=version.encode()
    files['release.json']=json.dumps({'version':version,'goal_slots':['AR_FIXTURE']}).encode()
    files['config/slots.json']=json.dumps({'slots':[{'key':'AR_FIXTURE'}]}).encode()
    files['SOURCE_SHA256SUMS.txt']=''.join(hashlib.sha256(v).hexdigest()+'  '+n+'\n' for n,v in files.items()).encode()
    archive=root/'controller-fixture.zip'
    with zipfile.ZipFile(archive,'w') as z:
        for p,b in files.items(): z.writestr('Codex_Daily_Control_3_1/'+p,b)
    return archive


def cli(*args):
    proc=subprocess.run([sys.executable,str(CLI),*map(str,args)],capture_output=True,text=True,cwd=ROOT,timeout=15)
    return proc.returncode,json.loads(proc.stdout)


def main():
    with tempfile.TemporaryDirectory(prefix='ar-acb-test-') as t:
        d=Path(t);z=make_fixture(d);p=d/'adopter';(p/'.agentic-sdlc').mkdir(parents=True)
        (p/'USER_FILE').write_text('unchanged')
        ec, report=cli('inspect','--package',z)
        assert ec==0 and report['manifest_verified'] and not report['native_host_verified']
        ec, report=cli('install','--project',p,'--package',z)
        assert ec==0 and report['status']=='REGISTERED_READ_ONLY'
        ec, report=cli('status','--project',p,'--package',z)
        assert ec==0 and report['controller_package_current'] is True
        ec,report=cli('uninstall','--project',p)
        assert ec==0 and report['status']=='UNREGISTERED'
        assert (p/'USER_FILE').read_text()=='unchanged'
    print('AGENT_CONTINUITY_BRIDGE_PORTABLE_SELFTEST_PASS')


if __name__ == '__main__':
    main()
