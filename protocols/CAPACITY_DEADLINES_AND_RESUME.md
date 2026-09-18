# Capacity, Deadlines and Resume Semantics

## Capacity is an execution constraint, not a product verdict

Token limits, agent quotas, unavailable compute, external service downtime and other capacity interruptions can stop physical execution without invalidating the product objective or campaign.

## Capacity checkpoint

When useful legal work remains but execution cannot continue because capacity is unavailable:

- preserve the same campaign identity;
- checkpoint exact state;
- persist READY/BLOCKED tactical work;
- record resource/capacity blocker;
- emit a resumable capacity terminal only if physical relaunch is required.

Do not create a new campaign solely because capacity returned later.

## Deadlines

Separate:

- CLIENT/business deadlines;
- internal forecasts;
- campaign estimates;
- external windows.

A capacity interruption may invalidate an old forecast without changing the product quality bar.

Do not invent a new committed date unless the authority that owns that deadline rebases it.

## Resume

When capacity returns:

1. reconstruct current Product/Engineering State;
2. verify charter remains valid;
3. verify no newer authority superseded the campaign;
4. reacquire execution authority if required;
5. refresh time-sensitive dependencies;
6. resume the SAME campaign from checkpoint.

## Failure classification

Do not count a forced no-capacity interval as engineering underperformance.

Do count failures to checkpoint, reconstruct or resume safely as system defects.

## External provider changes

If a campaign depends on time-sensitive provider/model/pricing/terms/current availability, refresh that evidence before material external action.

A previously valid provider assumption is not permanently current.
