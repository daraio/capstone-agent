---
name: beam-tools
description: Size or check a simply supported steel W-section beam for a uniform load from a small AISC catalogue (Lab 3 tools). Deterministic; every number comes from the script.
allowed-tools: Bash(python3 ${CLAUDE_SKILL_DIR}/beam_tools.py *)
---

# Beam tools (Lab 3, as a skill)

Use this skill whenever the user asks to size, check, or compare a simply
supported steel W-section for a uniform load. Never compute a deflection,
stress, or section property yourself: run the script and report its numbers,
with their inputs. If a section is not in the catalogue the script says so;
do not substitute one from memory.

## Commands

List the catalogue:

```bash
python3 ${CLAUDE_SKILL_DIR}/beam_tools.py candidates
```

Section properties:

```bash
python3 ${CLAUDE_SKILL_DIR}/beam_tools.py lookup --section W12x26
```

Deflection against L/360:

```bash
python3 ${CLAUDE_SKILL_DIR}/beam_tools.py deflection --span-ft 20 --w-klf 0.5 --section W12x26
```

Full check (deflection and bending stress — the Checker from Lecture 6):

```bash
python3 ${CLAUDE_SKILL_DIR}/beam_tools.py check --span-ft 20 --w-klf 0.5 --section W12x26
```

## How to answer a sizing request

1. Run `candidates`.
2. Starting from the lightest section, run `check` until one passes.
3. Report the lightest passing section, its `delta_in`, `stress_ksi`, and the
   `inputs` block verbatim. Mention any lighter section that also passed.
4. If none passes, say so and report the `message` of the last attempt.

## May not

- Invent a section or a property not returned by the script.
- Report a result without its `inputs`.
- Change load, span, or limits the user did not state.
