#!/usr/bin/env python3
"""Independent installed framework QA; all changes in disposable E3 workspace only.
This is NOT Codex/Goal native verification; CLIENT/Planner authority is a synthetic fixture.
"""
from __future__ import annotations
import sys, json, hashlib, subprocess, shutil, os, time, traceback, stat, tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path
from collections import Counter

SOURCE=Path(__file__).resolve().parents[1]
ROOT=Path(tempfile.mkdtemp(prefix='ar13-installed-'))
T=SOURCE/'tools'
assert (T/'campaignctl.py').is_file()
checks=[]; logs=[]
def stamp():return datetime.now(timezone.utc).isoformat().replace('+00:00','Z')
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def take(label,ok,detail=''):
    checks.append({'test':label,'pass':bool(ok),'detail':str(detail)[:1200]})
    print(('PASS' if ok else 'FAIL')+' '+label+' '+str(detail)[:150],flush=True)
    if not ok: raise AssertionError(label+' '+str(detail))
def invoke(cmd,ok=True,contains=None,timeout=45):
    r=subprocess.run([str(x) for x in cmd],text=True,capture_output=True,timeout=timeout,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
    logs.append({'argv':[str(x) for x in cmd], 'rc':r.returncode,'out':r.stdout[-1800:],'err':r.stderr[-1800:]})
    if (r.returncode==0)!=ok or (contains and contains not in r.stdout+r.stderr):
        raise AssertionError(f'CLI {cmd} exit={r.returncode}, expected success {ok}, must contain {contains}, stdout={r.stdout[-1200:]},stderr={r.stderr[-1200:]}')
    return r

def put(p,dat):p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(dat,indent=2)+'\n',encoding='utf-8')
def get(p):return json.loads(p.read_text(encoding='utf-8'))
def ctl(control,*cmd,ok=True,contains=None,timeout=45):return invoke([sys.executable,control/'tools'/'campaignctl.py','--control-root',control,*cmd],ok,contains,timeout)
def scaffold(project,profile='SMALL',pid='B-FRESH',language='en',runtime=True,optout=True):
    cmd=[sys.executable,T/'scaffold_project.py','--target',project,'--profile',profile,'--product-id',pid,'--objective','Independent E3 disposable test project','--language',language]
    if runtime:cmd.append('--with-runtime')
    if optout:cmd.append('--no-feedback-workflow')
    return invoke(cmd)

