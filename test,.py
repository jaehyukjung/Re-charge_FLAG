import copy
import math
import random
global DIST_FUNC


class Prob_Instance:
    def __init__(self):
        self.objective = 'Total_Distance'
        self.req_list = [] # 고객 요청 list
        self.stn_list = [] # station list
        global DIST_FUNC
        DIST_FUNC = get_distance_lat

    def __repr__(self):
        return str('Objective - ' + self.objective + ', Station - ' + str(self.stn_list.__len__()) + ', Request - ' + str(self.req_list.__len__()))

    def deepcopy(self):
        return copy.deepcopy(self)


class Request: # 입력 데이터: car (요청)
    def __init__(self, ID: int, Loc, Rchg_amount):
        self.id = ID
        # self.loc = [random.uniform(37.4, 37.9), random.uniform(127.0, 127.9)] # 위치
        self.loc = Loc
        # self.rchg_amount = 15 # 충전량
        self.rchg_amount = Rchg_amount
        self.rchg_type = [0, 1, 1] # 0: 불가능, 1: 가능 (초고속,고속,완속)
        self.time_wdw = [0, 10000000] # time window -> x

    def initialize(self):
        self.done = False
        self.priority = -1 # 우선순위
        self.start_time = -1 # 충전 시작 시간


class Station: # 고정식 충전소
    def __init__(self, ID: int, Loc):
        self.id = ID
        self.loc = Loc  # Lat and Long : 위치
        self.max_capacity = 80
        self.avail_time = 0 # 시작 가능 시간
        self.rchg_speed = [0, 50, 6]  # Different Charging Speed
        self.rchg_cost = [0, 7.5, 0.8225]  # Different Charging Cost
        self.origin = []  # Original Station's Location

    def initialize(self):
        self.now_capacity = self.max_capacity
        self.priority = -1
        self.measures = {}
        self.measures['total_distance'] = 0
        self.measures['total_tardiness'] = 0
        self.measures['total_time'] = 0
        self.served_req = []
        self.can_recharge = True

    def recharge(self, target: Request):
        if not self.doable(target): raise Exception('Infeasible Recharging!')
        target.done = True
        global DIST_FUNC
        req_distance = DIST_FUNC(self.loc, target.loc)
        self.measures['total_distance'] += req_distance
        self.avail_time += req_distance / 60 # 이동속도: 60
        self.avail_time = max(self.avail_time, target.time_wdw[0])
        target.start_time = self.avail_time
        self.measures['total_tardiness'] += max(0, self.avail_time - target.time_wdw[1])
        self.avail_time += 0 # Add Recharging Time
        self.loc = target.loc
        self.served_req.append(target.id)
        self.measures['total_time'] += self.finish_time(self, target)

    def finish_time(self, target: Request,req_distance):
        global DIST_FUNC
        req_distance = DIST_FUNC(self.loc, target.loc)
        go_station = req_distance / target.speed # 주유소까지 가는 시간
        speed = max(self.rchg_speed * target.rchg_type)
        recharge_time = target.rchg_amount / speed # 주유하는 시간.
        return max(self.avail_time, self.measures['total_time']) + recharge_time



    def doable(self, target: Request) -> bool: # -> return 값 힌트
        if target.done:
            return False
        elif target.rchg_amount > self.now_capacity:
            return False
        else:
            return True

    def __repr__(self):
        return str('Station # ' + str(self.id))


class MovableStation(Station): # 이동식 충전소 (고정식 충전소 상속)
    def __init__(self, ID, Loc, moveSpeed=40):
        Station.__init__(self, Loc, ID)
        self.move_speed = moveSpeed  # in km/h (Set Default Value)

    def initialize(self):
        Station.initialize(self)

    def recharge(self, target: Request):
        if not self.doable(target): raise Exception('Infeasible Recharging!')
        target.done = True
        global DIST_FUNC
        req_distance = DIST_FUNC(self.loc, target.loc)  # 수정
        self.measures['total_distance'] += req_distance
        car_req_distance = req_distance * (target.speed / (target.speed + self.move_speed))
        self.avail_time += car_req_distance / target.speed  # 거속시로 구한거  ==> 주유소가 시작할 수 있는시간.
        self.avail_time = max(self.avail_time, target.time_wdw[0])
        target.start_time = self.avail_time
        self.measures['total_tardiness'] += max(0, self.avail_time - target.time_wdw[1])
        self.avail_time += 0  # Add Recharging Time
        self.loc = target.loc
        # ==========  주유 가능량 추가 한 부분
        self.now_capacity -= target.rchg_amount
        # ==============================================
        self.avail_time += self.rchg_speed[2]
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
    R = 6372800  # Earth radius in meters
    lat1, lon1 = coord1
    lat2, lon2 = coord2

    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi / 2) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2

    return (2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))) / 1000  # Returns in kilometers