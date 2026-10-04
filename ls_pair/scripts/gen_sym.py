#!/usr/bin/env python3
"""Write the xschem symbols of the level-shifter pair (xschem/ls_*.sym).

Graphics are adapted from the IHP standard-cell symbols sg13cmos5l_buf_1.sym and
sg13cmos5l_inv_1.sym (Apache-2.0, Copyright 2023 IHP PDK Authors): triangle, inversion bubble,
signal leads at (+-40, 0).  The IHP cells carry VDD/VSS as properties; these level shifters need
real supply pins, so they are subcircuit symbols (type=subcircuit, netlisted as an X line from
the .sch of the same name).  Pin order = .subckt port order: do not change it.
Pin positions (symbol coordinates):
  ls_up: vss (0,30)  vddl (-10,-30)  vddh (10,-30)  out (40,0)  in (-40,0)
  ls_dn: vss (0,30)  vddl (0,-30)    out (40,0)     in (-40,0)
"""
import os
D=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','xschem')
CREDIT=["* Graphics adapted from IHP-Open-PDK sg13cmos5l_stdcells buf_1 / inv_1 symbols",
        "* Copyright 2023 IHP PDK Authors, Apache License 2.0 (https://www.apache.org/licenses/LICENSE-2.0)"]
def write(name,desc,pins,body,texts):
    o=['v {xschem version=3.4.4 file_version=1.2']+CREDIT+['}','G {}',
       'K {type=subcircuit\nformat="@name @pinlist @symname"\ntemplate="name=x1"\ndescription="'+desc+'"\n}',
       'V {}','S {}','E {}']
    o+=body
    for (pn,x,y,d) in pins: o.append(f'B 5 {x-2.5} {y-2.5} {x+2.5} {y+2.5} {{name={pn} dir={d}}}')
    o+=texts
    open(os.path.join(D,name),'w').write("\n".join(o)+"\n")
TRI=['L 4 -20 -20 -20 20 {}','L 4 -20 -20 20 0 {}','L 4 -20 20 20 0 {}','L 4 -40 0 -20 0 {}']
COMMON=['T {in} -35 -14 0 0 0.2 0.2 {}',
        'T {@name} -40 24 0 0 0.2 0.2 {}','T {@symname} 46 8 0 0 0.2 0.2 {}',
        'T {vss} 6 14 0 0 0.15 0.15 {}']
# non-inverting, three supplies: buffer triangle
write('ls_up_1v2_3v3.sym','1.2V to 3.3V level shifter (non-inverting), IHP SG13CMOS5L',
      [('vss',0,30,'inout'),('vddl',-10,-30,'inout'),('vddh',10,-30,'inout'),('out',40,0,'out'),('in',-40,0,'in')],
      TRI+['L 4 20 0 40 0 {}','L 4 0 10 0 30 {}','L 4 -10 -30 -10 -15 {}','L 4 10 -30 10 -5 {}'],
      COMMON+['T {out} 36.25 -14 0 1 0.2 0.2 {}','T {vddl} -14 -36 0 1 0.15 0.15 {}','T {vddh} 14 -36 0 0 0.15 0.15 {}'])
# inverting, vddl only: inverter triangle with bubble
write('ls_dn_3v3_1v2.sym','3.3V to 1.2V level shifter (inverting), IHP SG13CMOS5L',
      [('vss',0,30,'inout'),('vddl',0,-30,'inout'),('out',40,0,'out'),('in',-40,0,'in')],
      TRI+['L 4 30 0 40 0 {}','A 4 25 0 5 180 360 {}','L 4 0 10 0 30 {}','L 4 0 -30 0 -10 {}'],
      COMMON+['T {out} 46 -22 0 0 0.2 0.2 {}','T {vddl} 6 -36 0 0 0.15 0.15 {}'])
print('symbols written')
