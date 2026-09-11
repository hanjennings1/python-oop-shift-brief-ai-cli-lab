# Shift Brief AI CLI
**Completed Sept 10, 2026** 

## Overview
A Python CLI prototype that turns messy end-of-shift notes into structured, AI-generated shift handoff briefs, and it supports revising those briefs with follow-up feedback.

Store leads write shift notes that are often messy or incomplete; this tool takes those notes and produces a clean, structured handoff brief covering:

```
Shift Summary:
Open Issues:
Action Items:
Follow-Up Questions:
Risk Notes:
```

Users can also request revisions (e.g. "make the action items more specific"), and the app uses conversation history so revisions build on the previous brief.

## Architecture

The app is split into three components, each with a single responsibility:

| File | Responsibility |
|---|---|
| `lib/ai_client.py` | `OllamaChatClient` — generic, reusable client for talking to a local Ollama chat model. Owns message history, prompt validation, the API call, response extraction, and error handling. Knows nothing about shift briefs. |
| `lib/brief_builder.py` | `HandoffBriefBuilder` — owns the shift-handoff domain logic: building create/revise prompts, checking that AI responses include the required sections, and formatting output for display. |
| `lib/shift_cli.py` | `ShiftBriefCLI` — owns the command-line experience: parsing commands, validating user input, displaying output, and routing to the brief builder. Never calls the AI service directly. |

This separation keeps the AI client reusable for other projects, keeps prompt/domain logic out of the reusable client, and keeps the CLI focused purely on user interaction.

## Setup

Install dependencies before running the app or its tests.

**Option 1: Pipenv (recommended)**
```bash
pipenv install --dev
pipenv shell
```

**Option 2: pip**
```bash
python -m pip install -r requirements.txt
```

## Running the Tests

```bash
pytest
```

The test suite mocks the AI service call, so Ollama does not need to be running to pass the tests.

## Manual Run

To try the CLI with a real model, first make sure [Ollama](https://ollama.com) is installed and running, then pull the model:

```bash
ollama pull llama3.2
```

Then start the app:

```bash
python lib/shift_cli.py
```

## Usage

```
Shift Handoff Brief CLI
Create and revise AI-assisted shift handoff briefs.

Commands:
- brief <shift notes>     Create a new handoff brief.
- revise <feedback>       Revise the previous brief using feedback.
- history                 Show the current conversation message count.
- reset                   Clear conversation history.
- help                    Show this command list.
- exit or quit            Stop the program.
```

Example session:

```
> brief Register 2 froze twice during closing. Maya restarted it, but it may need IT review tomorrow.

Shift Handoff Brief
Shift Summary:
Register 2 froze twice during closing and may need IT review...

Open Issues:
...

Action Items:
...

Follow-Up Questions:
...

Risk Notes:
...

> revise Make the action items more specific and include who should review Register 2.

Revised Shift Handoff Brief
...

> history
Conversation messages: 4

> reset
Conversation history reset.

> exit
Goodbye!
```

Generated content will vary between runs since it's produced by the model — the app checks for the required section structure rather than exact wording.

