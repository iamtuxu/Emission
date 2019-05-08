import glbV
import math
# Vehicle Class

class Vehicle:
    def __init__(self, x, v, lane, id):
        self.x = 0 # km
        self.v = 0 # km/h
        self.a = 0 # km/h^2
        self.beta = glbV.beta #h^-1
        self.lane = lane
        self.leader = None
        self.id = id
        self.A = 0.156461
        self.B = 0.0200193
        self.C = 0.000492646
        self.M = 1.4788
        self.co2 = 0
        self.pm = 0
        self.nox = 0
        self.co = 0
        self.thc = 0


    def updateA(self):
        self.a = self.beta * (self.lane.u - self.v) - \
                 glbV.alpha * glbV.g * max(0, self.lane.grade(self.x)) * (3600 ** 2 / 1000)


    def updateA_IDM(self):
        if self.leader == None:
            self.a = self.beta * (self.lane.u - self.v) - \
                     glbV.alpha * glbV.g * max(0, self.lane.grade(self.x)) * (3600 ** 2 / 1000)
        else:
            sj = 1000 * (self.leader.x - self.x) - glbV.l_idm
            sstar = glbV.s0_idm + glbV.T_idm * (self.v / 3.6) + (self.v / 3.6 * (self.v - self.leader.v) / 3.6) \
                    / (2 * math.sqrt(glbV.a_idm * glbV.b_idm))
            self.a = glbV.a_idm * (1 - (self.v / self.lane.u) ** glbV.delta_idm - (sstar / sj) ** 2)
            - glbV.alpha * glbV.g * max(0, self.lane.grade(self.x))
            # unit convention
            self.a = self.a * 3600 * 3600 / 1000


    def updateA_Gipps(self):
        if self.leader == None:
            self.a = self.beta * (self.lane.u - self.v) - \
                     glbV.alpha * glbV.g * max(0, self.lane.grade(self.x)) * (3600 ** 2 / 1000)
        else:
            v_free = 2.5 * glbV.a_gipps * glbV.T_gipps * (1 - self.v / self.lane.u) \
                     * ((self.v / self.lane.u + 0.025) ** 0.5) + self.v / 3.6
            v_cong = math.sqrt((glbV.b_gipps * (glbV.theta_gipps + glbV.T_gipps / 2)) ** 2
                               + glbV.b_gipps * ((self.leader.v / 3.6) ** 2 / 3.5
                                                 + 2 * (self.leader.x - self.x - self.lane.jamspacing) * 1000
                                                 - glbV.T_gipps * self.v / 3.6)) \
                     - glbV.b_gipps * (glbV.theta_gipps + glbV.T_gipps / 2)
            self.a = (min(v_free, v_cong) * 3.6 - self.v) / (glbV.dt / 3600)


    def updateV(self):
        self.v = self.v + self.a * (glbV.dt / 3600)

    def updateX(self):
        if self.leader == None:
            self.x = self.x + self.v * (glbV.dt / 3600)
        else:
            self.x = min(self.x + self.v * (glbV.dt / 3600), self.leader.x - self.lane.jamspacing)
        # print('veh id', self.id, 'position', self.x)


    def calVSP(self):
        return (self.v / 3.6) * (self.a * 1000 / (3600 ** 2) + glbV.g * self.lane.grade(self.x)
                                 + (self.A + self.B * self.v / 3.6 + self.C * ((self.v / 3.6) ** 2)) / self.M)

    def updateE(self):
        self.co2 = self.co2 + glbV.dt * (0.2532 * self.calVSP() + 1.0522)
        self.pm = self.pm + glbV.dt * math.exp(0.0425 * self.calVSP() - 5.0915)
        self.nox = self.nox + glbV.dt * math.exp(0.0664 * self.calVSP() - 4.2)
        self.co = self.co + glbV.dt * math.exp(0.051 * self.calVSP() - 2.664)
        self.thc = self.thc + glbV.dt * math.exp(0.0596 * self.calVSP() - 4.8019)






    
        