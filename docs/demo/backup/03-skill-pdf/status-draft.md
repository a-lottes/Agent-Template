# Weekly Status Report

Date: 2026-10-21

## Highlights

- Go-live rescheduled from 30 Nov to 14 Dec due to data migration readiness.
- Pilot scope confirmed: claims department only.

## Decisions This Week

| Date | Decision | Decided by |
|---|---|---|
| 2026-10-12 | Go-live date moved from 30 Nov to 14 Dec because the data migration is not ready | Clara |
| 2026-10-12 | Pilot starts with the claims department only | TBD |

## Open Actions by Owner

### Ben
- **[OVERDUE]** Deliver the interface specification — due 2026-10-19 — status: open

### Clara
- Check budget impact for the extra two weeks with finance — due: TBD — status: open

### Unassigned (TBD)
- Run a load test before go-live — due: TBD — status: open

## Top Risks

1. Test environment still uses production-like data; cleanup unowned (impact/likelihood: TBD, mitigation: TBD)
2. Vendor API rate limit might not carry the pilot load (impact/likelihood: TBD, mitigation: TBD)

## Questions for the Steering Committee

- Who owns the pilot-start decision (currently unassigned)?
- Has the budget impact for the two-week delay been confirmed with finance?
- Who will own and schedule the pre-go-live load test?
- Who will own cleanup of production-like data in the test environment, and by when?
