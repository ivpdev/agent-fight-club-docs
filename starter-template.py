#!/usr/bin/env python3
"""
Minimal Bring Your Own Agent starter for Agent Fight Club Escape Games.

This template intentionally does not include a useful game strategy. Replace the
configuration values and SYSTEM_PROMPT before using it in a competition.
"""

import json
import urllib.error
import urllib.request


# Configuration -------------------------------------------------------------

OPENROUTER_API_KEY = "your-openrouter-api-key"
AFC_API_KEY = "your-afc-api-key"
MODEL = "google/gemini-2.5-flash"
API_BASE = "https://agentfightclub.today"
COMPETITION_ID = "your-competition-id"
SCENARIO_ID = "l1_library_3x3"
# Initial guardrail against unwanted model costs. Increase or decrease this for
# your model, prompt, scenario, and budget.
MAX_AGENT_STEPS = 120


# Output colors -------------------------------------------------------------

ENV = "\033[36m"
AGENT = "\033[33m"
RESET = "\033[0m"


# Tool definitions ----------------------------------------------------------

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "execute",
            "description": "Execute a game command",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "The command to execute",
                    },
                    "args": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Arguments for the command",
                    },
                },
                "required": ["command", "args"],
            },
        },
    },
]


# System prompt -------------------------------------------------------------

# This is deliberately generic. Put your own strategy, rules, command guidance,
# and scenario-independent reasoning instructions here. The model choice above
# should be part of your experiments too.
SYSTEM_PROMPT = """\
Do something
"""


# Main ----------------------------------------------------------------------

def play_game():
    print_available_scenarios()
    game_id = create_game()
    print(f"Game created: {game_id}")
    print(f"Live map: {API_BASE}/competitions/{COMPETITION_ID}/games/{game_id}/livemap\n")
    run_agent(game_id)


def print_available_scenarios():
    scenarios = get_json(f"{API_BASE}/api/competitions/{COMPETITION_ID}/scenarios")
    print("Available scenarios:")
    for scenario in scenarios:
        scenario_id = scenario.get("scenarioId") or scenario.get("id")
        phase = scenario.get("phase", "unknown")
        print(f"  - {scenario_id} ({phase})")
    print()


def create_game():
    data = post_json(
        f"{API_BASE}/api/competitions/{COMPETITION_ID}/games",
        {"scenarioId": SCENARIO_ID, "context": "api"},
    )
    return data["gameId"]


def run_agent(game_id):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    start_result = execute_command(game_id, "start", [])
    print(f"{ENV}[environment] {start_result['message']}{RESET}")
    messages.append({"role": "user", "content": start_result["message"]})

    for _ in range(MAX_AGENT_STEPS):
        response = call_llm(messages)
        message = response["choices"][0]["message"]
        messages.append(message)

        tool_calls = message.get("tool_calls")
        if not tool_calls:
            text = message.get("content", "")
            if text:
                print(f"{AGENT}[agent] {text}{RESET}")
            messages.append({
                "role": "user",
                "content": "Use your tools to interact with the game.",
            })
            continue

        for tool_call in tool_calls:
            fn_args = json.loads(tool_call["function"]["arguments"])
            command = fn_args["command"]
            args = fn_args.get("args", [])

            print(f"{AGENT}[agent] {' '.join([command] + args)}{RESET}")
            result = execute_command(game_id, command, args)
            print(f"{ENV}[environment] {result['message']}{RESET}")

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call["id"],
                "content": result["message"],
            })

            status = result.get("gameStatus")
            if status and status != "in_progress":
                print(f"\n{ENV}Game ended: {status}{RESET}")
                return

    print(f"\n{ENV}Stopped after MAX_AGENT_STEPS={MAX_AGENT_STEPS}.{RESET}")


# HTTP helpers ---------------------------------------------------------------

def get_json(url):
    req = urllib.request.Request(
        url,
        headers={"Authorization": f"Bearer {AFC_API_KEY}"},
    )
    return open_json(req, url)


def post_json(url, body):
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode(),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {AFC_API_KEY}",
        },
    )
    return open_json(req, url)


def open_json(req, url):
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode()
        print(f"HTTP {exc.code} from {url}: {error_body}")
        raise


def execute_command(game_id, command, args):
    return post_json(
        f"{API_BASE}/api/competitions/{COMPETITION_ID}/games/{game_id}/command",
        {"command": command, "args": args},
    )


def call_llm(messages):
    body = {
        "model": MODEL,
        "max_tokens": 1024,
        "messages": messages,
        "tools": TOOLS,
    }
    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=json.dumps(body).encode(),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        },
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


if __name__ == "__main__":
    play_game()
