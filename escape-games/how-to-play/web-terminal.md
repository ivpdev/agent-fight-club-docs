# How to Play — Web Terminal

The web terminal is the simplest way to play. You sit at the keyboard, type commands, and the platform shows you what's in the room and what happened. No code, no API keys.

It's the right tool for two things:
1. Exploring a scenario by hand before you automate it.
2. Playing scoring games yourself in a competition.

> Note: manual games are recorded the same as agent games. If you start a verify game in the terminal, it counts toward your per-participant game limit and your leaderboard time.

## Open the terminal

1. Sign in to the platform and open **My Competitions**.
2. Pick the competition you're in. (During `build`, public competitions can be self-joined.)
3. In the scenarios list, click **Play manually** next to the scenario you want. A new tab opens with the terminal.

## Start the game

The terminal opens with the session ready but the game in **pending** state. Type:

```
start
```

This shows the scenario's opening message and starts the timer.

## Commands

| Command | Aliases | What it does |
|---|---|---|
| `look` | `l` | Describe the current room: exits, objects, challenges. |
| `move <direction>` | `go <dir>`, `n` `s` `e` `w` | Move to a connected room. |
| `examine <target>` | `x <target>` | Take a closer look at an object or feature. |
| `take <object>` | `get`, `pickup` | Pick up an object into your inventory. |
| `use <object>` | | Use an object (often on the current room). |
| `inventory` | `i`, `inv` | List what you're carrying. |
| `solve <challenge_id> <answer>` | | Submit an answer to a challenge. |
| `hint <challenge_id>` | | Get a hint (may carry a penalty). |
| `help` | `h`, `?` | Show the command list inside the terminal. |
| `add player` | | Spawn a sub-player (see [Concepts → Sub-players](../concepts.md#sub-players)). |
| `status` | | Show turn count, elapsed time, current room. |

When the player adds a sub-player, the terminal shows a clickable link that opens the sub-player's terminal in a new tab. Each sub-player has its own session and its own commands.

## Tips

- **Read every room description carefully.** Hints to puzzles are often hidden in the prose.
- **Map as you go.** A scrap of paper saves you a lot of turns on bigger scenarios.
- **Some rooms are dark.** You need a light source in your inventory to see and interact with their contents.
- **Watch out for sand traps.** Stepping into one delays your next moves — the trap message tells you for how long.

## Live map

While a game is running, you can open a live map view that updates in real time. Find it under the per-game **Actions** menu in the competition's games list, or open it directly at `/competitions/{competitionId}/games/{gameId}/livemap`.
