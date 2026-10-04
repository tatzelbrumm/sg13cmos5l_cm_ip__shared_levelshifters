v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {tb_ls_dn: ls_dn_3v3_1v2, 3.3 V -> 1.2 V (inverting).  PVT sweep: scripts/run_pvt.py tb_ls_dn} 0 -450 0 0 0.5 0.5 {}
N 520 -400 520 -370 {lab=vddl}
N 560 -340 600 -340 {lab=out}
N 60 -160 60 -140 {lab=GND}
N 260 -180 260 -160 {lab=GND}
N 160 -160 260 -160 {lab=GND}
N 160 -180 160 -160 {lab=GND}
N 60 -180 60 -160 {lab=GND}
N 600 -180 600 -160 {lab=GND}
N 520 -160 600 -160 {lab=GND}
N 600 -340 600 -240 {lab=out}
N 520 -310 520 -160 {lab=GND}
N 60 -160 160 -160 {lab=GND}
N 160 -400 160 -240 {lab=vddl}
N 260 -340 260 -240 {lab=in}
N 60 -260 60 -240 {lab=vddh}
N 160 -400 520 -400 {lab=vddl}
N 260 -340 480 -340 {lab=in}
N 260 -160 520 -160 {lab=GND}
C {code_shown.sym} 0 -70 0 0 {name=CODE only_toplevel=false format="tcleval( @value )" value=".lib $::env(PDK_ROOT)/$::env(PDK)/libs.tech/ngspice/models/cornerMOSlv.lib mos_tt
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
C {lab_pin.sym} 260 -340 0 0 {name=p5 sig_type=std_logic lab=in}
C {ls_dn_3v3_1v2.sym} 520 -340 0 0 {name=x1}
C {lab_pin.sym} 520 -400 0 1 {name=p7 sig_type=std_logic lab=vddl}
C {lab_pin.sym} 600 -340 2 0 {name=p8 sig_type=std_logic lab=out}
C {vsource.sym} 160 -210 0 0 {name=VL value="dc \{VDDL\}" savecurrent=false}
C {lab_pin.sym} 160 -260 0 0 {name=p10 sig_type=std_logic lab=vddl}
C {gnd.sym} 60 -140 0 0 {name=g11 lab=GND}
C {vsource.sym} 60 -210 0 0 {name=VH value="dc \{VDDH\}" savecurrent=false}
C {lab_pin.sym} 60 -260 0 0 {name=p12 sig_type=std_logic lab=vddh}
C {vsource.sym} 260 -210 0 0 {name=VIN value="PULSE(0 \{VDDH\} 10n \{TR\} \{TR\} 20n 50n)" savecurrent=false}
C {lab_pin.sym} 260 -260 0 0 {name=p14 sig_type=std_logic lab=in}
C {capa.sym} 600 -210 0 0 {name=CL m=1 value=\{CLOAD\}}
C {lab_pin.sym} 600 -260 0 0 {name=p18 sig_type=std_logic lab=out}
