# MiniMax H3 Director OS - Director Brain

## Purpose

Director Brain converts raw story input into cinematic decisions before prompt generation.

## Pipeline

Story Analysis -> Visual Intent -> Case Retrieval -> Shot Planning -> Prompt Compilation

## Rules

1. Never generate a prompt before director analysis.
2. Define the purpose of every shot.
3. Decide audience focus before camera selection.
4. Prefer one emotional objective per shot.

## Output

- directorDecision
- recommendedCases
- shotStrategy
