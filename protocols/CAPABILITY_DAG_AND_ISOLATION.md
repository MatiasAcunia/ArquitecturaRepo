# Capability DAG and Isolation

## Two graph levels

### Strategic capability graph

Owned by I2/I1.

Nodes represent meaningful capabilities/engines, dependencies, owner, current state, product unlock and current gate.

### Tactical campaign DAG

Owned dynamically by I3.

I3 may create, split, merge, reorder, reprioritize or retire work units while the charter remains valid.

Do not force I2 to enumerate the tactical DAG.

## Parallelism

Parallel execution is legal only when:

- dependencies permit;
- write/resource sets are isolated or explicitly serialized;
- shared DB/provider/publication/current-state resources remain controlled;
- workspace identity is explicit where necessary;
- evidence attribution remains exact;
- expected benefit exceeds coordination cost.

No fixed worker count is a goal.

## Assignment isolation

A material assignment should bind enough of:

- campaign/assignment identity;
- capability owner;
- baseline SHA/snapshot;
- workspace/branch/worktree identity;
- role;
- allowed write set;
- protected surfaces;
- DB/shared resources;
- input authority refs;
- expected evidence;
- output/head/artifact identity.

Isolation does not grant authority to mutate protected state, spend money, publish, or modify another project.

## Reconciliation

I3 is the singular campaign integration owner.

Executor completion is evidence, not merge or route authority.

Campaign closeout records accepted/rejected work, exact integrated head/state, evidence, remaining blockers and next tactical work or strategic terminal.
