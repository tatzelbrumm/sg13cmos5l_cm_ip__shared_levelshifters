# Turn 2, 2026-10-03

## Prompt
Next step if you want it: wrap your two chosen cells into one pair with xschem symbols and a testbench.
Yes, please.

Re: screenshot
NEVER, EVER suggest creating a spreadsheet unless explicitly prompted. Consider a spreadsheet a format devised by corporate executives and therefore less than useless per definitionem.

(The screenshot showed the app's own "Create a spreadsheet" button under my previous reply.)

## Message sent while I was working
Process is the cmos5L variant of IHP sg13g2. Are you aware of it and using it? if so, carry on.

## Response
The pair is in `ls_pair/` in your chipalooza2 folder: xschem cells `ls_up_1v2_3v3` (the SAR ADC shifter) and `ls_dn_3v3_1v2` (a two-transistor HV inverter on VDDL), each with a symbol, plus three testbenches (up, down, loopback) and a PVT runner.

| | Functional (45 PVT points) | tt, 27 °C, 1.2 / 3.3 V | Worst static current |
|---|---|---|---|
| `ls_up`, 50 fF | 45/45 | 0.48 ns rise, 0.68 ns fall | 18 nA |
| `ls_dn`, 20 fF | 45/45 | out falls 0.07 ns after in rises, rises 1.25 ns after in falls | 74 pA |
| loopback | 45/45 | 0.56 / 1.89 ns end to end | – |

**What I checked**

- Both schematics netlist in xschem to exactly the source netlists, device by device. I confirmed the checker fails when I swap a net on purpose.
- The xschem testbenches reproduce my earlier survey sweep to within 1e-5.

**Things to know**

- `ls_dn` inverts and has no `vddh` port. Add an LV inverter after it if you need the same polarity. Its rise and fall delays differ by 1–2.5 ns.
- Both cells have a single `vss`; in a slot, tie `vss_1v2` and `vss_3v3` together, as the harness does.
- I simulated with the model files from your lpopamp folder, not the current IHP `dev` release (that needs a newer OSDI). The testbenches point at `$PDK_ROOT/$PDK`, so your own install is used when you run them.
- I netlisted and rendered headless with xschem 3.4.4. I have not opened the files in the GUI on your machine, and some port label text overlaps the symbols slightly.
- Not done: layout of `ls_dn`, post-layout extraction, Monte Carlo, behaviour with one supply off.

`ls_up` derives from the Apache-2.0 SAR_ADC_IHP netlist, so I copied that `LICENSE` into the folder. The README has the usage commands.

Next step if you want it: a layout of `ls_dn`.

This prompt and response are saved in `_claude_logs/2026-10-03_turn02_prompt_and_response.md`.
