# -*- coding: utf-8 -*-
"""
Created on Wed Sep 19 10:30:56 2018

@author: elindgre
"""

import numpy as np
import matplotlib.pyplot as plt



#Vehicle parameters
gears = [3.59, 2.19, 1.41, 1, 0.83]
final_gear = 3.36
Cw = 0.31
A = 2.05
tire_r = 0.665/2 #305/30-19   0.660/2 #295/30-19 
m = 1580
shift_rpm = 6700

rpm_axis = [0, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 7200, 8200]
Tq =       [100, 300, 680, 680, 680, 620, 580, 460, 0, 0]
Tq_fac = 0.92
drivetrain_loss = 0.22 #Only for engine HP estimation

#Simulation parameters
starting_gear = 2
starting_v = 100
target_v = 200
sim_duration = 10

#Todo
#Växlingstid
#Simulerat roll-race mellan bilar








#Don't touch!
roh = 1.225
sim_duration = sim_duration * 10
gear = starting_gear - 1
tire_c = 3.14 * tire_r * 2
t_vect = range(sim_duration)
v_vect = np.zeros(sim_duration)
v_vect[0] = starting_v / 3.6
rpm_vect = np.zeros(sim_duration)
power_vect = np.zeros(len(Tq))
target_reached = 0
s_vect = np.zeros(sim_duration)
g_vect = np.zeros(sim_duration)

for p in range(len(power_vect)):
    power_vect[p] = 1.360 * Tq[p]*Tq_fac * rpm_axis[p] / 9.5488 / 1000



for tick in range(len(t_vect)):
    Fair = roh * np.power(v_vect[tick],2) * Cw * A / 2
    rpm = 60 * gears[gear] * final_gear * v_vect[tick] / tire_c
    rpm_vect[tick] = rpm
    Ftq = np.interp(rpm,rpm_axis,Tq) * Tq_fac * gears[gear] * final_gear / tire_r
    a = (Ftq - Fair) / m
    g_vect[tick] = a / 9.82
    
    if tick < sim_duration - 1:    
        v_vect[tick+1] = v_vect[tick] + a * 0.1
    
    if rpm > shift_rpm:
        gear = min(gear + 1,4)

    if (v_vect[tick] > target_v/3.6) and target_reached != 1:
        print "Time to target:"
        print float(tick)/10        
        target_reached = 1

#Calc distance covered            
for t in range(len(v_vect)):
    if t < sim_duration - 1:
        s_vect[t+1] = s_vect[t] + v_vect[t] * 0.1
    
    
    
print "Peak wheel hp"
print float(max(power_vect))

print "Peak engine hp"
print float(max(power_vect)) / (1-drivetrain_loss)

f, axes = plt.subplots(4, 1)
axes[0].plot(v_vect * 3.6)
axes[0].set_ylabel('Vehicle speed')

axes[1].plot(g_vect,'g')
axes[1].set_ylabel('Acceleration (g)')

axes[2].plot(rpm_vect,'r')
axes[2].set_ylabel('Engine speed')

axes[3].plot(s_vect,'g')
axes[3].set_ylabel('Distance covered')



