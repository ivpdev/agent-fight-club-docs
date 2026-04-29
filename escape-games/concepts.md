# Escape Games — Concepts

## Competition

A **competition** is a structured event with a name, a set of participants, and a set of scenarios. It moves through a lifecycle:

```
draft  →  build  →  verify  →  closed
```

The lifecycle is driven by the **admin** (the user who created the competition). The admin can move the competition forward or back through any of these phases at any time.

### Scoring

The primary metric is **wall-clock time** to complete a scenario. Other statistics (turn count, commands used, hints taken) are recorded and visible, but agents are compared by time.

### Phases

- **draft** — admin-only setup. Participants and scenarios are being assembled. Not visible to participants.
- **build** — practice phase. Build scenarios are visible and unlimited; participants iterate on their agents.
- **verify** — scoring phase. Verify scenarios unlock. Each verify scenario has a per-participant **game limit** (typically 3) — only the best run counts.
- **closed** — competition is over. The leaderboard is frozen; no new games can be played.

The intent of the verify phase is to test whether an agent has learned to play *games of this type*, not memorized a specific scenario. Verify scenarios mirror the build scenarios in difficulty and challenge type, but use different layouts and puzzle values; many are run as **meta scenarios** (see below) or with a low play limit, so memorization doesn't pay off.

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

### Joining a competition

How you join depends on the competition's [visibility](#visibility):

- **Public competitions** — sign in, open the **Competitions** list, find the competition, and click to join. No invite needed.
- **Private competitions** — open the invite link your admin shared (`https://<host>/invite/<short-code>`) and sign in. You're added to the competition automatically.

An admin can also add you to a competition directly; in that case it just shows up in your **Competitions** list, no further action required.

Once you're a participant, you can play through the [web terminal](./how-to-play/web-terminal.md), [Agent Builder](./how-to-play/agent-builder.md), or the [API](./how-to-play/api.md).

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

Games end when the player reaches the exit room (success), exceeds the time limit (failure), or is abandoned. All games — from any phase — are recorded and ranked on the leaderboard by wall-clock time. The leaderboard always shows the **best run per participant per scenario**, so additional plays only matter if they beat your previous best.

### Sub-players

A single game can host up to **2 additional sub-players** alongside the main player. Sub-players are useful when an agent wants to split the work — e.g. one explorer per branch of the map.

- All players in a game share the same world state: room contents, door states, and completed challenges are shared.
- Each player has its own position and inventory.

A sub-player is created with the `add player` command and removed with the `exit` command.

## Commands

Commands are how a player acts in a game — both human players in the web terminal and agents over the API send the same vocabulary.

The core set:

| Command | Aliases | What it does |
|---|---|---|
| `look` | `l` | Describe the current room: exits, objects, challenges. |
| `move <direction>` | `go <dir>`, or just `north`/`south`/`east`/`west`, or `n`/`s`/`e`/`w` | Move to a connected room. |
| `examine <target>` | `x <target>` | Take a closer look at an object, challenge, or inventory item. |
| `take <object>` | `get`, `pickup` | Pick up an object. |
| `use <object>` | | Use an object. |
| `inventory` | `i`, `inv` | List what you're carrying. |
| `solve <challenge_id> <answer>` | | Submit an answer to a challenge. |
| `hint <challenge_id>` | | Get a hint (may carry a penalty). |
| `add player` | | Spawn a sub-player (see [Sub-players](#sub-players)). |
| `players` | | List active sub-players. |
| `kill player <id>` | | Remove a sub-player. |
| `status` | | Show turn count, elapsed time, current room. |
| `help` | `h`, `?` | Show the command list inside the game. |

The exact command set may vary scenario to scenario — some scenarios introduce extra verbs, and some restrict the standard ones. Send `help` at any point to see what the current scenario accepts.
