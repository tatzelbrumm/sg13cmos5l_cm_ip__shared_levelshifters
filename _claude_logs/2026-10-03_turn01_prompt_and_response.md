# Turn 1, 2026-10-03

## Prompt
Looking at the chipalooza 2026 submission, a loose end of lots of designs, with the exception of a handful of the most sophisticated designs, is to have some "auxiliary" digital control logic between the digital signals from the harness and the analog/mixed signal main contents in every slot.
Level shifters are a recurring problem. Look at the designs in chipalooza2 and the harness, https://github.com/RTimothyEdwards/sg13cmos5l_ocd_chipalooza
for small level shifter (primarily 1.2V to 3…V, also in the other direction) cells, preferably that are well characterized, to integrate into any design that need it, in particular mine.

After every turn, download my prompt and your response in a directory on my computer.

## Messages sent while I was working
1. Seems that several chats have uploaded ngspice, the IHP PDK and other circuit design tools separately. Can this double work be avoided by skills, or is you cloud organized so that every chat is on their own?
2. Do not use Microsoft text or spreadsheet formats for presenting results. Don't even suggest it.
3. I think that in CACE, there's something like a -j option and other options that prevent simulation runs, in particular ngspice, to remain in busy wait state. could these solve the slow simulation problem or are you already aware of these options? Anyhow, carry on.

## Response
**Bottom line**

The PDK's 1.2 V stdcell list has no level shifter, so the usable cells are scattered across the designs. None of the repos publishes numbers for its shifter, so I simulated them all in one testbench using your PDK models: 5 corners × −40/27/125 °C × three supply pairs (1.08/3.6, 1.2/3.3, 1.32/3.0 V), 45 points per cell. Pre-layout, no parasitics.

**1.2 → 3.3 V**

| Cell (where) | Area | PVT pass | Delay tt/27 °C, up/down | Static current | Min VDDL |
|---|---|---|---|---|---|
| SAR ADC `level_shifter_1v2_to_3v3` | 466 µm² | 45/45 | 0.5 / 0.7 ns | < 0.1 nA (max 18 nA) | 1.0 V (1.08 V slow corners) |
| Harness `level_shift` (biasgen submodule) | 125 µm², needs in_n and in_p | 41/45 | 1.1 / 1.0 ns | < 0.1 nA (max 20 nA) | 1.04 V (1.12 V slow corners) |
| bidir `level_shifter_up` | 244 µm², layout looks unrouted | 42/45 | 6.1 / 1.8 ns | 170 nA, up to 4.9 µA hot | 1.04–1.12 V |
| lpopamp Schmitt `lvlshifter` | netlist only | 45/45 | 0.8 / 5.4 ns | 25 µA while input is high | 0.8 V |
| hsxo-cpz2 `level_shifter_xd` | schematic only | fails at 1.2 V | – | – | needs about 1.8 V |

**3.3 → 1.2 V**

- **HV inverter powered from VDDL** (the `MMP8/MMN9` pair in bidir-level-shifter): two HV transistors, 45/45 pass, no static current. It inverts, and its low switching threshold skews rising and falling delays by 1–2.5 ns, so expect duty-cycle distortion on clocks.
- **SAR `level_shifter_3v3_to_1v2`**: 45/45 pass, 0.6–2.5 ns, but about 3,975 µm² and needs a differential input plus enable. Overkill for control signals.

**What I'd use**

- **1.2 → 3.3 V:** the SAR cell. It is the only one that passes every point, and its GDS is inside the slot 16 submission, which reports DRC and LVS as PASS.
- **Smaller option:** the harness `level_shift` is a quarter of the size and its layout is already LVS-equivalent in the harness frame. It fails at 1.08 V / 3.6 V with slow NMOS, so it is only safe if VDDL stays at or above about 1.2 V.
- **3.3 → 1.2 V:** the HV inverter.

**Caveats**

- I rebuilt the hsxo cell from its schematic, so its failure is my model of it.
- The 3.6 V gate stress on the HV inverter is not checked against IHP's rating.
- Your own design isn't in `chipalooza2`, so I don't know how many shifters you need or in which direction.

Next step if you want it: wrap your two chosen cells into one pair with xschem symbols and a testbench.

The notes, netlists, scripts and raw results are in `_claude_logs/level_shifter_survey/` inside your chipalooza2 folder. This prompt and response are saved in `_claude_logs/2026-10-03_turn01_prompt_and_response.md`.

Sources: [harness repo](https://github.com/RTimothyEdwards/sg13cmos5l_ocd_chipalooza), [biasgen submodule](https://github.com/RTimothyEdwards/sg13cmos5l_ocd_ip__biasgen), [IHP-Open-PDK](https://github.com/IHP-GmbH/IHP-Open-PDK), and the designs in your chipalooza2 folder.
