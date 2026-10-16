#!/usr/bin/env python3
"""Offline, deterministic bounded execution work-order preflight and progress guard.

This tool cannot grant actor/CLIENT authority or validate licensing. It ensures an
I3 execution request has checkable outputs, ordered operations and a bounded fallback;
receipts remain advisory until separately source/currentness/authority verified.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

SCHEMA = 'agentic-execution-work-order-v1'
SHA256_RE = re.compile(r'^[0-9a-f]{64}$')


def load(path: Path) -> dict[str, Any]:
    obj = json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(obj, dict):
        raise ValueError('JSON must be an object')
    return obj


def nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def relative_path(path: Any) -> bool:
    if not nonempty(path) or '\\' in path or '\x00' in path or path.startswith('/'):
        return False
    parts = path.split('/')
    return all(x and x not in {'.','..'} for x in parts) and not (len(parts[0])>1 and parts[0][1]==':')


def validate(order: dict[str, Any]) -> list[str]:
    errors=[]
    if order.get('schema')!=SCHEMA: errors.append('invalid schema')
    for field in ('work_order_id','campaign_id','planner_actor','executor_actor','goal_outcome','source_revision'):
        if not nonempty(order.get(field)): errors.append(f'missing {field}')
    outcome=order.get('deliverable')
    if not isinstance(outcome,dict):
        errors.append('missing deliverable'); outcome={}
    for field in ('identity','acceptance_owner','acceptance_evidence'):
        if not nonempty(outcome.get(field)): errors.append(f'missing deliverable.{field}')
    if not relative_path(outcome.get('acceptance_evidence')):errors.append('acceptance_evidence must be a relative path')
    outputs=outcome.get('required_outputs')
    if not isinstance(outputs,list) or not outputs:
        errors.append('required_outputs cannot be empty'); outputs=[]
    for i,x in enumerate(outputs):
        if not isinstance(x,dict) or not relative_path(x.get('path')) or x.get('proof') not in ('exists','sha256_manifest'):
            errors.append(f'required_outputs[{i}] invalid')
    steps=order.get('steps')
    if not isinstance(steps,list) or not steps:
        errors.append('missing procedural steps');steps=[]
    seen=set()
    for i,s in enumerate(steps):
        if not isinstance(s,dict):
            errors.append(f'step {i}: not an object');continue
        n=s.get('id')
        if not nonempty(n) or n in seen: errors.append(f'step {i}: missing/duplicate id')
        seen.add(n)
        for f in ('operation','tool_route','physical_output','verification','failure_route'):
            if not nonempty(s.get(f)):errors.append(f'step {i}: missing {f}')
        for f in ('max_attempts','max_minutes'):
            v=s.get(f)
            if not isinstance(v,int) or isinstance(v,bool) or not (1<=v<=240):errors.append(f'step {i}: {f} must be positive bounded integer')
    budget=order.get('budget')
    if not isinstance(budget,dict):errors.append('missing budget'); budget={}
    for f in ('max_minutes','max_paid_calls','max_no_progress_cycles'):
        v=budget.get(f)
        if not isinstance(v,int) or isinstance(v,bool) or not (0<=v<=720):errors.append(f'budget.{f} invalid')
    if budget.get('max_minutes',0)<=0:errors.append('budget.max_minutes must be >0')
    if budget.get('max_no_progress_cycles',0)<=0:errors.append('budget.max_no_progress_cycles must be >0')
    metric=order.get('progress_metric')
    if not isinstance(metric,dict):errors.append('missing progress_metric');metric={}
    if not nonempty(metric.get('name')):errors.append('missing progress_metric.name')
    for f in ('baseline','target'):
        v=metric.get(f)
        if not isinstance(v,int) or isinstance(v,bool) or v<0:errors.append(f'progress_metric.{f} invalid')
    if isinstance(metric.get('baseline'),int) and isinstance(metric.get('target'),int) and metric['target']<=metric['baseline']:
        errors.append('progress target must exceed baseline')
    for f in ('authorized_completion_scope','nonblocking_advisory_gates','forbidden_work'):
        v=order.get(f)
        if not isinstance(v,list):errors.append(f'missing {f} list')
    if not order.get('authorized_completion_scope'):errors.append('completion scope cannot be empty')
    if not nonempty(order.get('exit_when_blocked')):errors.append('missing precise stop and recovery rule')
    return errors


def assess(order:dict[str,Any], receipt:dict[str,Any]) -> dict[str,Any]:
    errs=validate(order)
    if errs:return {'decision':'INVALID_ORDER','errors':errs}
    if receipt.get('work_order_id')!=order['work_order_id'] or receipt.get('source_revision')!=order['source_revision']:
        return {'decision':'STALE_OR_WRONG_RECEIPT','errors':['work order or source revision mismatch']}
    baseline=order['progress_metric']['baseline'];target=order['progress_metric']['target']
    observed=receipt.get('observed_metric')
    previous=receipt.get('previous_metric',baseline)
    stagnant=receipt.get('no_progress_cycles',0)
    elapsed=receipt.get('elapsed_minutes',0)
    paid=receipt.get('paid_calls',0)
    for name,value in [('observed_metric',observed),('previous_metric',previous),('no_progress_cycles',stagnant),('elapsed_minutes',elapsed),('paid_calls',paid)]:
        if not isinstance(value,int) or isinstance(value,bool) or value<0:
            return {'decision':'INVALID_RECEIPT','errors':[f'{name} must be nonnegative integer']}
    if observed<baseline or observed<previous or observed>target:
        return {'decision':'INVALID_RECEIPT','errors':['progress metric inconsistent with baseline/previous/target']}
    if elapsed>=order['budget']['max_minutes'] or paid>order['budget']['max_paid_calls']:
        return {'decision':'STOP_BUDGET_EXHAUSTED','observed':observed,'target':target}
    if observed==previous and stagnant>=order['budget']['max_no_progress_cycles']:
        return {'decision':'STOP_NO_DELIVERY','observed':observed,'target':target,'action':'change execution method; no self-retry loop'}
    if observed==target:
        return {'decision':'READY_FOR_INDEPENDENT_ACCEPTANCE','observed':observed,'target':target,'warning':'local counter cannot authenticate CLIENT acceptance, physical hashes, privacy or rights'}
    return {'decision':'CONTINUE_BOUNDED_EXECUTION','observed':observed,'target':target,'delta':observed-previous}


def main()->int:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('command',choices=['validate','assess'])
    p.add_argument('--order',required=True,type=Path)
    p.add_argument('--receipt',type=Path)
    args=p.parse_args()
    try:
        order=load(args.order)
        if args.command=='validate':
            err=validate(order);result={'decision':'VALID' if not err else 'INVALID_ORDER','errors':err}
        else:
            if args.receipt is None:raise ValueError('--receipt required for assess')
            result=assess(order,load(args.receipt))
        print(json.dumps(result,indent=2,ensure_ascii=False))
        return 0 if result['decision'] in {'VALID','READY_FOR_INDEPENDENT_ACCEPTANCE','CONTINUE_BOUNDED_EXECUTION'} else 2
    except (OSError,ValueError,json.JSONDecodeError) as e:
        print(json.dumps({'decision':'INVALID_INPUT','error':str(e)},ensure_ascii=False))
        return 2


if __name__=='__main__':raise SystemExit(main())
