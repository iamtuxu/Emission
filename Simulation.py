from Lane import Lane
import glbV    # global variables
import numpy as np
import math

# Initialize Road Network
# we have a lane segment with 1km length
ln = Lane(1)

# Run Simulation
for t in np.arange(0, glbV.sim_time, glbV.dt):
    # each time step, generate cars at the beginning of the lane
    if(ln.ttvehs < glbV.pltveh):
        ln.veh_arrival(ln.q, glbV.dt)

    # update all vehicles' speed and location on each lane


    for tempVeh in ln.cars:
        # update acceleration
        if glbV.opt == 1:
            tempVeh.updateA()
        elif glbV.opt == 2:
            tempVeh.updateA_IDM()
        elif glbV.opt == 3:
            tempVeh.updateA_Gipps()
        else:
            print("model not built yet")
        tempVeh.updateV()
        tempVeh.updateX()
        tempVeh.updateE() # update emission


    # each time step, remove vehicles reach the end of the lane
    # vehicle emission is also calculated in this function
    ln.veh_transfer()


    if(len(ln.cars) == 0 and ln.ttvehs > 0):
        break

    # print('number of vehicles', len(ln.cars), 'at time', t)
    # if len(ln.cars) > 0:
    #     print('position of first car', ln.cars[0].x)
print('alpha', glbV.alpha, 'Beta', glbV.beta)
print('total CO2', ln.co2)
print('total PM', ln.pm)
print('total NOX', ln.nox)
print('total CO', ln.co)
print('total THC', ln.thc)


