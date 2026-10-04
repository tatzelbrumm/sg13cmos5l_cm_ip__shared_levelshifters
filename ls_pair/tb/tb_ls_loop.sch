v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {tb_ls_loop: 1.2 V -> ls_up -> 3.3 V node h -> ls_dn -> 1.2 V (net inversion)} 0 -480 0 0 0.5 0.5 {}
N 530 -400 530 -370 {lab=vddl}
N 700 -400 700 -370 {lab=vddl}
N 740 -340 780 -340 {lab=out}
N 80 -160 80 -140 {lab=GND}
N 280 -180 280 -160 {lab=GND}
N 180 -160 280 -160 {lab=GND}
N 180 -180 180 -160 {lab=GND}
N 80 -180 80 -160 {lab=GND}
N 620 -180 620 -160 {lab=GND}
N 780 -180 780 -160 {lab=GND}
N 540 -160 620 -160 {lab=GND}
N 700 -160 780 -160 {lab=GND}
N 780 -340 780 -240 {lab=out}
N 620 -340 660 -340 {lab=h}
N 620 -340 620 -240 {lab=h}
N 580 -340 620 -340 {lab=h}
N 700 -310 700 -160 {lab=GND}
N 620 -160 700 -160 {lab=GND}
N 540 -310 540 -160 {lab=GND}
N 280 -160 540 -160 {lab=GND}
N 80 -160 180 -160 {lab=GND}
N 550 -420 550 -370 {lab=vddh}
N 530 -400 700 -400 {lab=vddl}
N 180 -400 530 -400 {lab=vddl}
N 180 -400 180 -240 {lab=vddl}
N 80 -420 550 -420 {lab=vddh}
N 80 -420 80 -240 {lab=vddh}
N 280 -340 500 -340 {lab=in}
N 280 -340 280 -240 {lab=in}
C {ls_up_1v2_3v3.sym} 540 -340 0 0 {name=x1}
C {lab_pin.sym} 550 -420 2 0 {name=p3 sig_type=std_logic lab=vddh}
C {lab_pin.sym} 280 -340 0 0 {name=p5 sig_type=std_logic lab=in}
C {ls_dn_3v3_1v2.sym} 700 -340 0 0 {name=x2}
C {lab_pin.sym} 700 -400 0 1 {name=p7 sig_type=std_logic lab=vddl}
C {lab_pin.sym} 780 -340 2 0 {name=p8 sig_type=std_logic lab=out}
C {vsource.sym} 180 -210 0 0 {name=VL value="dc \{VDDL\}" savecurrent=false}
C {lab_pin.sym} 180 -260 0 0 {name=p10 sig_type=std_logic lab=vddl}
C {gnd.sym} 80 -140 0 0 {name=g11 lab=GND}
C {vsource.sym} 80 -210 0 0 {name=VH value="dc \{VDDH\}" savecurrent=false}
C {lab_pin.sym} 80 -260 0 0 {name=p12 sig_type=std_logic lab=vddh}
C {vsource.sym} 280 -210 0 0 {name=VIN value="PULSE(0 \{VDDL\} 10n \{TR\} \{TR\} 20n 50n)" savecurrent=false}
C {lab_pin.sym} 280 -260 0 0 {name=p14 sig_type=std_logic lab=in}
C {capa.sym} 620 -210 0 0 {name=CH m=1 value=\{CHIGH\}}
C {lab_pin.sym} 620 -260 0 0 {name=p16 sig_type=std_logic lab=h}
C {capa.sym} 780 -210 0 0 {name=CL m=1 value=\{CLOAD\}}
C {lab_pin.sym} 780 -260 0 0 {name=p18 sig_type=std_logic lab=out}
C {code_shown.sym} 0 -70 0 0 {name=CODE only_toplevel=false format="tcleval( @value )" value=".lib $::env(PDK_ROOT)/$::env(PDK)/libs.tech/ngspice/models/cornerMOSlv.lib mos_tt
.lib $::env(PDK_ROOT)/$::env(PDK)/libs.tech/ngspice/models/cornerMOShv.lib mos_tt
.temp 27
.param VDDL=1.2 VDDH=3.3 CHIGH=50f CLOAD=20f TR=100p
.tran 20p 48n
.meas tran t_up_rise trig v(in) val='VDDL/2' rise=1 targ v(h) val='VDDH/2' rise=1
.meas tran t_up_fall trig v(in) val='VDDL/2' fall=1 targ v(h) val='VDDH/2' fall=1
.meas tran t_rf trig v(in) val='VDDL/2' rise=1 targ v(out) val='VDDL/2' fall=1
.meas tran t_fr trig v(in) val='VDDL/2' fall=1 targ v(out) val='VDDL/2' rise=1
.meas tran vh_hi avg v(h) from=26n to=29n
.meas tran vout_lo avg v(out) from=26n to=29n
.meas tran vout_hi avg v(out) from=6n to=9n
.meas tran ih_lo avg i(VH) from=6n to=9n
.meas tran ih_hi avg i(VH) from=26n to=29n
.control
pre_osdi $::env(PDK_ROOT)/$::env(PDK)/libs.tech/ngspice/osdi/psp103_nqs.osdi
run
.endc"}
