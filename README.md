# capstone-agent — a persistent research agent on Claude Code (ME/CE/AM 295, Lab 4)

This repository is the agent. Students: on GitHub, **Use this template → Create a
new repository** (private, named `capstone-agent`), then clone it to your laptop.

| Path | Part (Lecture 7) | What it is |
|---|---|---|
| `CLAUDE.md` | 3 · memory files | Operating instructions, loaded at the start of every session; imports the two memory files |
| `memory/USER.md` | 3 · memory files | Stable preferences about you, as dated directives |
| `memory/MEMORY.md` | 3 · memory files | Curated durable facts and decisions |
| `memory/daily/` | 3 · memory files | One working note per day, appended by runs |
| `.claude/skills/beam-tools/` | 4 · skills | Lab 3 tools: `SKILL.md` + `beam_tools.py` |
| `.claude/skills/arxiv-digest/` | 4 · skills | Read-only arXiv digest: `SKILL.md` + `arxiv_digest.py` |
| `.claude/settings.json` | 6 · permissions | Pinned model; allow / ask / deny rules (enforced by Claude Code, not the model) |
| `PERMISSIONS.md` | 6 · permissions | The specification the settings enforce |
| `routine/ROUTINE_PROMPT.md` | 5 · scheduler | The cloud routine's settings and prompt |
| `digests/` | output | One digest per run, each with provenance |

Parts 1 (where it runs) and 2 (sessions) are not files here: on your laptop they
are Claude Code itself; in the cloud they are the routine and its transcripts at
claude.ai/code.

Quick check after cloning:

```bash
python3 .claude/skills/beam-tools/beam_tools.py check --span-ft 20 --w-klf 0.5 --section W8x15
# {"passes": false, "delta_in": 1.293, "limit_in": 0.667, ..., "message": "delta = 1.29 in > 0.67 in; need Ix >= 93 in4", ...}
```

Full walkthrough: the Lab 4 tutorial (Claude Code edition), Parts A–H.
