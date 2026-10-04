v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {ls_dn_3v3_1v2: 3.3 V -> 1.2 V level shifter, INVERTING} 60 -420 0 0 0.5 0.5 {}
T {HV inverter powered from VDDL (pattern of bidir-level-shifter bidir_channel MMP8/MMN9)} 60 -390 0 0 0.3 0.3 {}
T {in: 0..VDDH (3.0-3.6 V)   out: 0..VDDL.  Low switching threshold (~0.6 V): rise/fall delays differ by 1-2.5 ns.} 30 -110 0 0 0.3 0.3 {}
N 290 -300 310 -300 {lab=vddl}
N 290 -360 310 -360 {lab=vddl}
N 290 -180 310 -180 {lab=vss}
N 310 -180 310 -120 {lab=vss}
N 290 -120 310 -120 {lab=vss}
N 290 -360 290 -330 {lab=vddl}
N 230 -300 250 -300 {lab=in}
N 230 -180 250 -180 {lab=in}
N 290 -150 290 -120 {lab=vss}
N 310 -360 310 -300 {lab=vddl}
N 230 -240 230 -180 {lab=in}
N 290 -240 290 -210 {lab=out}
N 190 -240 230 -240 {lab=in}
N 230 -300 230 -240 {lab=in}
N 290 -240 330 -240 {lab=out}
N 290 -270 290 -240 {lab=out}
N 190 -120 290 -120 {lab=vss}
N 190 -360 290 -360 {lab=vddl}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 270 -300 0 0 {name=MP1
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 270 -180 0 0 {name=MN1
l=0.45u
w=0.8u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {iopin.sym} 190 -120 0 1 {name=p2 lab=vss}
C {iopin.sym} 190 -360 0 1 {name=p3 lab=vddl}
C {opin.sym} 330 -240 0 0 {name=p4 lab=out}
C {ipin.sym} 190 -240 0 0 {name=p5 lab=in}
C {title.sym} 160 -40 0 0 {name=l1 author="Christoph Maier"}
