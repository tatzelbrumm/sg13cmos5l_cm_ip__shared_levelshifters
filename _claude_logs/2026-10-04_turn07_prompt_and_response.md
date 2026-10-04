# Turn 7 — 2026-10-04

## Prompt (Christoph Maier)

For the level shifter symbols, look in the other chipalooza2 designs and in particular the IHP standard cell libraries for something suitable. If no 1:1 plug-in symbol exists, it may make sense to adapt an inverter symbol.

## Response (Claude)

No 1:1 plug-in symbol exists, so I adapted the IHP inverter and buffer symbols.

Where I looked:
- IHP sg13g2 / sg13cmos5l standard cells (liberty cell list and the xschem symbols): no level shifter. They have inverters, buffers, gates, flops, `slgcp`, `sighold` and tie cells.
- IHP IO library: pads only (IOPad*), no standalone shifter.
- chipalooza2: SAR_ADC_IHP, bidir-level-shifter and the lpopamp netlist contain level shifters, but their symbols are plain boxes. SAR's 1.2 -> 3.3 V symbol has exactly the pins of `ls_up` (vss vddl vddh out in); its 3.3 -> 1.2 V cell is a different circuit (inp, inn, en_hv).

What I did, in `ls_pair/`:
- `ls_up_1v2_3v3.sym`: buffer triangle from `sg13cmos5l_buf_1`; vddl and vddh on top, vss at the bottom.
- `ls_dn_3v3_1v2.sym`: inverter triangle with bubble from `sg13cmos5l_inv_1`; vddl on top, vss at the bottom.
- Both are subcircuit symbols with real supply pins, because the IHP cells carry VDD/VSS only as properties. Pin names and order are unchanged.
- `scripts/gen_sym.py` writes them. `gen_tb.py` and the three testbenches were adjusted to the new pin positions.
- `gen_cells.py` now refuses to run without `--force`, so it cannot overwrite your hand-edited `.sch` files. README updated.

Checked: both cells still netlist to the reference device by device, and the tt results are unchanged (ls_up 0.48 / 0.68 ns, ls_dn 0.07 / 1.25 ns, loopback 0.56 / 1.89 ns).

Not done: GUI check of the symbols in xschem 3.4.8, and the full 45-point PVT sweeps were not re-run (the netlists did not change). The changes are uncommitted in your git tree.
