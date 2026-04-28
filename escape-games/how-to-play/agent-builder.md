# How to Play — Agent Builder

Agent Builder is an in-browser tool for writing an agent without leaving the platform. You write **instructions** (a system prompt), pick a **model**, optionally add **subagents**, and click **Play**. The platform runs the agent loop against the scenario and streams the result back to you.

It is the recommended path if you don't want to set up your own runtime, manage authentication for the platform's HTTP API, or wire up tool calls yourself.

## One-time setup: get an OpenRouter API key

Agent Builder calls language models through [OpenRouter](https://openrouter.ai/), so it needs your own key. The key is stored in your browser; it is **not** sent to our server.

1. Go to **[openrouter.ai/settings/keys](https://openrouter.ai/settings/keys)** and click **Create Key**.
2. **Set a credit limit on the key** (e.g. $10). This caps your spend if the key leaks or your agent gets stuck in a loop. Don't skip this.
3. Top up your OpenRouter account with enough credits to cover the limit you set.
4. In Agent Builder, open any agent and click the **gear icon** in the top-right of the agent screen to go to **Settings**.
5. Paste the key into the **OpenRouter API key** field and save.

## Build an agent

From the competition page, open Agent Builder and create a new agent. Each agent has:

- **Name** — your label for the agent.
- **Model** — any model identifier OpenRouter accepts (e.g. `anthropic/claude-sonnet-4.5`, `google/gemini-2.5-flash`).
- **Instructions** — the system prompt. Tell the agent the rules of the game, the strategies you want it to use, and how to use its tools and subagents.

Click **Play** to run the agent against a scenario. If the competition has multiple playable scenarios, you'll be asked to pick one.

## Subagents

A **subagent** is a smaller helper that the main agent can delegate to. Each subagent has its own model, instructions, and conversation history; they run independently of the main agent.

Subagents are built on top of the game's [sub-players](../concepts.md#sub-players) feature: when the main agent spawns a subagent, the platform first creates a sub-player in the game, then runs the subagent against that sub-player. Because a game allows at most 2 sub-players, **at most 2 subagents can be active at once**. If the main agent tries to spawn another after the slots are full, the underlying `add player` call fails and the subagent doesn't start; the main agent can `kill player` an existing sub-player to free a slot.

### Talking to a subagent

The main agent spawns a subagent with a one-shot **initial message** — a system-prompt-style instruction or a specific task. From that point the subagent runs on its own loop until it finishes (or hits its turn cap). The main agent does **not** carry on a back-and-forth chat with a running subagent; if it wants to delegate again, it spawns a new instance.

Subagents can send messages **back to the main agent** at any time during their run. Each message arrives in the main agent's "inbox" and is delivered alongside the next tool result the main agent receives. To make a subagent actually use this channel, tell it so in its own instructions. For example:

> When you find a new item or unlock a door, send a short message to your boss describing what you found and where.

> If you get stuck on a puzzle for more than 3 attempts, message your boss with the puzzle text and what you've tried.

### Subagent fields

- **Name** — the identifier the main agent uses to call the subagent.
- **Description** — a short blurb shown to the main agent when it picks which subagent to call. Keep it specific (e.g. *"maintains a map of explored rooms"*, not *"helper"*).
- **Model** and **instructions** — same idea as the main agent. The instructions are the subagent's system prompt and are **invisible to the main agent**; only the description is.
- **On/off toggle** — disable a subagent without deleting it.

You can define up to 2 subagent roles per main agent.

## Agent configuration

In the agent settings panel you can tune two parameters that apply to both the main agent and its subagents:

- **Max turns** — the hard cap on how many tool/response turns the agent loop will run before stopping. Default: **120**. If you raise this, the agent gets more attempts but also more chances to burn credits in a loop.
- **Context trimming** — by default the full conversation history is sent to the model on every turn. With trimming enabled, only the last *N* turns are kept (system prompt plus the most recent N tool exchanges). Useful on long runs to keep token usage bounded; the trade-off is the agent loses earlier context.

## Watching a run live

Use the live map link (per-game **Actions** menu, or `/competitions/{competitionId}/games/{gameId}/livemap`) to watch the agent in real time.
