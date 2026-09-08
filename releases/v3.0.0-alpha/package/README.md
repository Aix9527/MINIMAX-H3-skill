# MiniMax H3 Director OS v3.0.0-alpha Package

## Overview

This is the complete MiniMax H3 Director Skill Package.

It converts story ideas into structured cinematic video prompts through an AI director workflow.

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
Story Analysis
    ↓
Character / Scene Memory
    ↓
Shot Planning
    ↓
Prompt Compiler
    ↓
Quality Gate
    ↓
MiniMax H3 Generation
```

## H3 Production Rules

### 1. Single Action Principle

One prompt describes one primary action.

Good:

```
She opens the door and slowly turns back.
```

Avoid:

```
She opens the door, walks across the room, sits down and starts typing.
```

Complex scenes should be split into multiple shots.

### 2. Camera Language

Every shot should define camera behavior:

- push in
- pull back
- tracking shot
- handheld movement
- aerial shot
- close-up
- over-the-shoulder

### 3. Audio Design

Use native H3 audio generation:

- environment sound
- action sound
- atmosphere
- dialogue

### 4. Continuity Control

Maintain:

- character memory
- scene memory
- style memory
- costume consistency
- prop consistency

### 5. Speaker Lock

Dialogue scenes use ownership control:

- only active speaker moves mouth
- listener remains silent
- prevent speaker swap
- preserve character identity

### 6. Visual Style Control

Define:

- lighting
- color palette
- lens feeling
- cinematic mood
- pacing

## Import

Use `SKILL.md` as the main skill definition.

Use `director.json` for structured generation configuration.

## Included Modules

- Director Brain
- Story Analyzer
- Prompt Compiler
- Shot Planner
- Quality Gate
- Character Continuity Rules
- Scene Memory System
- Case Library
- Camera Patterns
- Audio Patterns
- Lighting Patterns
- Failure Prevention Rules
- Production Examples

## Version

MiniMax H3 Director OS v3.0.0-alpha
