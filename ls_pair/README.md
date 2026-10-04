# ls_pair: 1.2 V <-> 3.3 V level shifter pair for IHP SG13CMOS5L

Two small cells with xschem symbols, three testbenches, and a PVT runner.
Built 2026-10-03 from the survey in `../level_shifter_survey/`.

| Cell | Direction | Ports (order) | Devices | Source |
|---|---|---|---|---|
| `ls_up_1v2_3v3` | 1.2 -> 3.3 V, non-inverting | `vss vddl vddh out in` | 2 LV + 6 HV MOS | netlist of `SAR_ADC_IHP` `level_shifter_1v2_to_3v3` (Apache-2.0, Arjun Ananth et al.) |
| `ls_dn_3v3_1v2` | 3.3 -> 1.2 V, **inverting** | `vss vddl out in` | 2 HV MOS | HV inverter on VDDL, the `MMP8`/`MMN9` pattern in `bidir-level-shifter` `bidir_channel` |

`ls_dn` has no `vddh` port: the 3.3 V domain only supplies the input signal.
For a non-inverting down-shift follow it with an LV inverter (e.g. `sg13cmos5l_inv_1`) on VDDL.

## Results (pre-layout, no parasitics, tt/ss/ff/sf/fs x -40/27/125 C x (VDDL,VDDH) = (1.08,3.6), (1.2,3.3), (1.32,3.0) V)

| | Functional | Delay at tt, 27 C, 1.2/3.3 V | Delay over all 45 points | Static current, worst |
|---|---|---|---|---|
| `ls_up`, 50 fF | 45/45 | 0.48 ns rise, 0.68 ns fall | 0.2 - 7.1 ns rise, 0.35 - 10.5 ns fall | 18 nA |
| `ls_dn`, 20 fF, 500 ps input edges | 45/45 | out falls 0.07 ns after in rises, out rises 1.25 ns after in falls | 0.01 - 0.14 ns / 0.8 - 2.6 ns | 74 pA |
| loopback up + dn | 45/45 | 0.56 ns / 1.89 ns | 0.3 - 7.1 ns / 1.1 - 12.0 ns | - |

Minimum VDDL for `ls_up` (from the survey sweep, 27 C): 1.0 V at tt / 3.3 V, 1.08 V at ss and sf / 3.6 V.
`ls_dn` has a low switching threshold (about 0.6 V at the input), so rising and falling delays differ by 1 - 2.5 ns:
expect duty-cycle distortion on clock-like signals. Its HV gates see the full input swing (3.0 - 3.6 V):
check that against IHP's gate-oxide rating for your supply tolerance.

## Current and charge (pre-layout, `scripts/run_iq.py`, `scripts/analyze_iq.py`, results in `simulation/iq_*`)
One rising and one falling input edge, input transition time TR, CL = 20 fF. Positive = delivered by the source.
Charges are net of the pre-edge current; cross-checked against an independent integration of the waveforms (0.5 %).

| | ls_up (VDDL 1.2 V, VDDH 3.3 V, tt, 27 C, TR 100 ps) | ls_dn (VDDL 1.2 V, input 3.3 V) |
|---|---|---|
| quiescent, VDDH | 2 - 3 pA (45-point PVT: 0 .. 2.7 nA, worst ff/125 C) | no VDDH pin |
| quiescent, VDDL | 33 - 53 pA (PVT: up to 18 nA at ff/125 C, input high) | 35 - 55 fA (PVT: up to 74 pA) |
| quiescent, input | +-20 pA (PVT: up to 0.2 nA) | below 1 fA (simulator resolution) |
| charge from VDDH per input edge | 275 fC rising, 226 fC falling; 215 / 228 fC + 3.13 V x CL (rising) intrinsic | - |
| charge from VDDL per input edge | -0.9 fC rising, 29.4 fC falling (the LV inverter output node `inb` rising) | -3.9 fC rising, 31.9 fC falling = 8.4 fC + 1.14 V x CL |
| charge into the input per edge | +30 fC / -30 fC (25 fF x 1.2 V) | +12 fC / -12 fC (3.7 fF x 3.3 V) |
| peak current from VDDH (rise / fall) | 0.91 mA / 0.46 mA, independent of TR up to ~3 ns | - |
| peak current from VDDL (rise / fall) | 6 uA / 226 uA | 5 uA / 68 uA |
| peak input current (rise) | 301 uA = Cin x VDDL / TR; a residual peak of ~50 uA remains for TR >= 1 ns (cause not investigated) | 152 uA, scales with 1/TR |

