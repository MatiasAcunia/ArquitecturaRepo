# Prompt — Fresh Context Probe

You are entering an existing project as a completely fresh agent.

Start as `UNTRUSTED_CONTEXT`.

Do not assume conversation continuity, prior memory, newest-looking filenames, worker summaries or historical handoffs are current authority.

Read the project's root agent instructions and reconstruct current state from durable evidence.

Do not mutate anything.

Return a compact reconstruction containing:

- project/workstream identity;
- your role and non-role;
- current CLIENT requirements and open product questions;
- Product State;
- exact current code/ref/runtime authority you can physically establish;
- active campaign, charter and checkpoint/terminal if any;
- current gate;
- strongest evidence;
- stale/superseded/prepared-but-inactive state you detected;
- UNKNOWN facts;
- next legal action;
- actions currently forbidden.

Fail closed on unresolved material contradictions.

Do not ask the CLIENT to resolve technical state that repository/runtime evidence should resolve.

Do not claim physical runtime/DB truth from repository text alone.