def installed_baseline(control,pid):
    """Synthetic CLIENT decision: documented real baseline fields, never external user authority."""
    req=control/'state'/'CLIENT_REQUIREMENTS_CURRENT.md'
    s=req.read_text(encoding='utf-8').replace('Baseline status: DRAFT','Baseline status: CLIENT_CONFIRMED').replace('CLIENT confirmation: PENDING','CLIENT confirmation: CONFIRMED').replace('Confirmed at: PENDING',stamp())
    if 'Confirmed at:' not in s:s += '\nConfirmed at: '+stamp()+'\n'
    req.write_text(s,encoding='utf-8')
    t=control/'state'/'TECHNICAL_BASELINE_CURRENT.json';x=get(t)
    x.update({'status':'CURRENT','updated_at':stamp(),'baseline_version':'e3'})
    x['environment']={'development_os':'Independent portable fixture','deployment_target':'Local Python fixture only','network_mode':'LOCALHOST_ONLY','machine_profile':{'assessment_status':'OBSERVED','os_summary':'Independent CI platform','cpu_summary':'Virtual CPU','ram_gb':4,'storage_free_gb':2,'gpu_summary':'NOT_REQUIRED','notes':'No external services'}}
    x['stack']={'language':'Python','runtime':'CPython','backend':'Local test adapter','frontend':'No UI','database':'SQLite file','persistence_migrations':'Versioned local file','package_manager':'stdlib','test_stack':'subprocess','deployment':'Offline temporary directory','rationale':'Minimal deterministic framework test'}
    x['security']={'authentication_model':'NONE_LOCAL_TEST','authorization_model':'Local fixture only','secrets_management':'No credentials','data_classification':'Synthetic data','backup_recovery':'Disposable fixture','exposure_controls':['No network listeners']}
    x['ui_quality']={'strategy':'SIMPLE_FUNCTIONAL_UNLESS_PRODUCT_REQUIRES_MORE','required_checks':['CLI output truthful and clear']}
    x['unresolved']=[];put(t,x)
    p=control/'state'/'DELIVERY_PLAN_CURRENT.json';d=get(p)
    d.update({'status':'CURRENT','updated_at':stamp(),'plan_version':'e3','planning_start_date':'2026-10-16','target_release_date':'2027-01-15','next_review_date':'2027-01-01','unresolved':[],
       'milestones':[{'id':'B1','title':'Portable adapter effect','target_date':'2026-12-01','status':'PLANNED','capability_ids':['CAP_NOTE'],'depends_on':[],'done_when':'Source readback and independently checked receipt','forecast_confidence':'HIGH','evidence_refs':[]}]})
    put(p,d)
    report=invoke([sys.executable,control/'tools'/'baseline_guard.py','--control-root',control,'--json'])
    take('B2-synthetic-confirmed-baseline',json.loads(report.stdout)['ready'] is True)
    ps=control/'state'/'PRODUCT_STATE_CURRENT.json';v=get(ps)
    v.update({'status':'CURRENT','state_version':'1','current_code_ref':'e3-reviewed-src-v1','requirement_refs':['REQ-E3-SYNTHETIC'],'open_product_questions':[],
         'capabilities':[{'id':'CAP_NOTE','owner':'E3-TEST','physical_state':'PLANNED','gate':'INTEGRATION','dependencies':[],'evidence_refs':[]}],
         'active_campaign':None,'current_gate':'INTEGRATION','blockers':[]})
    put(ps,v)
    bs=control/'state'/'CURRENT_BOOTSTRAP_STATE.json';s=get(bs)
    s.update({'status':'READY','observed_code_ref':'e3-reviewed-src-v1','observed_at':stamp(),'current_gate':'INTEGRATION','next_legal_boundary':'Synthetic CLIENT authorized portable adapter test'})
    if 'currentness' in s:s['currentness'].update({'verified':True,'verified_at':stamp(),'unresolved':[]})
    put(bs,s)

