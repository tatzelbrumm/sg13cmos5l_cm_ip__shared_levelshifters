# Level shifter survey for Chipalooza (SG13CMOS5L), 2026-10-03

## What was looked at
- Your `chipalooza2` folder (all 17 design folders) and the harness
  `RTimothyEdwards/sg13cmos5l_ocd_chipalooza` plus its `sg13cmos5l_ocd_ip__biasgen` submodule.
- The IHP PDK `dev` branch: the `sg13cmos5l_stdcell` (1.2 V) cell list contains **no level shifter**.
  (The `sg13cmos5l_stdcell_hv` library is not in that branch listing, so I could not check it.)
- Your own design is not in `chipalooza2`, so how many shifters you need, and in which direction, is not assessed.

## Where the candidates are
| Cell | Location | Direction |
|---|---|---|
| `level_shift` (harness) | harness `netlist/schematic/chipalooza_frame.spice`; layout `magic/level_shift.mag` and GDS inside `biasgen/gds/sg13cmos5l_ocd_ip__biasgen2.gds.gz` (Apache-2.0) | 1.2 -> 3.3 V, needs in_n and in_p |
| `level_shifter_1v2_to_3v3` | `SAR_ADC_IHP/circuit_files/{xschem,layout/Levelshifter_1.2-3.3}` | 1.2 -> 3.3 V |
| `level_shifter_3v3_to_1v2` | `SAR_ADC_IHP/circuit_files/{xschem,layout/Levelshifter_3.3-1.2}` | 3.3 -> 1.2 V, differential in + enable |
| `level_shifter_up` | `bidir-level-shifter/xschem/schematics`, `layout/level_shifter_up.gds` | 1.2 -> 3.3 V, differential out |
| HV inverter on VDDL (`MMP8/MMN9` in `bidir_channel`) | `bidir-level-shifter/xschem/schematics/bidir_channel.sch` | 3.3 -> 1.2 V |
| `lvlshifter` | `sg13cmos5l_rodovalho_ip__lpopamp/ngspice/netlists/lvlshifter.spice` | 1.2 -> 3.3 V (Schmitt style) |
| `level_shifter_xd` | `hsxo-cpz2/xschem/level_shifter_xd.sch` | 1.2 -> 3.3 V, schematic only |
| `ldo_enable`, `predriver_comp` | `sg13cmos5l_vyges_ip__ldo_capless`, `chipalooza_lvds_pll` | embedded in their blocks, not general-purpose |

None of these repos publishes measured or simulated numbers for its shifter, apart from the bidir README.

## Method
One testbench for every cell, PSP103 models copied from your `lpopamp/ngspice/models`.
Corners tt/ss/ff/sf/fs x -40/27/125 C x (VDDL, VDDH) = (1.08, 3.6), (1.2, 3.3), (1.32, 3.0) V
= 45 points per cell. Up-shift: 50 fF load, 100 ps input edges. Down-shift: 20 fF load,
500 ps input edges. Static current = average over a quiet window with the input low / high.
A point counts as functional if the output reaches 95 % / 5 % of its rail.
Pre-layout, no parasitics. `hsxo` cell and the harness `level_shift` wrapper (two LV
inverters generating in_n / in_p) were built by me; all other netlists are copied.

## Results, 1.2 -> 3.3 V
| Cell | Area | PVT pass | tplh / tphl, tt 27 C [ns] | Range over PVT [ns] | Static, tt 27 C | Static, worst | Min VDDL (tt / slow, VDDH 3.3 / 3.6) |
|---|---|---|---|---|---|---|---|
| SAR l2h | 466 um2 | 45/45 | 0.48 / 0.68 | 0.2 - 10.5 | < 0.1 nA | 18 nA | 1.00 / 1.08 V |
| harness level_shift (+2 LV inv) | 125 um2 (cell only) | 41/45 | 1.1 / 1.0 | 0.4 - 8.9 | < 0.1 nA | 20 nA | 1.04 / 1.12 V |
| bidir level_shifter_up | 244 um2 | 42/45 | 6.1 / 1.75 | 0.7 - 12.6 | 170 nA (input high) | 4.9 uA | 1.04 / 1.12 V |
| lpopamp Schmitt | netlist only | 45/45 | 0.83 / 5.4 | 0.35 - 9.1 | 25 uA (input high) | 51 uA | 0.80 / 0.84 V |
| hsxo level_shifter_xd | schematic only | fails at 1.2 V | - | - | 55 uA stuck | - | needs about 1.8 V |

Failing points: harness `level_shift` at 1.08 / 3.6 V with slow NMOS (ss, sf; -40 and 27 C);
bidir `level_shifter_up` at 1.08 / 3.6 V in ss and sf (27 and 125 C).

## Results, 3.3 -> 1.2 V
| Cell | Area | PVT pass | Delay in-rise / in-fall [ns] | Static |
|---|---|---|---|---|
| HV inverter on VDDL (inverting) | 2 HV transistors | 45/45 | 0.01 - 0.14 / 0.8 - 2.6 | < 0.1 nA |
| SAR `3v3_to_1v2` | 3975 um2 | 45/45 | 0.9 - 2.5 / 0.6 - 1.5 | up to 40 nA |

The HV inverter switches at a low input threshold, so rising and falling delays differ by
1 to 2.5 ns: expect duty-cycle distortion on clock-like signals.
HV gate oxide sees the full input swing (3.0 - 3.6 V); check that against IHP's rating.

## Layout status
- SAR cells: GDS is inside the slot 16 final submission, whose repo reports DRC (incl. official
  wrapper) and LVS as PASS.
- Harness `level_shift`: the harness's own frame LVS compares the layout and schematic of this cell as equivalent.
  (Its top level LVS still fails for unrelated reasons, per the harness README.)
- bidir `level_shifter_up.gds`: only Metal1 and no Metal2/vias, and there is no LVS run for it in the repo.

## Files here
`cells.spice` all netlists; `run.py` testbench generator; `sweep_*.py` and `analyze_up.py`;
`*_results.json` raw results. Run one at a time: two parallel ngspice runs stalled each other here.
