v {xschem version=3.4.4 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N 320 -200 340 -200 {}
N 340 -200 340 -230 {}
N 340 -230 320 -230 {}
N 320 -100 340 -100 {}
N 340 -100 340 -70 {}
N 340 -70 320 -70 {}
N 60 -300 320 -300 {lab=vddl}
N 320 -230 320 -300 {lab=vddl}
N 60 -30 320 -30 {lab=vss}
N 320 -70 320 -30 {lab=vss}
N 280 -200 260 -200 {lab=in}
N 260 -200 260 -100 {lab=in}
N 260 -100 280 -100 {lab=in}
N 60 -150 260 -150 {lab=in}
N 320 -170 320 -130 {lab=out}
N 320 -150 500 -150 {lab=out}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 300 -200 0 0 {name=MP1
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 300 -100 0 0 {name=MN1
l=0.45u
w=0.8u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {iopin.sym} 60 -30 0 1 {name=p2 lab=vss}
C {iopin.sym} 60 -300 0 1 {name=p3 lab=vddl}
C {opin.sym} 500 -150 0 0 {name=p4 lab=out}
C {ipin.sym} 60 -150 0 0 {name=p5 lab=in}
T {ls_dn_3v3_1v2: 3.3 V -> 1.2 V level shifter, INVERTING} 60 -420 0 0 0.5 0.5 {}
T {HV inverter powered from VDDL (pattern of bidir-level-shifter bidir_channel MMP8/MMN9)} 60 -390 0 0 0.3 0.3 {}
T {in: 0..VDDH (3.0-3.6 V)   out: 0..VDDL.  Low switching threshold (~0.6 V): rise/fall delays differ by 1-2.5 ns.} 60 40 0 0 0.3 0.3 {}
