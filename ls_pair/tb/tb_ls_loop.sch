v {xschem version=3.4.4 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {tb_ls_loop: 1.2 V -> ls_up -> 3.3 V node h -> ls_dn -> 1.2 V (net inversion)} -300 -480 0 0 0.5 0.5 {}
C {ls_up_1v2_3v3.sym} 420 -300 0 0 {name=x1}
C {gnd.sym} 420 -230 0 0 {name=g1 lab=GND}
N 360 -370 360 -390 {}
C {lab_pin.sym} 360 -390 0 0 {name=p2 sig_type=std_logic lab=vddl}
N 480 -370 480 -390 {}
C {lab_pin.sym} 480 -390 0 0 {name=p3 sig_type=std_logic lab=vddh}
N 570 -300 600 -300 {}
C {lab_pin.sym} 600 -300 2 0 {name=p4 sig_type=std_logic lab=h}
N 270 -300 250 -300 {}
C {lab_pin.sym} 250 -300 0 0 {name=p5 sig_type=std_logic lab=in}
C {ls_dn_3v3_1v2.sym} 900 -300 0 0 {name=x2}
C {gnd.sym} 900 -230 0 0 {name=g6 lab=GND}
N 900 -370 900 -390 {}
C {lab_pin.sym} 900 -390 0 0 {name=p7 sig_type=std_logic lab=vddl}
N 1050 -300 1080 -300 {}
C {lab_pin.sym} 1080 -300 2 0 {name=p8 sig_type=std_logic lab=out}
N 750 -300 730 -300 {}
C {lab_pin.sym} 730 -300 0 0 {name=p9 sig_type=std_logic lab=h}
C {vsource.sym} -200 -300 0 0 {name=VL value="dc \{VDDL\}" savecurrent=false}
N -200 -330 -200 -350 {}
C {lab_pin.sym} -200 -350 0 0 {name=p10 sig_type=std_logic lab=vddl}
C {gnd.sym} -200 -270 0 0 {name=g11 lab=GND}
C {vsource.sym} -100 -300 0 0 {name=VH value="dc \{VDDH\}" savecurrent=false}
N -100 -330 -100 -350 {}
C {lab_pin.sym} -100 -350 0 0 {name=p12 sig_type=std_logic lab=vddh}
C {gnd.sym} -100 -270 0 0 {name=g13 lab=GND}
C {vsource.sym} 0 -300 0 0 {name=VIN value="PULSE(0 \{VDDL\} 10n \{TR\} \{TR\} 20n 50n)" savecurrent=false}
N 0 -330 0 -350 {}
C {lab_pin.sym} 0 -350 0 0 {name=p14 sig_type=std_logic lab=in}
C {gnd.sym} 0 -270 0 0 {name=g15 lab=GND}
C {capa.sym} 600 -300 0 0 {name=CH m=1 value=\{CHIGH\}}
N 600 -330 600 -350 {}
C {lab_pin.sym} 600 -350 0 0 {name=p16 sig_type=std_logic lab=h}
C {gnd.sym} 600 -270 0 0 {name=g17 lab=GND}
C {capa.sym} 1220 -300 0 0 {name=CL m=1 value=\{CLOAD\}}
N 1220 -330 1220 -350 {}
C {lab_pin.sym} 1220 -350 0 0 {name=p18 sig_type=std_logic lab=out}
C {gnd.sym} 1220 -270 0 0 {name=g19 lab=GND}
C {code_shown.sym} -300 -120 0 0 {name=CODE only_toplevel=false format="tcleval( @value )" value=".lib $::env(PDK_ROOT)/$::env(PDK)/libs.tech/ngspice/models/cornerMOSlv.lib mos_tt
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
