# MiniMax H3 Director OS v3.0.0-alpha Package

## Overview

This is the complete MiniMax H3 Director Skill Package.

It converts story ideas into structured cinematic video prompts through a director workflow.

## Package Structure

```
package/
├── SKILL.md
├── director.json
├── core/
├── compiler/
├── schema/
├── cases/
├── patterns/
├── failures/
└── examples/
```

## Core Workflow

```
Story Input
    ↓
Director Brain
    ↓
Scene Analysis
    ↓
Shot Planning
    ↓
Prompt Compiler
    ↓
MiniMax H3 Generation
```

## H3 Production Rules

### Single Action Principle

One prompt describes one primary action.

Example:

Good:

```
She opens the door and slowly turns back.
```

Avoid:

```
She opens the door, walks across the room, sits down and starts typing.
```

### Camera Language

Define:

- push in
- pull back
- tracking shot
- handheld movement
- aerial shot

### Audio Design

Include:

- environment sound
- action sound
- dialogue
- atmosphere

### Continuity Control

Use:

- character memory
- scene memory
- style memory

### Speaker Lock

For dialogue scenes:

- only active speaker performs mouth movement
- listener remains silent
- maintain character ownership

## Import

Use `SKILL.md` as the main skill definition.

Use `director.json` for structured generation configuration.

## Included Modules

- Director Brain
- Prompt Compiler
- Shot Planner
- Quality Gate
- Character Continuity Rules
- Case Library
- Camera Patterns
- Audio Patterns
- Lighting Patterns
- Failure Prevention Rules
