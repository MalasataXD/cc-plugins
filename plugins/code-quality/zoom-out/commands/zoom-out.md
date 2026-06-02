---
description: Zoom out and map the modules and callers around an area of code. Usage /zoom-out [optional file, module, or area]
---
Invoke the `zoom-out` skill shipped with this plugin (`${CLAUDE_PLUGIN_ROOT}/skills/zoom-out/SKILL.md`) and apply it to the arguments below.

Arguments: `$ARGUMENTS`

Parsing rules:
1. If `$ARGUMENTS` is non-empty, treat it as the file, module, or area to zoom out on, and scope the map to its surroundings.
2. If `$ARGUMENTS` is empty, zoom out on the area of code currently in focus in the conversation.
3. Follow the skill exactly: go up a layer of abstraction and map the relevant modules and callers using the project's domain glossary vocabulary.
