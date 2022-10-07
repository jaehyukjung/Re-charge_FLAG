import copy
from distance import *


class Prob_Instance:
    def __init__(self):
        self.objective = 'Total_Waiting_Time'
        self.req_list = []
        self.stn_list = []

    def __repr__(self):
        return str(
            'Objective - ' + self.objective + ', Station - ' + str(self.stn_list.__len__()) + ', Request - ' + str(
                self.req_list.__len__()) + '\n')

    def deepcopy(self):
        return copy.deepcopy(self)


class Request:
    def __init__(self, ID: int, Loc, Rchg_amount, department_time):
        self.id = ID
        self.loc = Loc
        self.rchg_amount = Rchg_amount
        self.time_wdw = [department_time, department_time]
        self.speed = 60
        self.dist_list = []
        self.tardiness = 0

    def initialize(self):
        self.done = False
        self.priority = -1
        self.start_time = self.time_wdw[0]

class Station:
    def __init__(self, ID: int, Loc):
        self.id = ID
        self.loc = Loc
        self.max_capacity = 100000
        self.avail_time = 0
        self.rchg_speed = 50 # Different Charging Speed
        self.origin = []  # Original Station's Location

    def initialize(self):
        self.now_capacity = self.max_capacity
        self.priority = -1
        self.served_req = []
        self.can_recharge = True
        self.measures = {}
        self.measures['total_distance'] = 0
        self.measures['total_wait'] = 0
        self.measures['total_time'] = 0

    def recharge(self, target: Request):
        with open('dist.p', 'rb') as file:
            distance_dic = pickle.load(file)

        if not self.doable(target):
            raise Exception('Infeasible Recharging!')
        target.done = True
        req_distance = distance_dic[dic_key(target.loc, self.loc)]
        self.measures['total_distance'] += req_distance

        self.avail_time = target.start_time + req_distance / 60  # 도착 시간
        self.measures['total_wait'] += max(self.avail_time , self.measures['total_time']) - target.start_time
        recharge_time = target.rchg_amount / self.rchg_speed  # 주유하는 시간
        self.avail_time = max(self.avail_time, self.measures['total_time'])
        target.tardiness = max(0,self.measures['total_time']-target.time_wdw[1])
        self.measures['total_time'] = self.avail_time + recharge_time
        target.loc = self.loc
        self.now_capacity -= target.rchg_amount
        self.served_req.append(target.id)

    def doable(self, target: Request) -> bool:
        if target.done:
            return False
        elif target.rchg_amount > self.now_capacity:
            return False
        else:
            return True

    def __repr__(self):
        return str('Station # ' + str(self.id))


class MovableStation(Station):
    def __init__(self, ID, Loc, moveSpeed=40):
        Station.__init__(self, ID, Loc)
        self.move_speed = moveSpeed
        self.start_loc = Loc

    def initialize(self):
        Station.initialize(self)

    def recharge(self, target: Request):
        with open('dist.p', 'rb') as file:
            distance_dic = pickle.load(file)

        if not self.doable(target): raise Exception('Infeasible Recharging!')
        target.done = True
        global DIST_FUNC
        req_distance = distance_dic[dic_key(self.loc, target.loc)]
        self.measures['total_distance'] += req_distance
        self.avail_time = max(target.start_time,self.measures['total_time']) + req_distance/self.move_speed # 도착시간
        recharge_time = target.rchg_amount / self.rchg_speed  # 주유하는 시간
        self.measures['total_wait'] += max(self.avail_time, (self.measures['total_time'])) - target.start_time + recharge_time
        self.measures['total_time'] = (self.avail_time + recharge_time)  # Movable의 경우 끝난 시간 + 다음 req의 이동시간 +주유시간
        self.loc = target.loc
        self.now_capacity -= target.rchg_amount
        self.served_req.append(target.id)


    def doable(self, target: Request) -> bool:
        if target.done:
            return False
        elif target.rchg_amount > self.now_capacity:
            return False
        else:
            return True

    def __repr__(self):
        return str('Movable Station # ' + str(self.id))




