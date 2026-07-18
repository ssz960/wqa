# Registry contract

The Manifest is the only synchronization entry point. Paths are repository-relative and must remain inside the pinned checkout. `active.json` is an upstream recommendation, not a server activation command.

Server flow:

`pinned commit -> Manifest -> size/hash/schema checks -> streaming staging import -> count/query/profile checks -> atomic Active switch -> retain Previous`

Runtime flow:

`Active Snapshot database -> bounded indexed recall -> authoritative Field/Operator/Profile validation -> snapshot_id + simulation_profile_hash audit`

The repository does not authorize WorldQuant execution. Missing coverage, unverified Operator compatibility, an invalid hash, an illegal Simulation Profile, or an unavailable resource check must fail closed.
