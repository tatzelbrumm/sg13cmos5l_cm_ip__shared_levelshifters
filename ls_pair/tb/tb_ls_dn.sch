v {xschem version=3.4.4 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {tb_ls_dn: ls_dn_3v3_1v2, 3.3 V -> 1.2 V (inverting).  PVT sweep: scripts/run_pvt.py tb_ls_dn} -300 -480 0 0 0.5 0.5 {}
C {ls_dn_3v3_1v2.sym} 420 -300 0 0 {name=x1}
C {gnd.sym} 420 -230 0 0 {name=g1 lab=GND}
N 420 -370 420 -390 {}
C {lab_pin.sym} 420 -390 0 0 {name=p2 sig_type=std_logic lab=vddl}
N 570 -300 600 -300 {}
C {lab_pin.sym} 600 -300 2 0 {name=p3 sig_type=std_logic lab=out}
N 270 -300 250 -300 {}
C {lab_pin.sym} 250 -300 0 0 {name=p4 sig_type=std_logic lab=in}
C {vsource.sym} -200 -300 0 0 {name=VL value="dc \{VDDL\}" savecurrent=false}
N -200 -330 -200 -350 {}
C {lab_pin.sym} -200 -350 0 0 {name=p5 sig_type=std_logic lab=vddl}
C {gnd.sym} -200 -270 0 0 {name=g6 lab=GND}
C {vsource.sym} -100 -300 0 0 {name=VH value="dc \{VDDH\}" savecurrent=false}
N -100 -330 -100 -350 {}
C {lab_pin.sym} -100 -350 0 0 {name=p7 sig_type=std_logic lab=vddh}
C {gnd.sym} -100 -270 0 0 {name=g8 lab=GND}
C {vsource.sym} 0 -300 0 0 {name=VIN value="PULSE(0 \{VDDH\} 10n \{TR\} \{TR\} 20n 50n)" savecurrent=false}
N 0 -330 0 -350 {}
C {lab_pin.sym} 0 -350 0 0 {name=p9 sig_type=std_logic lab=in}
C {gnd.sym} 0 -270 0 0 {name=g10 lab=GND}
C {capa.sym} 740 -300 0 0 {name=CL m=1 value=\{CLOAD\}}
N 740 -330 740 -350 {}
C {lab_pin.sym} 740 -350 0 0 {name=p11 sig_type=std_logic lab=out}
C {gnd.sym} 740 -270 0 0 {name=g12 lab=GND}
C {code_shown.sym} -300 -120 0 0 {name=CODE only_toplevel=false format="tcleval( @value )" value=".lib $::env(PDK_ROOT)/$::env(PDK)/libs.tech/ngspice/models/cornerMOSlv.lib mos_tt
.lib $::env(PDK_ROOT)/$::env(PDK)/libs.tech/ngspice/models/cornerMOShv.lib mos_tt
.temp 27
.param VDDL=1.2 VDDH=3.3 CLOAD=20f TR=500p
.tran 20p 48n
.meas tran t_rf trig v(in) val='VDDH/2' rise=1 targ v(out) val='VDDL/2' fall=1
.meas tran t_fr trig v(in) val='VDDH/2' fall=1 targ v(out) val='VDDL/2' rise=1
.meas tran voh avg v(out) from=6n to=9n
.meas tran vol avg v(out) from=26n to=29n
.meas tran ih_lo avg i(VH) from=6n to=9n
.meas tran ih_hi avg i(VH) from=26n to=29n
.meas tran il_lo avg i(VL) from=6n to=9n
.meas tran il_hi avg i(VL) from=26n to=29n
.control
pre_osdi $::env(PDK_ROOT)/$::env(PDK)/libs.tech/ngspice/osdi/psp103_nqs.osdi
run
.endc"}