def run_full_installed():
    project=ROOT/'installed_e3';shutil.rmtree(project,ignore_errors=True)
    scaffold(project,profile='STATEFUL',pid='B-FRESH',language='es')
    control=project/'.agentic-sdlc';take('B1-real-scaffold-installed-tools',all((control/'tools'/f).exists() for f in ('campaignctl.py','goal_plan.py','tool_port.py','validate_project.py')))
    first=invoke([sys.executable,control/'tools'/'reconstruct_context.py','--root',control]); take('B1-initial-context-is-untrusted','UNTRUSTED_CONTEXT' in first.stdout)
    invoke([sys.executable,control/'tools'/'validate_project.py','--root',control])
    blocked=invoke([sys.executable,control/'tools'/'baseline_guard.py','--control-root',control,'--json'],False)
    take('B1-no-silent-client-consent',json.loads(blocked.stdout)['ready'] is False)
    ctl(control,'init','--charter','campaigns/C1/CHARTER.json',ok=False,contains='PROJECT_BASELINE_NOT_READY')
    installed_baseline(control,'B-FRESH')
    charter={'schema_version':'campaign-charter-0.1','campaign_id':'C1','product_or_workstream':'B-FRESH','capability':'CAP_NOTE',
      'baseline_ref':'synthetic:CLIENT-confirmed-e3','critical_path_relevance':'Single safe portable effect',
      'goal':{'current_capability':'A v1 synthetic note file','required_capability':'A v2 synthetic note file'},
      'architecture_envelope':{'owners':['E3-TEST'],'fixed_interfaces':['write_text only'], 'allowed_interface_evolution':['No external effect'],
                              'state_semantics':['Read back target SHA'], 'protected_boundaries':['No .agentic-sdlc writes from tool']},
      'resource_envelope':{'allowed_write_surfaces':['src'],'protected_surfaces':['.agentic-sdlc','.git'],'shared_resources':[],'external_authority_gates':[],'allowed_tool_operations':['write_text'],'portable_test_adapter_only':True},
      'verification_gates':['UNIT_PROPERTY','INTEGRATION','RUNTIME_PHYSICAL'],'independent_review_required':True,
      'charter_invalidation_events':['Changed CLIENT baseline'],'done_when':['Fixture target physical readback','Independent review SHA matches']}
    cr=control/'campaigns'/'C1'/'CHARTER.json';put(cr,charter)
    registry={'schema_version':'identity-registry-0.1','updated_at':stamp(),'actors':[
         {'actor_id':'I3-E3','role_class':'I3_ENGINEERING_CAMPAIGN_LEAD','scope':'C1','status':'ACTIVE','current_run_id':'R-E3','supersedes_actor_id':None},
         {'actor_id':'I4-QA-E3','role_class':'I4_EXECUTION_TEAM_MEMBER','scope':'C1','status':'ACTIVE','current_run_id':'R-QA','supersedes_actor_id':None}]}
    put(control/'state'/'IDENTITY_REGISTRY_CURRENT.json',registry)
    authority={'schema_version':'execution-authority-0.1','updated_at':stamp(),'authority_status':'ACTIVE','campaign_id':'C1','campaign_lead_actor_id':'I3-E3',
      'current_run_id':'R-E3','baseline_ref':'synthetic:CLIENT-confirmed-e3','checkpoint_ref':None,'allowed_write_surfaces':['src'],
      'protected_surfaces':['.agentic-sdlc','.git'],'expires_at':(datetime.now(timezone.utc)+timedelta(minutes=65)).isoformat().replace('+00:00','Z'),'lease_duration_minutes':65}
    put(control/'state'/'EXECUTION_AUTHORITY_CURRENT.json',authority)
    # Fail closed when a synthetic charter/CLIENT authorisation is absent, then explicitly init under fixture.
    ctl(control,'init','--charter','campaigns/C1/CHARTER.json',ok=False,contains='activate-product-state')
    ctl(control,'init','--charter','campaigns/C1/CHARTER.json','--activate-product-state')
    take('B2-real-installed-campaign-init',get(control/'runtime'/'CAMPAIGN_RUNTIME_CURRENT.json')['revision']==1)
    ctl(control,'add','--id','W1','--title','Make a bounded local change','--write','src')
    ctl(control,'start','--id','W1','--actor','UNREGISTERED','--run','FAKE',ok=False)
    ctl(control,'start','--id','W1','--actor','I3-E3','--run','R-E3')
    runtime_path=control/'runtime'/'CAMPAIGN_RUNTIME_CURRENT.json'
    rr=get(runtime_path)['revision']
    reviewed=control/'evidence'/'plan-review.txt';reviewed.parent.mkdir(exist_ok=True);reviewed.write_text('synthetic plan review by independent E3 harness\n')
    goal={'schema_version':'agentic-goal-contract-v1','goal_id':'G-E3','campaign_id':'C1','charter_ref':'campaigns/C1/CHARTER.json',
       'charter_sha256':sha(cr),'authority_refs':{'campaigns/C1/CHARTER.json':sha(cr)},'definition_of_done':'Observe source content readback',
       'hard_gates':['Independent physical SHA'],'forbidden_effects':['network','deleting user data'],'write_envelope':['src']}
    put(control/'state'/'GOAL_CONTRACT_CURRENT.json',goal)
    plan={'steps':[{'tool_operation':'write_text','target':'src/note.py'}], 'hypotheses':[], 'blockers':[],'plan_mode':'SMALL_SOLO'}
    planfile=project/'fixture_plan.json';put(planfile,plan)
    # Plan update is an actual installed CLI CAS revision zero to one.
    result=invoke([sys.executable,control/'tools'/'goal_plan.py','--control-root',control,'--expected-revision','-1','--plan-file',planfile,'--review-evidence-ref','evidence/plan-review.txt'])
    take('B2-installed-goal-plan-cas-and-runtime-bind',get(control/'runtime'/'TACTICAL_PLAN_CURRENT.json')['revision']==0)
    invoke([sys.executable,control/'tools'/'goal_plan.py','--control-root',control,'--expected-revision','-1','--plan-file',planfile,'--review-evidence-ref','evidence/plan-review.txt'],False)
    # The native Goal authorization remains a HOLD, and is never advertised as enabled.
    gd=invoke([sys.executable,control/'tools'/'goal_guard.py','--control-root',control],False)
    take('B2-native-goal-stays-unproven',json.loads(gd.stdout)['may_execute_material_goal'] is False)
    # This is a deterministic installed *portable-test* adapter. Target bytes are the external oracle.
    src=project/'src'/'note.py';src.parent.mkdir(exist_ok=True);src.write_bytes(b'VALUE = 1\n')
    sys.path.insert(0,str(control/'tools'))
    from tool_port import _source_tree_digest,_workspace_path_sha256
    cmd={'campaign_id':'C1','actor_id':'I3-E3','run_id':'R-E3','work_unit_id':'W1','runtime_revision':rr,
         'source_tree_sha256':_source_tree_digest(project,control),'workspace_path_sha256':_workspace_path_sha256(project),
         'goal_sha256':sha(control/'state'/'GOAL_CONTRACT_CURRENT.json'),'plan_sha256':sha(control/'runtime'/'TACTICAL_PLAN_CURRENT.json'),
         'allowed_write_surfaces':['src'],'idempotency_key':'e3-tool-once','operation_id':'write_text','target':'src/note.py',
         'content_utf8':'VALUE = 2\n','expected_previous_sha256':hashlib.sha256(b'VALUE = 1\n').hexdigest()}
    cmdfile=control/'state'/'tool_command.json';put(cmdfile,cmd)
    t=ctl(control,'tool-dispatch','--workspace',project,'--command',cmdfile,'--adapter','portable-test-v1')
    receipt=json.loads(t.stdout)
    take('B2-portable-source-physical-effect',src.read_bytes()==b'VALUE = 2\n' and receipt.get('phase')=='OBSERVED' and receipt.get('physical_target_sha256')==sha(src))
    before=runtime_path.read_bytes(); ctl(control,'tool-dispatch','--workspace',project,'--command',cmdfile,'--adapter','portable-test-v1')
    take('B4-idempotent-replay-no-runtime-change',runtime_path.read_bytes()==before)
    unauthorized=dict(cmd);unauthorized['idempotency_key']='e3-unallowed';unauthorized['target']='.agentic-sdlc/state/PRODUCT_STATE_CURRENT.json'
    put(control/'state'/'unsafe.json',unauthorized);pstate=sha(control/'state'/'PRODUCT_STATE_CURRENT.json')
    ctl(control,'tool-dispatch','--workspace',project,'--command',control/'state'/'unsafe.json','--adapter','portable-test-v1',ok=False)
    take('B4-protected-state-not-written',sha(control/'state'/'PRODUCT_STATE_CURRENT.json')==pstate)
    # Command was observed, then the campaign resumes durable event transitions.
    ev=get(runtime_path)['event_log'];take('B2-observed-effect-ledger',len([e for e in ev if e['action']=='TOOL_DISPATCH_OBSERVED'])==1)
    charter_before=sha(cr)
    ctl(control,'fail','--id','W1','--note','Synthetic reviewer requested correction')
    ctl(control,'retry','--id','W1')
    ctl(control,'start','--id','W1','--actor','I3-E3','--run','R-E3')
    take('B2-same-charter-fail-retry-no-new-campaign',sha(cr)==charter_before and get(runtime_path)['campaign_id']=='C1')
    ctl(control,'verify','--id','W1','--evidence','evidence/plan-review.txt')
    ctl(control,'done','--id','W1','--result-ref','src/note.py','--evidence','evidence/plan-review.txt')
    ctl(control,'checkpoint','--summary','Synthetic physical effect verified')
    ctl(control,'hold','--reason','Simulate host interruption')
    ctl(control,'add','--id','W-FORBIDDEN','--title','should refuse',ok=False)
    ctl(control,'resume')
    ctl(control,'next')
    # review exact frozen source in disposable workspace, independent reviewer run
    review=control/'evidence'/'source-review.txt';review.write_text('observed sha '+sha(src)+'\n')
    ref=get(runtime_path)['integrated_ref']
    ctl(control,'freeze','--candidate-ref',ref)
    ctl(control,'review','--reviewer','I4-QA-E3','--run','R-QA','--verdict','PASS_FOR_STRATEGIC_RETURN','--evidence','evidence/source-review.txt')
    # Adversarial clone of the real installed reviewed campaign: the terminal must not mutate it.
    for invalid in ('MUTATED','DELETED'):
        alt=ROOT/('review_stale_'+invalid);shutil.rmtree(alt,ignore_errors=True)
        shutil.copytree(control,alt)
        target=alt/'evidence'/'source-review.txt'
        if invalid=='MUTATED':target.write_text('forged changed bytes\n')
        else:target.unlink()
        alt_runtime=alt/'runtime'/'CAMPAIGN_RUNTIME_CURRENT.json'
        before_alt=alt_runtime.read_bytes()
        ctl(alt,'terminal','--type','CAPABILITY_READY_FOR_PLANNER_ACCEPTANCE','--reason','Should reject stale evidence',ok=False)
        take('B4-installed-review-'+invalid.lower()+'-fail-closed',alt_runtime.read_bytes()==before_alt)
    # Clone with expired authority must reject a mutator without event movement.
    expired=ROOT/'expired_lease';shutil.rmtree(expired,ignore_errors=True)
    shutil.copytree(control,expired)
    ap=expired/'state'/'EXECUTION_AUTHORITY_CURRENT.json';av=get(ap);av['expires_at']='2020-01-01T00:00:00Z';put(ap,av)
    exp_runtime=expired/'runtime'/'CAMPAIGN_RUNTIME_CURRENT.json';exp_before=exp_runtime.read_bytes()
    ctl(expired,'add','--id','W-EXPIRED','--title','Not authorized',ok=False)
    take('B4-expired-lease-no-state-mutation',exp_runtime.read_bytes()==exp_before)
    ctl(control,'terminal','--type','CAPABILITY_READY_FOR_PLANNER_ACCEPTANCE','--reason','Synthetic verified terminal')
    st=get(runtime_path)
    take('B2-legal-terminal-with-independent-review',st['campaign_status']=='STRATEGIC_TERMINAL' and bool(st.get('review_freeze')))
    # The terminal is for return to planner, not publication/acceptance of native host.
    result=invoke([sys.executable,control/'tools'/'project_status.py','--control-root',control,'--json'])
    take('B2-derived-status-available',result.returncode==0 and len(result.stdout)>150)
    valid=invoke([sys.executable,control/'tools'/'validate_project.py','--root',control])
    take('B2-final-installed-schema-validation',valid.returncode==0)
    recon=invoke([sys.executable,control/'tools'/'reconstruct_context.py','--root',control])
    take('B2-final-installed-context-reconstruction',recon.returncode==0)
    return {'project':str(project),'receipt':{k:receipt.get(k) for k in ('phase','result','bytes_written','physical_target_sha256','provider_cost')},'runtime_revision':st['revision'],'events':len(st['event_log']),'terminal':st['campaign_status'],'tool_files':len(list((control/'tools').glob('*.py')))}

def main():
  result={'source':os.environ.get('GITHUB_SHA', 'LOCAL_SOURCE_FIXTURE'),'runner':sys.version.split()[0], 'started':stamp(),'checks':checks,'logs':logs}
  try:result['scenario']=run_full_installed();result['outcome']='PASS'
  except Exception as exc:result['outcome']='FAIL';result['exception']=repr(exc);traceback.print_exc()
  finally:
    result.update({'finished':stamp(),'pass_count':sum(i['pass'] for i in checks),'fail_count':sum(not i['pass'] for i in checks)})
    (ROOT/'installed_lifecycle_result.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
  print('RESULT:',result['outcome'],result.get('exception',''),flush=True)
  if result['outcome']=='PASS': shutil.rmtree(ROOT,ignore_errors=True)
  return 0 if result['outcome']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