Dependence on input transition time (tt, 27 C): ls_up VDDH charge on a rising input is flat up to TR = 300 ps
(273 - 284 fC), then 325 fC at 1 ns, 453 fC at 3 ns, 852 fC at 10 ns (growing roughly linearly with TR: current flows while
the input is slowly crossing its mid range); falling input 216 - 291 fC. ls_dn VDDL charge changes by less than 10 % from 20 ps to 10 ns;
its peaks scale with 1/TR. Input charge is C x V for all TR; only its peak scales.
Over the 45 PVT points the VDDH charge at VDDL >= 1.2 V is 165 - 372 fC (rising) and 127 - 342 fC (falling); at
VDDL = 1.08 V it is 335 fC - 2.35 pC (rising) and 310 fC - 3.28 pC (falling); the 2.35 pC point (sf, -40 C, 1.08 / 3.6 V) has tplh = 6.1 ns, tphl = 9.0 ns: the cell is at the edge of
its working range there. Largest peaks: 1.37 mA from VDDH (ff, -40 C, 1.32 / 3.0 V).
Quiescent values were checked against the simulator's gmin (1e-12 / 1e-15 / 1e-18): no change. Values below ~1 pA
are model leakage at the edge of what the solver resolves (abstol 1 fA).

## Symbols
Neither the IHP standard-cell library (no level-shifter cell among its sg13g2 / sg13cmos5l cells) nor the IHP IO
library (pads only) has a level shifter, and the symbols in the other chipalooza2 designs are plain boxes. The two
symbols are therefore adapted from the IHP `sg13cmos5l_buf_1` / `inv_1` symbols (Apache-2.0): a buffer triangle
for `ls_up` (vddl, vddh on top, vss at the bottom), an inverter triangle with bubble for `ls_dn`.
Unlike the IHP cells they carry real supply pins and are subcircuit symbols (`type=subcircuit`, netlisted as an
`X` line to the `.sch` of the same name). Pin names and order are unchanged: `ls_up` has the pins of the SAR_ADC_IHP
`level_shifter_1v2_to_3v3`, so the two are interchangeable by pin name.

## Files
```
xschemrc            sources $PDK_ROOT/$PDK xschemrc (default PDK=ihp-sg13cmos5l), adds xschem/ and tb/
xschem/             ls_up_1v2_3v3.{sch,sym}  ls_dn_3v3_1v2.{sch,sym}
tb/                 tb_ls_up.sch  tb_ls_dn.sch  tb_ls_loop.sch   (xschem testbenches, ngspice)
netlist/            plain SPICE subcircuits netlisted by xschem
scripts/            gen_sym.py (symbols), gen_tb.py (testbenches), check_netlist.py, run_pvt.py,
                    run_iq.py + analyze_iq.py (current and charge),
                    gen_cells.py (original .sch generator; refuses to run: the .sch were hand-edited since)
simulation/         PVT results of this run (tb_*_pvt.json / .log), current and charge (iq_*.json, iq_summary.txt)
```

## Use
```sh
export PDK_ROOT=/foss/pdks PDK=ihp-sg13cmos5l      # your PDK install
cd ls_pair && xschem tb/tb_ls_loop.sch              # then Netlist, Simulate
python3 scripts/check_netlist.py                    # xschem netlist vs source, device by device
python3 scripts/run_pvt.py tb_ls_up                 # 45-point PVT sweep (add --quick for tt only)
```
The testbenches load `$PDK_ROOT/$PDK/libs.tech/ngspice/models/cornerMOS{lv,hv}.lib` and the PSP103 OSDI
`$PDK_ROOT/$PDK/libs.tech/ngspice/osdi/psp103_nqs.osdi`. Adjust that path if your install differs.
To use the cells in a design, copy `xschem/ls_*` into its xschem library, or add this `xschem/` folder to
`XSCHEM_LIBRARY_PATH`. Use one `vss` net for both cells; the harness shorts `vss_1v2` and `vss_3v3` in the frame.

## What was verified, and what was not
- Both schematics netlist in xschem to exactly the source netlists (model, terminals, w/l/ng/m, port order).
  The checker was confirmed to fail when a net is swapped deliberately.
- Testbench results reproduce the survey sweep to within 1e-5 relative.
- **Models:** simulated with the cmos5l model files from `sg13cmos5l_rodovalho_ip__lpopamp/ngspice/models`
  and its PSP103 OSDI, not with the current IHP `dev` branch release (which needs a newer OSDI).
  Corner parameter values (tt/ss/ff) agree with the `dev` files; the device model cards were not diffed.
- Not done: layout of `ls_dn`, post-layout extraction, Monte Carlo, behaviour with one supply off,
  ESD or latch-up checks. The GDS of `ls_up` exists in `SAR_ADC_IHP/circuit_files/layout/Levelshifter_1.2-3.3/`
  (466 um2, DRC/LVS clean inside the slot 16 submission).

## Licence
`ls_up` is derived from the SAR_ADC_IHP netlist (Apache-2.0); see `LICENSE`.
