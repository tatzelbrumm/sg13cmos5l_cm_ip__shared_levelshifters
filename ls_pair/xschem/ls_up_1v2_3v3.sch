v {xschem version=3.4.4 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N 220 -200 240 -200 {}
N 240 -200 240 -230 {}
N 240 -230 220 -230 {}
N 220 -100 240 -100 {}
N 240 -100 240 -70 {}
N 240 -70 220 -70 {}
N 430 -100 450 -100 {}
N 450 -100 450 -70 {}
N 450 -70 430 -70 {}
N 430 -200 410 -200 {}
N 410 -200 410 -230 {}
N 410 -230 430 -230 {}
N 610 -200 630 -200 {}
N 630 -200 630 -230 {}
N 630 -230 610 -230 {}
N 610 -100 590 -100 {}
N 590 -100 590 -70 {}
N 590 -70 610 -70 {}
N 860 -200 880 -200 {}
N 880 -200 880 -230 {}
N 880 -230 860 -230 {}
N 860 -100 880 -100 {}
N 880 -100 880 -70 {}
N 880 -70 860 -70 {}
N 60 -340 430 -340 {lab=vddh}
N 430 -340 430 -300 {lab=vddh}
N 430 -300 860 -300 {lab=vddh}
N 430 -230 430 -300 {lab=vddh}
N 610 -230 610 -300 {lab=vddh}
N 860 -230 860 -300 {lab=vddh}
N 60 -300 220 -300 {lab=vddl}
N 220 -230 220 -300 {lab=vddl}
N 60 -30 860 -30 {lab=vss}
N 220 -70 220 -30 {lab=vss}
N 430 -70 430 -30 {lab=vss}
N 610 -70 610 -30 {lab=vss}
N 860 -70 860 -30 {lab=vss}
N 180 -200 160 -200 {lab=in}
N 160 -200 160 -100 {lab=in}
N 160 -100 180 -100 {lab=in}
N 60 -150 160 -150 {lab=in}
N 220 -170 220 -130 {lab=inb}
N 220 -150 260 -150 {lab=inb}
N 430 -170 430 -130 {lab=a}
N 430 -150 410 -150 {lab=a}
N 430 -160 550 -160 {lab=a}
N 550 -160 550 -200 {lab=a}
N 550 -200 570 -200 {lab=a}
N 610 -170 610 -130 {lab=b}
N 610 -150 630 -150 {lab=b}
N 610 -140 490 -140 {lab=b}
N 490 -140 490 -200 {lab=b}
N 490 -200 470 -200 {lab=b}
N 390 -100 370 -100 {lab=in}
N 650 -100 670 -100 {lab=inb}
N 820 -200 800 -200 {lab=a}
N 800 -200 800 -100 {lab=a}
N 800 -100 820 -100 {lab=a}
N 800 -150 780 -150 {lab=a}
N 860 -170 860 -130 {lab=out}
N 860 -150 1000 -150 {lab=out}
C {sg13cmos5l_pr/sg13_lv_pmos.sym} 200 -200 0 0 {name=M2
l=0.13u
w=1.2u
ng=1
m=1
mm_ok=1
model=sg13_lv_pmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_lv_nmos.sym} 200 -100 0 0 {name=M1
l=0.13u
w=0.6u
ng=1
m=1
mm_ok=1
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 410 -100 0 0 {name=M3
l=0.45u
w=2u
ng=1
m=4
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 450 -200 0 1 {name=M6
l=0.4u
w=2u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 590 -200 0 0 {name=M5
l=0.4u
w=2u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 630 -100 0 1 {name=M4
l=0.45u
w=2u
ng=1
m=4
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 840 -200 0 0 {name=M16
l=0.4u
w=2u
ng=1
m=2
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 840 -100 0 0 {name=M12
l=0.45u
w=2u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {lab_pin.sym} 260 -150 2 0 {name=l8 sig_type=std_logic lab=inb}
C {lab_pin.sym} 410 -150 0 0 {name=l9 sig_type=std_logic lab=a}
C {lab_pin.sym} 630 -150 2 0 {name=l10 sig_type=std_logic lab=b}
C {lab_pin.sym} 370 -100 0 0 {name=l11 sig_type=std_logic lab=in}
C {lab_pin.sym} 670 -100 2 0 {name=l12 sig_type=std_logic lab=inb}
C {lab_pin.sym} 780 -150 0 0 {name=l13 sig_type=std_logic lab=a}
C {iopin.sym} 60 -30 0 1 {name=p14 lab=vss}
C {iopin.sym} 60 -300 0 1 {name=p15 lab=vddl}
C {iopin.sym} 60 -340 0 1 {name=p16 lab=vddh}
C {opin.sym} 1000 -150 0 0 {name=p17 lab=out}
C {ipin.sym} 60 -150 0 0 {name=p18 lab=in}
T {ls_up_1v2_3v3: 1.2 V -> 3.3 V level shifter, non-inverting} 60 -420 0 0 0.5 0.5 {}
T {Netlist identical to SAR_ADC_IHP level_shifter_1v2_to_3v3 (Apache-2.0, Arjun Ananth et al.)} 60 -390 0 0 0.3 0.3 {}
T {in: 0..VDDL   out: 0..VDDH   vddl 1.08-1.32 V, vddh 3.0-3.6 V.  Needs VDDL >= 1.08 V (tt: 1.0 V).} 60 40 0 0 0.3 0.3 {}
