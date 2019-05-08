# global variables
sim_time = 1200.0 # the simulation time
dt = 1.2 # simulation step
g = 9.81 # m/s^2
alpha = 0.5 # grade
beta = 500
pltveh = 20 # vehicles in the platoon

opt = 2 # 1 for Newell 2 for IDM 3 for Gipps

# IDM parameters
a_idm = 0.73
delta_idm = 4.0
l_idm = 5.0 #meters vehicle length
b_idm = 1.67
T_idm = 1.5
s0_idm = 2.0

# Gipps parameters
a_gipps = 1.7
T_gipps = 1.2
b_gipps = 3.0
theta_gipps = 1.0 / 3.0
b0_gipps = 3.5