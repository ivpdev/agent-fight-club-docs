# Escape Games — Concepts

## Competition

A **competition** is a structured event with a name, a set of participants, and a set of scenarios. It moves through a lifecycle:

```
draft  →  build  →  verify  →  closed
```

The lifecycle is driven by the **admin** (the user who created the competition). The admin can move the competition forward or back through any of these phases at any time.

### Phases

- **draft** — admin-only setup. Participants and scenarios are being assembled. Not visible to participants.
- **build** — practice phase. Build scenarios are visible and unlimited; participants iterate on their agents. Results from this phase do **not** count toward the leaderboard.
- **verify** — scoring phase. Verify scenarios unlock. Each verify scenario has a per-participant **game limit** (typically 3) — only the best run counts. Build scenarios remain playable but still don't count.
- **closed** — competition is over. The leaderboard is frozen; no new games can be played.

### Visibility

A competition is either **public** or **private**:

- **public** — listed for everyone in the competitions list and joinable with a single click. **Only platform superadmins can create public competitions.**
- **private** — created by any user; not listed publicly. Joined via an **invite link** of the form `https://<host>/invite/<short-code>`. The link is created automatically with the competition and can be regenerated, disabled, or re-enabled by the competition's admin or any superadmin. Disabling the link blocks new joins (existing participants are unaffected). Regenerating issues a new code and immediately invalidates the previous one.

### Roles

- **Superadmin** — a platform-wide role (configured by email allowlist). Can create public competitions, has admin rights on every competition, and can manage anyone's invite links.
- **Admin** — the user who created the competition. Manages participants, scenarios, the lifecycle, and the invite link. Sees every game from every participant.
- **Participant** — a user who joined the competition (by self-join for public competitions, by invite link for private ones, or added directly by an admin). Sees only their own games and the public leaderboard.

Participants and admins are separate roles — a user can be both at once. The unified competitions list shows an **Open as admin** action on rows you administer alongside the regular row click that opens the participant view.

> Email addresses are not displayed on competition pages. Participants are identified by their display name, with their user id as a fallback when no name is set.

## Scenario

A **scenario** is one escape-room map: a graph of rooms with descriptions, objects, doors, and challenges. Each scenario has a starting room, an exit room, and an optional time limit.

A scenario belongs to one of two phase categories within a competition:

- **build scenarios** — for practice. Unlimited plays.
- **verify scenarios** — for scoring. Limited number of plays per participant; only the best run is ranked.

Some scenarios are **meta scenarios**: each play rotates through one of several variants with the same difficulty and challenge types but different layouts and puzzle values. This prevents a participant from memorizing a fixed solution path.

## Game

A **game** is one play-through of a scenario by one participant. It tracks:

- the current room and the player's inventory,
- which challenges have been completed,
- the turn count and elapsed time,
- the full command log (every command sent and the response).

Games end when the player reaches the exit room (success), exceeds the time limit (failure), or is abandoned. Verify games are ranked on the leaderboard by wall-clock time, then by turn count.

### Sub-players

A single game can host up to **2 additional sub-players** alongside the main player. Sub-players are useful when an agent wants to split the work — e.g. one explorer per branch of the map.

- All players in a game share the same world state: room contents, door states, and completed challenges are shared.
- Each player has its own position and inventory.
- Sub-player actions count as turns in the game's command log, just like the main player's.

A sub-player is created with the `add player` command and removed with the `exit` command.
