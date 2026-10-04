# Turn 6 — 2026-10-04

## Prompt (Christoph Maier)

I hand edited the level shifter xschem schematics. For the level up shifter, I'm using diagonal lines. This kind of cross-coupled structure is one of the very few cases where I use diagonal wires. Look at the schematics and show what conclusions you draw for updating your drawing skill. Let me check them before you update your schematic drawing skill.

(mid-turn) Make sure you don't leave dangling git locks.

## Response (Claude)

Your edits pass the round trip: xschem netlists both cells to the same 8 and 2 devices as the reference, so the diagonals change nothing electrically. I haven't touched the skill. No git lock files are left in `levelshifters/.git`; I only ran read-only git commands there, and I won't run more.

Conclusions I would put into the skill:

1. **Diagonals only for a cross-coupled pair.** Gate stubs on the inner sides, each gate wire running diagonally to the opposite device's drain track. The two diagonals cross at their midpoints with no dot. In ls_up, M6 is flipped and M5 is not, and the X spans 80 x 60 units between the gate stubs and the drain tracks. Everything else stays orthogonal.
2. **Draw every net as a wire.** My version used lab_pin stubs for every net between columns (a, b, in, inb). You drew them all, including the long ones. Labels now only name nodes once (a, b, inb) and repeat the name at the far gate (in at M3, inb at M4).
3. **Vertical pitch.** PMOS and NMOS rows are 280 apart in yours, 100 in mine. The gap holds one horizontal track per long net (a, inb, in), with crossings without dots.
4. **Align columns by pins, not origins.** The drain pins of each branch share one x, so the drain-to-drain wire is straight. The flipped M6 therefore sits 40 units off its partner M3. Only the cross-coupled pair is mirrored; M3 and M4 are not.
5. **Bulk goes to the rail.** It jogs 20 units sideways and runs straight to the rail beside the source wire. Mine looped the bulk back to the source.
6. **Ports and notes.** Ports sit in one column at the left, at the height of the rail or input they feed. The output sits at mid-height of the output column. In the inverter the ports hug the cell. Notes go under the bottom rail, and `title.sym` with the author name goes at the bottom.

Questions before I edit the skill:
- Which other diagonal cases do you use, beyond the cross-coupled pair?
- Is repeating the net name at the far gate deliberate, or incidental?
- Is 280 a rule, or just "enough tracks"? I would write it as one 40-unit track per long net plus margins.
