---
name: "xschem-analog-schematic"
description: "Draw or tidy xschem .sch schematics from a SPICE netlist, for any PDK (IHP, sky130, gf180, ...), in readable analog style, verified by netlisting back and comparing device by device."
---

# xschem-analog-schematic

Use this skill when the deliverable is an **xschem schematic** (`.sch` / `.sym`), not a figure.
For SVG/PNG figures in reports, use `analog-schematic` instead.

The skill is **process-agnostic**. Everything that depends on a PDK (symbol names, pin positions,
parameter names, how a resistor's substrate is connected) is **read from that PDK's `.sym`
files**, never assumed. The IHP and sky130 tables at the end are worked examples, not defaults.

The netlist is the source of truth. The schematic is derived from it, and it is not done until
xschem's own netlist of it matches the source **device by device**. A schematic that looks right
proves nothing: in the first session that used this skill, two bulk stubs touched and xschem
silently merged `vss` into `vdd`, and a hand edit moved two gates from `vbn` to `vss`. Only the
round-trip comparison caught them.

## Workflow

1. **Identify the PDK and its xschem library.** Find the PDK's `xschemrc`, usually
   `$PDK_ROOT/$PDK/libs.tech/xschem/xschemrc`, and the symbol directory it adds to
   `XSCHEM_LIBRARY_PATH`. Look at an existing schematic in the user's project to see how it
   references symbols, for example `sg13g2_pr/sg13_hv_nmos.sym` or
   `sky130_fd_pr/nfet_01v8.sym`, and use the same form.
2. **Build the symbol table from the `.sym` files** (see "PDK adapter"). For every device model in
   the netlist you need: the symbol file, pin names with offsets and `@pinlist` order, the
   `template` (property names and defaults) and the `format` (how xschem writes the netlist line).
   For a PDK you haven't used before, also netlist a one-device test schematic per symbol, with a
   distinct label on every pin, and check that the terminal order is what you derived.
3. **Parse the source subcircuit.** Use the `.subckt` port order, and for each device: model,
   terminal nets in SPICE order, and its parameters. Map each terminal to a symbol pin through the
   `@pinlist` order. Replace `{param}` expressions by their defaults; the schematics carry plain
   values.
4. **Plan the placement** using the style rules below: rows, columns, mirror pairs, rails. Write
   it as a `name: (x, y, rot, flip)` table before writing any file.
5. **Write the `.sch`**, with real orthogonal wires for every net that has a short route, and a
   `lab_pin` only where a wire would cross more than half the sheet. Use the property names from
   the PDK's own `template` (`w`/`l`/`ng`/`m` for IHP, `W`/`L`/`nf`/`mult` for sky130).
6. **Write the `.sym`.** Its pin order must equal the `.subckt` port order.
7. **Netlist with xschem and compare** (see Verification). Fix every mismatch before delivering.
8. **Render and look.** Use `xschem -q -x --svg --plotfile f.svg f.sch`, convert it to PNG
   (cairosvg), and open the PNG. Check that no labels overlap, rails are continuous and stacks are
   straight. Do not copy the images into the user's folders: files that pass through the app get a
   provenance stamp. Show them in the conversation only if asked.

A first pass that puts a net label on every terminal (stub plus `lab_pin`) is acceptable as a
quick, connectivity-exact draft. Say that it is a draft. The finished style below uses wires.

## Style (from Christoph Maier's hand-drawn d2s_miller / d2s_loadcomp, 2026-10-01)

These rules are about circuit structure, not about any one process.

**Sheet structure**
- Signal flows **left to right**: inputs on the left, output on the right edge.
- **All ports in one column at the far left** (x ≈ 60), ordered top to bottom by where they are
  used. The positive supply sits at the top, ground at the bottom, and each bias or input pin at
  the height of the row it feeds, so that its wire runs straight across. The output `iopin` sits
  on the **right edge**, at mid-height between the output devices.
- **Rails are wires, not labels.** The supply is one horizontal bus across the full width at the
  top, ground one bus across the bottom. Every source and bulk that goes to a rail is wired to it.

**Rows (y), all devices upright (rot 0)**
- PMOS current sources and mirror tops sit in one row just under the supply.
- PMOS cascodes go in the next row, then the signal row (input pairs, floating class-AB pairs).
- NMOS cascodes are in a row above the NMOS sinks; the sinks sit just above ground.
- Row pitch is 160–240 units. Leave horizontal routing channels between rows for long nets, such
  as the pair drains running to the folding nodes.

**Columns (x)**
- Each current branch forms **one vertical column**, rail to rail: for example, the mirror PMOS,
  its cascode, the floating pair, the NMOS cascode and the sink all share one x.
- **Differential pairs and mirrors are mirror images.** The left device is unflipped and the right
  one flipped (or the reverse), so that gates face outward for input pairs and inward for tails
  and mirrors that share a gate trunk. Pair spacing is about 220 units.
- Tail current sources sit directly above their input devices, about 40 units inside them.
- The output devices are in the rightmost column, PMOS at the top (on the supply) and NMOS at the
  bottom (on ground), with the output as a vertical trunk between them.

**Two-terminal devices**
- Degeneration resistors are horizontal, between the two sources of a pair.
- Compensation capacitors are horizontal, between the output trunk and the node they compensate.
- For a symbol whose pins sit at (0,−30) and (0,+30), "horizontal" means rot 1 or rot 3. Choose
  the one that puts the correct pin on the correct side (see Geometry).

**Wiring**
- Orthogonal only, every coordinate on the 10-unit grid, no diagonals.
- Crossings without a dot are not connections; xschem draws the dots at T-junctions.
- Bulks are wired to their source or rail, never left to a label alone. Even inside a branch, the
  PMOS bulk goes to the supply and the NMOS bulk to ground, unless the source netlist ties it
  elsewhere.

**What to avoid** (each of these was seen)
- Net-label soup: one label per terminal, with names colliding ("vbpvbp", "vddvss").
- Bulk or gate stubs from neighbouring devices that touch. xschem joins touching wire ends and
  labels, which merges nets **silently**.
- Leftover labels under a hand-drawn wire. They are harmless only while they agree with the wire;
  once someone edits the wire, they keep the old connection alive.

## Geometry (xschem 3.4; holds for every PDK)

- Instance placement is `C {sym} x y rot flip {props}`, and the pin position is
  `(x, y) + T(pin offset)`.
- **Flip negates x** of the pin offset in symbol coordinates (y points down). Then rotation,
  for an offset (x, y): rot 1 → (−y, x), rot 2 → (−x, −y), rot 3 → (y, −x).
  These rules were checked against hand-drawn files for rot 0/1/3 and for flip on MOS devices.
- Wires are `N x1 y1 x2 y2 {lab=net}`. The `lab` on a wire is only a hint; connectivity comes
  from geometry. Any wire end or pin that touches another joins the nets.
- Generic symbols come from xschem's own `devices/` library and are the same for every PDK:
  `lab_pin`, `ipin`, `opin`, `iopin` (pin at (0,0); `lab_pin` text sits left of the pin,
  `flip=1` puts it right), `isource` (p (0,−30), m (0,30); current flows p → m inside the
  source, as in SPICE `I p m`), and `title`.

## PDK adapter: read the symbols, don't assume them

For each symbol you use, parse the `.sym` file:

```python
import re
def sym_info(path):
    s = open(path).read()
    k = re.search(r'^K \{(.*?)\n\}', s, re.M | re.S) or re.search(r'^K \{(.*?)\}', s, re.M | re.S)
    kb = k.group(1) if k else ''
    typ = re.search(r'type=(\S+)', kb)
    fmt = re.search(r'\bformat="([^"]*)"', kb)
    tpl = re.search(r'\btemplate="([^"]*)"', kb)
    pins = []
    for m in re.finditer(r'^B 5 ([-\d.e]+) ([-\d.e]+) ([-\d.e]+) ([-\d.e]+) \{([^}]*)\}', s, re.M):
        x1, y1, x2, y2 = map(float, m.group(1, 2, 3, 4))
        a = dict(re.findall(r'(\w+)=(\S+)', m.group(5)))
        pins.append((a.get('name'), (x1 + x2) / 2, (y1 + y2) / 2, a.get('sim_pinnumber')))
    return dict(type=typ and typ.group(1), format=fmt and fmt.group(1),
                template=tpl and tpl.group(1), pins=pins)
```

- **Pins** are the `B 5` boxes (layer 5). The box centre is the connection point, and `name=` is
  the pin name.
- **`@pinlist` order**, which is the order of terminals on the netlist line, is the order of the
  `B 5` lines in the file, unless the pins carry `sim_pinnumber`, which then wins. Never assume
  D G S B; take it from the file. In sky130's `res_high_po` the box order is M, P, B.
- **`template`** gives the property names and their defaults; copy them and set the values from
  the netlist. **`format`** shows the netlist line. Check it for a model prefix that xschem adds
  (sky130 writes `sky130_fd_pr__@model`, so the schematic's `model=` holds the short name) and
  for terminals that are attributes rather than pins.
- **Substrate and bulk differ by PDK.** A three-terminal resistor may have a real bulk pin
  (sky130 `res_high_po`: pin B) or a `body=` attribute that is pasted into the pin list (IHP
  `rhigh`: `@pinlist @body`, default `sub!`). Wire a pin; set an attribute to the netlist's net
  name.
- **Device names.** Most PDK templates use `spiceprefix=X`, so xschem writes `X<name>`. Compare
  by instance name with the prefix stripped.

### Worked examples (read from the symbols, 2026-10-01)

The IHP rows were confirmed by round-trip netlisting of full schematics. Of the sky130 rows,
`pfet_01v8` and `res_high_po` were confirmed by netlisting one-device schematics; `nfet_01v8` and
`cap_mim_m3_1` were only read from their symbols.

| PDK, symbol | type | pins (name: offset) in `@pinlist` order | parameter names |
|---|---|---|---|
| IHP `sg13cmos5l_pr/sg13_hv_nmos` (`_lv_`, `sg13g2_pr/` same) | nmos | D (20,−30), G (−20,0), S (20,30), B (20,0) | `w l ng m`, `model=sg13_hv_nmos` |
| IHP `sg13_hv_pmos` | pmos | S (20,−30), G (−20,0), D (20,30), B (20,0) — **source on top** | same |
| IHP `rhigh` / `rppd` / `rsil` | res | P (0,−30), M (0,30); substrate = `body=` attribute | `w l b m` |
| IHP `cap_cmomi` / `cap_cmomf` | capacitor | c0 (0,−30), c1 (0,30) | `w l mmin mmax feed` |
| sky130 `sky130_fd_pr/nfet_01v8` | nmos | D (20,−30), G (−20,0), S (20,30), B (20,0) | `W L nf mult`, prefix `sky130_fd_pr__` |
| sky130 `pfet_01v8` | pmos | D (20,30), G (−20,0), S (20,−30), B (20,0) — pin **order** D G S B, source on top | same |
| sky130 `res_high_po` | resistor | M (0,30), P (0,−30), B (−20,0) — **bulk is a pin**, order M P B | `W L mult` |
| sky130 `cap_mim_m3_1` | capacitor | c0 (0,−30), c1 (0,30) | `W L MF` |

The IHP pmos lists S before D, while the sky130 pfet lists D first, with the same geometry. That
is exactly the kind of difference that makes a hard-coded D G S B order wrong for one of them.

## Verification

- Netlist each schematic with xschem in batch mode:
  `xschem --rcfile <dir>/xschemrc -n -s -q -x -o <dir>/net <dir>/<cell>.sch`
  - Use **absolute paths and set `PWD`** in the subprocess environment. xschem resolves relative
    names against `$PWD`, not against the working directory of the process. A wrong `PWD`
    silently netlists an empty schematic.
  - **Delete the old netlist first**, so that a failed run cannot be compared as if it were fresh.
  - **Don't treat the exit status as pass/fail.** xschem 3.4.8 has returned 10 while writing a
    complete netlist. Print the status and xschem's messages, then compare whatever was written.
- Parse xschem's netlist (`X…`/`M…`/`R…`/`C…`/`I…` lines; the `**.subckt` header gives the port
  order). Compare per device: model (allowing for a prefix the `format` adds), terminal nets
  **in `@pinlist` order** mapped back to the source's terminal order, the sizing parameters, and
  the port order. Report every difference and exit non-zero if there is any.
- Sanity-check the checker once by changing one label in a copy and confirming that it fails.
- Port order: in hierarchical use, xschem takes the port order from the **`.sym`**, for both
  the instance line and the `.subckt` definition it writes. The order of pin instances in the
  `.sch` is ignored there. This was checked with xschem 3.4.4: a parent schematic was netlisted
  with the child's pins in two different `.sch` orders, and the result was identical. The `.sch`
  order matters only when the schematic is netlisted **stand-alone** as the top level; then
  xschem orders the `**.subckt` header by the order of the pin instances in the file. Deleting
  and re-placing a pin, or cut-and-paste, moves it to the end or the front. Keep the `.sym`
  equal to the source netlist (it is what parents use), and keep the `.sch` in the same order so
  that stand-alone netlists stay usable.

Reference implementations (IHP-specific symbol table; replace it with a `sym_info` lookup when
porting): `gen_xschem.py` (label-draft generator) and `check_xschem.py` (round-trip comparison)
in `sg13cmos5l_cm_ip__single2diff2single_sudelbuecher/sudelbuecher/design_considerations/class_ab_pad_driver/`.

## Environment notes

- Set `PDK_ROOT` and `PDK` (for example `ihp-sg13cmos5l`, `sky130A`, `gf180mcuD`). A minimal
  project `xschemrc` that sources `$PDK_ROOT/$PDK/libs.tech/xschem/xschemrc` and appends its own
  directory is enough. Some PDKs (sky130 via open_pdks) also need their own library directory,
  such as `xschem_sky130`, on the path; check what the PDK's `xschemrc` appends.
- `devices/lab_pin.sym`-style references resolve only if `…/xschem_library` itself (not just
  `…/xschem_library/devices`) is on `XSCHEM_LIBRARY_PATH`. If labels don't name their nets,
  the netlist shows `net1, net2, …`; check the path before anything else.
- In a cloud container without the user's toolchain, `apt-get install xschem` works (3.4.4).
  PDK symbol libraries can be cloned from GitHub (IHP-Open-PDK, `dev` branch for sg13cmos5l;
  `StefanSchippers/xschem_sky130`). Rendering and netlisting work headless with `-q -x`.