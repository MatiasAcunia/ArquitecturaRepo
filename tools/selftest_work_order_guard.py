#!/usr/bin/env python3
"""Negative and positive external oracles for bounded execution contracts."""
import copy
import json
import sys
from pathlib import Path
from work_order_guard import assess,validate

ROOT=Path(__file__).resolve().parents[1]
order=json.loads((ROOT/'templates/EXECUTION_WORK_ORDER.json').read_text(encoding='utf-8'))
assert validate(order)==[],validate(order)
base={'work_order_id':order['work_order_id'],'source_revision':order['source_revision'],'observed_metric':0,'previous_metric':0,'no_progress_cycles':0,'elapsed_minutes':0,'paid_calls':0}

def go(patch,decision):
    r=assess(order,{**base,**patch})
    assert r['decision']==decision,(r,decision)

go({'observed_metric':120},'CONTINUE_BOUNDED_EXECUTION')
go({'observed_metric':420,'previous_metric':120},'READY_FOR_INDEPENDENT_ACCEPTANCE')
go({'observed_metric':0,'no_progress_cycles':2},'STOP_NO_DELIVERY')
go({'observed_metric':35,'elapsed_minutes':90},'STOP_BUDGET_EXHAUSTED')
go({'paid_calls':1},'STOP_BUDGET_EXHAUSTED')
go({'source_revision':'stale'},'STALE_OR_WRONG_RECEIPT')
go({'observed_metric':421},'INVALID_RECEIPT')
go({'observed_metric':10,'previous_metric':11},'INVALID_RECEIPT')
bad=copy.deepcopy(order);bad['steps'][0].pop('physical_output');assert validate(bad)
bad=copy.deepcopy(order);bad['steps'][0]['max_attempts']=0;assert validate(bad)
bad=copy.deepcopy(order);bad['deliverable']['acceptance_evidence']='../../untrusted';assert validate(bad)
bad=copy.deepcopy(order);bad['budget']['max_minutes']=0;assert validate(bad)
bad=copy.deepcopy(order);bad['authorized_completion_scope']=[];assert validate(bad)
print('WORK-ORDER GUARD SELFTEST PASSED: exact output, bounded progress, stale source, autonomy & STOP')
