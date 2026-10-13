#!/usr/bin/env python3
"""Falsify incomplete or conflicting v1.2 release planning."""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
def contains(path, terms):
    f=ROOT/path
    assert f.is_file(), "MISSING_PLAN "+path
    s=f.read_text(encoding="utf-8")
    for term in terms:
        assert term in s, "PLAN_MISSING_"+path+"_"+term
    return s

def main():
    gates=json.loads((ROOT/"state/V1_2_ACCEPTANCE_CRITERIA.json").read_text(encoding="utf-8"))
    assert gates["target_release"]=="1.2.0" and gates["gates"]
    contains("docs/30_V1_2_STABILIZATION_MASTER_PLAN.md",(
        "PASS1","PASS2","Wave A","Wave B","Wave C","Wave D","Wave E",
        "MISSING_EVIDENCE","P0-01","P1-05","recovery","independent",
        "1.1.0","CLIENT","two","HOLD"))
    contains("docs/31_V1_2_L3_TERMINAL_INTAKE.md",(
        "PASS / FAIL / HOLD / NOT_APPLICABLE","P0/P1/P2","NOT_TESTED",
        "SAME_CAMPAIGN_HARDENING_REQUIRED","private"))
    contains("README.md",("docs/30_V1_2_STABILIZATION_MASTER_PLAN.md",
                          "docs/31_V1_2_L3_TERMINAL_INTAKE.md","--force"))
    contains("docs/25_V1_2_SECURITY_HARDENING_AUDIT.md",("refuses --force",))
    print("V1.2 RELEASE PLANNING SELFTEST PASSED")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
