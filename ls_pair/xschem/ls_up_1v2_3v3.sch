v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {ls_up_1v2_3v3: 1.2 V -> 3.3 V level shifter, non-inverting} 70 -600 0 0 0.5 0.5 {}
T {Netlist identical to SAR_ADC_IHP level_shifter_1v2_to_3v3 (Apache-2.0, Arjun Ananth et al.)} 70 -570 0 0 0.3 0.3 {}
T {in: 0..VDDL   out: 0..VDDH   vddl 1.08-1.32 V, vddh 3.0-3.6 V.  Needs VDDL >= 1.08 V (tt: 1.0 V).} 60 -110 0 0 0.3 0.3 {}
N 180 -330 200 -330 {lab=vddl}
N 180 -180 200 -180 {lab=vss}
N 380 -180 400 -180 {lab=vss}
N 360 -460 380 -460 {lab=vddh}
N 580 -460 600 -460 {lab=vddh}
N 580 -180 600 -180 {lab=vss}
N 820 -460 840 -460 {lab=vddh}
N 820 -180 840 -180 {lab=vss}
N 180 -380 200 -380 {lab=vddl}
N 120 -330 140 -330 {lab=in}
N 120 -180 140 -180 {lab=in}
N 180 -280 520 -280 {lab=inb}
N 520 -460 540 -460 {lab=a}
N 420 -460 440 -460 {lab=b}
N 320 -180 340 -180 {lab=in}
N 520 -180 540 -180 {lab=inb}
N 760 -460 780 -460 {lab=a}
N 760 -180 780 -180 {lab=a}
N 820 -120 840 -120 {lab=vss}
N 360 -520 360 -460 {lab=vddh}
N 600 -520 600 -460 {lab=vddh}
N 840 -520 840 -460 {lab=vddh}
N 600 -120 820 -120 {lab=vss}
N 820 -150 820 -120 {lab=vss}
N 840 -180 840 -120 {lab=vss}
N 580 -520 600 -520 {lab=vddh}
N 360 -520 380 -520 {lab=vddh}
N 820 -520 840 -520 {lab=vddh}
N 820 -520 820 -490 {lab=vddh}
N 600 -520 820 -520 {lab=vddh}
N 580 -520 580 -490 {lab=vddh}
N 380 -520 380 -490 {lab=vddh}
N 380 -520 580 -520 {lab=vddh}
N 820 -320 820 -210 {lab=out}
N 200 -380 200 -330 {lab=vddl}
N 180 -380 180 -360 {lab=vddl}
N 120 -240 120 -180 {lab=in}
N 180 -280 180 -210 {lab=inb}
N 580 -150 580 -120 {lab=vss}
N 600 -180 600 -120 {lab=vss}
N 580 -120 600 -120 {lab=vss}
N 400 -180 400 -120 {lab=vss}
N 380 -150 380 -120 {lab=vss}
N 380 -120 400 -120 {lab=vss}
N 200 -120 380 -120 {lab=vss}
N 380 -360 380 -210 {lab=a}
N 580 -400 580 -210 {lab=b}
N 380 -400 440 -400 {lab=a}
N 380 -430 380 -400 {lab=a}
N 520 -400 580 -400 {lab=b}
N 580 -430 580 -400 {lab=b}
N 440 -400 520 -460 {lab=a}
N 440 -460 520 -400 {lab=b}
N 180 -300 180 -280 {lab=inb}
N 120 -240 320 -240 {lab=in}
N 320 -240 320 -180 {lab=in}
N 520 -280 520 -180 {lab=inb}
N 760 -360 760 -180 {lab=a}
N 760 -460 760 -360 {lab=a}
N 380 -360 760 -360 {lab=a}
N 380 -400 380 -360 {lab=a}
N 180 -150 180 -120 {lab=vss}
N 400 -120 580 -120 {lab=vss}
N 200 -180 200 -120 {lab=vss}
N 180 -120 200 -120 {lab=vss}
N 120 -260 120 -240 {lab=in}
N 820 -320 860 -320 {lab=out}
N 820 -430 820 -320 {lab=out}
N 80 -260 120 -260 {lab=in}
N 120 -330 120 -260 {lab=in}
N 80 -120 180 -120 {lab=vss}
N 80 -380 180 -380 {lab=vddl}
N 80 -520 360 -520 {lab=vddh}
C {sg13cmos5l_pr/sg13_lv_pmos.sym} 160 -330 0 0 {name=M2
l=0.13u
w=1.2u
ng=1
m=1
mm_ok=1
model=sg13_lv_pmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_lv_nmos.sym} 160 -180 0 0 {name=M1
l=0.13u
w=0.6u
ng=1
m=1
mm_ok=1
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 360 -180 0 0 {name=M3
l=0.45u
w=2u
ng=1
m=4
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 400 -460 0 1 {name=M6
l=0.4u
w=2u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 560 -460 0 0 {name=M5
l=0.4u
w=2u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 560 -180 0 0 {name=M4
l=0.45u
w=2u
ng=1
m=4
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 800 -460 0 0 {name=M16
l=0.4u
w=2u
ng=1
m=2
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 800 -180 0 0 {name=M12
l=0.45u
w=2u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {lab_pin.sym} 180 -260 2 0 {name=l8 sig_type=std_logic lab=inb}
C {lab_pin.sym} 380 -400 0 0 {name=l9 sig_type=std_logic lab=a}
C {lab_pin.sym} 580 -400 2 0 {name=l10 sig_type=std_logic lab=b}
C {lab_pin.sym} 320 -180 0 0 {name=l11 sig_type=std_logic lab=in}
C {lab_pin.sym} 520 -180 2 1 {name=l12 sig_type=std_logic lab=inb}
C {iopin.sym} 80 -120 0 1 {name=p14 lab=vss}
C {iopin.sym} 80 -380 0 1 {name=p15 lab=vddl}
C {iopin.sym} 80 -520 0 1 {name=p16 lab=vddh}
C {opin.sym} 860 -320 0 0 {name=p17 lab=out}
C {ipin.sym} 80 -260 0 0 {name=p18 lab=in}
C {title.sym} 160 -40 0 0 {name=l1 author="Christoph Maier"}
