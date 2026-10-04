v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {tb_ls_up: ls_up_1v2_3v3, 1.2 V -> 3.3 V.  PVT sweep: scripts/run_pvt.py tb_ls_up} 0 -470 0 0 0.5 0.5 {}
N 530 -390 530 -360 {lab=vddl}
N 580 -330 620 -330 {lab=out}
N 80 -150 80 -130 {lab=GND}
N 280 -170 280 -150 {lab=GND}
N 180 -150 280 -150 {lab=GND}
N 180 -170 180 -150 {lab=GND}
N 80 -170 80 -150 {lab=GND}
N 620 -170 620 -150 {lab=GND}
N 620 -330 620 -230 {lab=out}
N 540 -300 540 -150 {lab=GND}
N 280 -150 540 -150 {lab=GND}
N 80 -150 180 -150 {lab=GND}
N 550 -410 550 -360 {lab=vddh}
N 180 -390 530 -390 {lab=vddl}
N 180 -390 180 -230 {lab=vddl}
N 80 -410 550 -410 {lab=vddh}
N 80 -410 80 -230 {lab=vddh}
N 280 -330 500 -330 {lab=in}
N 280 -330 280 -230 {lab=in}
N 540 -150 620 -150 {lab=GND}
C {code_shown.sym} 0 -70 0 0 {name=CODE only_toplevel=false format="tcleval( @value )" value=".lib $::env(PDK_ROOT)/$::env(PDK)/libs.tech/ngspice/models/cornerMOSlv.lib mos_tt
.lib $::env(PDK_ROOT)/$::env(PDK)/libs.tech/ngspice/models/cornerMOShv.lib mos_tt
.temp 27
.param VDDL=1.2 VDDH=3.3 CLOAD=50f TR=100p
.tran 20p 48n
.meas tran tplh trig v(in) val='VDDL/2' rise=1 targ v(out) val='VDDH/2' rise=1
.meas tran tphl trig v(in) val='VDDL/2' fall=1 targ v(out) val='VDDH/2' fall=1
.meas tran voh avg v(out) from=26n to=29n
.meas tran vol avg v(out) from=6n to=9n
.meas tran ih_lo avg i(VH) from=6n to=9n
.meas tran ih_hi avg i(VH) from=26n to=29n
.meas tran il_lo avg i(VL) from=6n to=9n
.meas tran il_hi avg i(VL) from=26n to=29n
.control
pre_osdi $::env(PDK_ROOT)/$::env(PDK)/libs.tech/ngspice/osdi/psp103_nqs.osdi
run
.endc"}
C {ls_up_1v2_3v3.sym} 540 -330 0 0 {name=x1}
C {lab_pin.sym} 550 -410 2 0 {name=p3 sig_type=std_logic lab=vddh}
C {lab_pin.sym} 280 -330 0 0 {name=p5 sig_type=std_logic lab=in}
C {lab_pin.sym} 530 -390 0 1 {name=p7 sig_type=std_logic lab=vddl}
C {lab_pin.sym} 620 -330 2 0 {name=p8 sig_type=std_logic lab=out}
C {vsource.sym} 180 -200 0 0 {name=VL value="dc \{VDDL\}" savecurrent=false}
C {lab_pin.sym} 180 -250 0 0 {name=p10 sig_type=std_logic lab=vddl}
C {gnd.sym} 80 -130 0 0 {name=g11 lab=GND}
C {vsource.sym} 80 -200 0 0 {name=VH value="dc \{VDDH\}" savecurrent=false}
C {lab_pin.sym} 80 -250 0 0 {name=p12 sig_type=std_logic lab=vddh}
C {vsource.sym} 280 -200 0 0 {name=VIN value="PULSE(0 \{VDDL\} 10n \{TR\} \{TR\} 20n 50n)" savecurrent=false}
C {lab_pin.sym} 280 -250 0 0 {name=p14 sig_type=std_logic lab=in}
C {capa.sym} 620 -200 0 0 {name=CL m=1 value=\{CLOAD\}}
C {lab_pin.sym} 620 -250 0 0 {name=p18 sig_type=std_logic lab=out}
