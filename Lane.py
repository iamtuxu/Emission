from random import random
import math
from Vehicle import Vehicle
## Lane class

class Lane:
    def __init__(self, length):
        self.u = 60.0 # km/hr
        self.jamden = 150.0 #veh/km
        self.jamspacing = 1.0 / self.jamden #km
        self.cars = []
        self.pos = 0
        self.q = 3000.0
        self.length = length
        self.ttvehs = 0     # total number of vehs on the lane, also includes vehicles exited
        self.co2 = 0
        self.pm = 0
        self.nox = 0
        self.co = 0
        self.thc = 0

    def grade(self, x):
        return (0.04 + 0.06 * math.cos(20 * x)) / 100


    def veh_arrival(self, q, dt=1.2):
        # generate a vehicle with a probability
        prob = q / (3600.0 / dt)  # q is the flow rate
        temp = random()
        temp1 = (prob > temp)
        # temp1: 1 generate 0 no generate
        # temp2: 0 means the beginning of the lane is blocked
        # temp3: 0 means there is no car on the lane
        if len(self.cars) > 0:
            temp2 = self.cars[-1].x > self.jamspacing   # if there is space, generate new vehicle.
            temp3 = 1
        else:
            temp2 = 1  # if there is no vehicle on the lane, generate new vehicle
            temp3 = 0
        if (temp1 and temp2):
            tempVeh = Vehicle(0, 0, self, self.ttvehs)
            if temp3:
                tempVeh.leader = self.cars[-1]
            else:
                tempVeh.leader = None
            self.ttvehs = self.ttvehs + 1
            self.cars.append(tempVeh)


    def veh_transfer(self):
        if len(self.cars) > 0:
            tempVeh = self.cars[0]
            if tempVeh.x > self.length:
                self.co2 = self.co2 + tempVeh.co2
                self.pm = self.pm + tempVeh.pm
                self.nox = self.nox + tempVeh.nox
                self.co = self.co + tempVeh.co
                self.thc = self.thc + tempVeh.thc
                self.cars.pop(0)
                if(len(self.cars) > 0):
                    self.cars[0].leader = None




