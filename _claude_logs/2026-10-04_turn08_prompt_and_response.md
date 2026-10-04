# Turn 8 — 2026-10-04

## Prompt (Christoph Maier)

Good choice of symbols. I just need to think how to distinguish level shifting blocks from standard cells in the schematic.

Show me the skill text, before and after your proposed changes.
The difference in vertical pitch is due to the special situation that there are two VDD power rails.
Align columns by pins is a good guideline.
Bulk goes to the rail is a particularly good heuristic if the bulk connects to substrate by default. From there, it's nice if bulk connections to nmos and pmos follow the same rule, unless the schematic emphasises the difference of bulk connections.
I'm not sure about the use of the title.sym quite yet.

## Response (Claude)

Proposal for the xschem-analog-schematic skill, not yet saved. The full before / after / diff files are in `_claude_logs/turn08_skill_proposal/` (SKILL.before.md, SKILL.after.md, SKILL.diff). The diff is reproduced in the reply of this turn.

How your comments went in:
- Vertical pitch: dropped my "one track per net" explanation. The skill now says a second positive supply adds a rail and a PMOS row of its own, which is why such cells are taller.
- Align columns by pins: in as written.
- Bulk: wire to the rail when the bulk is tied to its supply by default; NMOS and PMOS the same; deviations drawn deliberately when the schematic wants to show a different bulk connection.
- `title.sym`: left out.

Still open: whether repeating a net name at the far end of a long wire belongs in the skill (I left it out), and how to mark level shifters in a schematic (the new Symbols section says nothing on that).
