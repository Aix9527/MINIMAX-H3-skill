# Prompt Validation Test

## Required Prompt Blocks

Every generated H3 prompt should contain:

- Reference Lock
- Scene
- Subject
- Single Action
- Camera Movement
- Lighting
- Audio
- Timing
- Ending Frame
- Constraints

## Failure Conditions

Reject when:

- multiple unrelated actions exist in one shot
- camera movement is missing
- ending frame is undefined

Status: RC1 Ready
