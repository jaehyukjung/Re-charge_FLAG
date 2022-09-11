import copy
import requests
import json
import pickle

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
        self.start_time = department_time
        self.rchg_amount = Rchg_amount
        self.time_wdw = [0, 10000000]
        self.speed = 60

    def initialize(self):
        self.done = False
        self.priority = -1
        self.start_time = -1


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
        self.measures = {}
        self.measures['total_distance'] = 0
        self.measures['total_wait'] = 0
        self.served_req = []
        self.can_recharge = True
        self.measures['total_time'] = 0  # 추가

    def recharge(self, target: Request):
        with open('dist.p', 'rb') as file:
            distance_dic = pickle.load(file)

        if not self.doable(target):
            raise Exception('Infeasible Recharging!')
        target.done = True
        req_distance = distance_dic[dic_key(target.loc, self.loc)]
        self.measures['total_distance'] += req_distance

        self.avail_time = target.start_time + req_distance / 60  # 도착 시간
        self.measures['total_wait'] += abs(min(0,self.avail_time - self.measures['total_time']))
        recharge_time = target.rchg_amount / self.rchg_speed  # 주유하는 시간
        self.avail_time = max(self.avail_time, self.measures['total_time'])
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
        self.avail_time = target.start_time # 도착시간
        self.measures['total_wait'] += abs(min(0, self.avail_time - (self.measures['total_time'])))
        recharge_speed = max([x * y for x, y in zip(self.rchg_speed, target.rchg_type)])  # 주유 속도
        recharge_time = target.rchg_amount / recharge_speed  # 주유 시간
        self.measures['total_time'] += (self.avail_time + recharge_time)  # Movable의 경우 끝난 시간 + 다음 req의 이동시간 +주유시간
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


def get_distance_lat(coord1, coord2):
    if coord2[0] == coord1[0] and coord2[1] == coord1[1]:
        dist = 0

    else:
        lat1, lon1 = coord1
        lat2, lon2 = coord2
        r = requests.get(
            f"http://router.project-osrm.org/route/v1/car/{lon1},{lat1};{lon2},{lat2}?overview=full""")
        routes = json.loads(r.content)
        route_1 = routes.get("routes")[0]
        dist = route_1["distance"]

    return dist / 1000  # Returns in kilometers


def dic_key(coord1, coord2):
    return str(coord1[0]) + str(coord1[1]) + 'to' + str(coord2[0]) + str(coord2[1])


