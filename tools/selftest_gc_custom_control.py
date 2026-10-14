#!/usr/bin/env python3
"""Two isolated custom-control-dir GC regressions. Never touches the supplied project.

Usage: python exec5_regression_custom_control.py "<source-repo>/tools/artifact_ledger.py"
PASS requires both successful exact removal and durable correct-ledger update.
"""
from __future__ import annotations
import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path


def run() -> int:
    if len(sys.argv) == 1:
        sys.argv.append(str(Path(__file__).with_name('artifact_ledger.py')))
    if len(sys.argv) != 2:
        raise SystemExit('Usage: python selftest_gc_custom_control.py [artifact_ledger.py]')
    tool = Path(sys.argv[1]).resolve(strict=True)
    assert tool.is_file()
    spec = importlib.util.spec_from_file_location('candidate_artifact_ledger', tool)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    with tempfile.TemporaryDirectory(prefix='gc-custom-control-falsifier-') as tmp:
        project = Path(tmp) / 'project'; project.mkdir()
        def git(*args: str) -> None:
            p = subprocess.run(['git', '-C', str(project), *args], capture_output=True, text=True)
            assert p.returncode == 0, (args,p.stdout,p.stderr)
        def call(*args: str) -> tuple[int, dict]:
            p = subprocess.run([sys.executable, str(tool), '--project', str(project),
                '--control-dir', '.customctl', *args], capture_output=True, text=True)
            try: d = json.loads(p.stdout)
            except json.JSONDecodeError: raise AssertionError((args,p.stdout,p.stderr))
            return p.returncode, d
        git('init', '-b', 'main')
        git('config','user.name','Audit Fixture')
        git('config','user.email','synthetic-no-email')
        (project/'.gitignore').write_text('.customctl/\n.agentic-sdlc-scratch/\n')
        (project/'review.txt').write_text('Synthetic review evidence only.\n')
        git('add','.gitignore','review.txt');git('commit','-m','fixture')
        runtime=project/'.customctl/runtime';runtime.mkdir(parents=True)
        ledger=runtime/'ARTIFACT_LIFECYCLE_CURRENT.json'
        ledger.write_text(json.dumps(module.initial()))
        rc,d=call('init-root','--root','.agentic-sdlc-scratch/c1','--owner','I3','--campaign','C1')
        assert rc==0,d
        target_name='.agentic-sdlc-scratch/c1/data.tmp'
        target=project/target_name
        action=f'from pathlib import Path;Path({str(target)!r}).write_bytes(b"SYNTHETIC GC FIXTURE")'
        rc,d=call('capture','--root','.agentic-sdlc-scratch/c1','--category','DERIVED_REBUILDABLE',
            '--safe-delete','--ttl-hours','-1','--',sys.executable,'-c',action)
        assert rc==0,d
        rc,d=call('review','--path',target_name,'--owner','I3','--campaign','C1',
            '--reviewer','SYNTHETIC_DIFFERENT_REVIEWER','--decision','ACCEPTED','--evidence-ref','review.txt')
        assert rc==0,d
        # A failed prior writer on selected custom ledger must prevent GC readiness.
        lock = ledger.with_name(ledger.name + '.lock')
        lock.write_text(json.dumps({'schema_version':'artifact-ledger-lock-v1',
            'status':'failed','pid':1,'host':'fixture.invalid','operation':'capture',
            'root':'.agentic-sdlc-scratch/c1','started_at':'2020-01-01T00:00:00Z'}))
        rc, blocked = call('gc')
        lock.unlink()
        if not (rc == 0 and blocked['ready_count'] == 0 and
                any(row['reason']=='INTERRUPTED_OPERATION_RECOVERY_REQUIRED'
                    for row in blocked['rows'])):
            print(json.dumps({'test':'GC_CUSTOM_CONTROL_FAILED_LOCK', 'result':'FAIL',
                'ready_count':blocked.get('ready_count'),
                'row_reasons':[row['reason'] for row in blocked.get('rows',[])]}))
            return 1
        print(json.dumps({'test':'GC_CUSTOM_CONTROL_FAILED_LOCK','result':'PASS'}))
        rc,plan=call('gc');assert rc==0 and plan['ready_count']==1,plan
        plan_path=Path(tmp)/'gc-plan.json';plan_path.write_text(json.dumps(plan))
        approval_path=Path(tmp)/'gc-approval.json'
        rc,d=call('approve-gc','--plan-file',str(plan_path),'--path',target_name,
            '--reviewer','SYNTHETIC_DIFFERENT_REVIEWER','--evidence-ref','review.txt',
            '--approval-out',str(approval_path))
        assert rc==0,d
        before=json.loads(ledger.read_text())
        rc,result=call('gc','--execute','--approval',str(approval_path))
        after=json.loads(ledger.read_text())
        observed={'exit_code':rc,'file_absent':not target.exists(),
            'before_revision':before['revision'],'after_revision':after['revision'],
            'recorded_status':after['files'][target_name]['status'],
            'failure_codes':result.get('failure_codes',[])}
        ok=rc==0 and not target.exists() and after['revision']>before['revision'] and after['files'][target_name]['status']=='DELETED'
        print(json.dumps({'result':'PASS' if ok else 'FAIL', 'test':'GC_CUSTOM_CONTROL_EXACT_LEDGER', **observed},indent=2))
        return 0 if ok else 1

if __name__=='__main__':
    raise SystemExit(run())
