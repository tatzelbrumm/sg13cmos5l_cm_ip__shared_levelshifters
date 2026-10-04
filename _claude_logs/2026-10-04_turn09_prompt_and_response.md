# Turn 9 — 2026-10-04

## Prompt (Christoph Maier)

I hand edited the test base schematics according to my (idosyncratic) preferences.
Look at them and propose refinements of the schematic drawing skill. Same procedure as last time, before, after, difference.

Look at the other designs whether full verification suites for level shifters already exist.

Eventually, I want a CACE verification suite with PVT coverage, along the lines of the examples in single2diff2single and the _sudelbuecher class AB amplifer draft block.
For the level shifters, I'm interested in current and charge characterization, too:
What, if any, is the quiescent current from the supplies and the input?
What are current peaks at the inputs and from the supplies?
What is the charge per switching transient?
Do current and charge depend on rise and fall time of the input signal?

## Response (Claude)

Skill proposal v2 (nothing saved to the skill). Before = last turn's proposal v1, after = v2; both, and the cumulative diff against the saved skill, are in `turn09_skill_proposal/` (SKILL.before.md = saved skill, SKILL.v1.md, SKILL.v2.md, SKILL.v1_to_v2.diff, SKILL.v2_vs_saved.diff).
v2 adds a "Testbenches around the cell" section drawn from your three edited testbenches (sources left, DUT, loads right; nested supply wires; one ground bus; loads hanging below the output wire; labels on wires) and one clause in the description.

Existing verification suites for level shifters: none that is a full suite.
- bidir-level-shifter/verification: one testbench per block, tt / 27 C, screenshots and prose; level_shifter_up plots the 3.3 V supply current (about 12 nA static). No sweep, no limits.
- SAR_ADC_IHP: LS_l2h_tb / LS_h2l_tb, single-point transient, PDK paths from another machine.
- lpopamp tb_lvlshifter: a 17-point corner / VDD / temperature harness for a single-supply 1.2 -> 3.3 V cell; delay and levels only, no currents.
- CACE: no level shifter. CACE files exist for the inverter macros, lvds_tx / lvds_pattern / ring_oscillator (supply current only) and your class-AB draft (Idd, quiescent currents, mismatch and process MC). None measures charge per transition.

Current and charge, pre-layout, tt / 27 C / nominal, TR 100 ps, CL 20 fF (details in ls_pair/README.md and simulation/iq_summary.txt):
- Quiescent: ls_up 2-3 pA from VDDH, 33-53 pA from VDDL, input +-20 pA; PVT worst case 2.7 nA / 18 nA / 0.2 nA (ff, 125 C). ls_dn 35-55 fA from VDDL, input below 1 fA; PVT worst 74 pA. Not simulator gmin (checked).
- Peaks: ls_up 0.91 mA (rise) / 0.46 mA (fall) from VDDH, 226 uA from VDDL on a falling input, 301 uA into the input on a rising edge (= Cin x VDDL / TR, Cin 25 fF). ls_dn 68 uA from VDDL, 152 uA into the input (Cin 3.7 fF). Largest over PVT: 1.37 mA from VDDH.
- Charge per input edge: ls_up 275 fC (rise) / 226 fC (fall) from VDDH, of which 215 / 228 fC is intrinsic and the rest is 3.13 V x CL on the rising edge; 29 fC from VDDL on the falling edge; input +-30 fC. About 1.7 pJ per cycle at 20 fF. ls_dn 8 fC intrinsic + 1.14 V x CL from VDDL on the output rising edge; input +-12 fC.
- Dependence on TR: ls_up VDDH charge is flat to 300 ps, then 325 fC (1 ns), 453 fC (3 ns), 852 fC (10 ns); supply peaks do not depend on TR up to ~3 ns; input peak goes as 1/TR. ls_dn charge changes by less than 10 % from 20 ps to 10 ns; its peaks go as 1/TR.
- At VDDL = 1.08 V the ls_up charge rises to 335 fC - 2.35 pC (sf, -40 C: delay 6-9 ns), i.e. the cell is at the edge of its working range there; at VDDL >= 1.2 V it stays within 165-372 fC.

Not done: the CACE suite (the quantities above map to CACE parameters; say go), layout, Monte Carlo.
