import copy
import math
import random

global DIST_FUNC


class Prob_Instance:  # 프린트 함수르 통해 출력할 때 어떻게 할 지를 설명한는 내용
    def __init__(self):
        self.objective = 'Total_Distance'
        self.req_list = []
        self.stn_list = []
        global DIST_FUNC
        DIST_FUNC = get_distance_lat

    def __repr__(self):
        return str(
            'Objective - ' + self.objective + ', Station - ' + str(self.stn_list.__len__()) + ', Request - ' + str(
                self.req_list.__len__()))

    # ----------신경
    def deepcopy(self):
        return copy.deepcopy(self)
    # ----------안씀


class Request:
    def __init__(self, ID: int, Rchg_amount):
        self.id = ID
        self.loc = [random.uniform(37.4, 37.9), random.uniform(127.0, 127.9)]
        self.rchg_amount = Rchg_amount
        self.rchg_type = [0, 1, 1]  # 초고속 고속 완속
        self.time_wdw = [0, 10000000] # time window -> x
        self.speed = 60

    def initialize(self):  # 초기화 하는 것!
        self.done = False  # 초기 실행은 False
        self.priority = -1
        self.start_time = -1  # 충전시작타임 즉 중간에 낄 수 없음.


class Station:
    def __init__(self, ID: int):
        self.id = ID
        self.loc = [random.uniform(37.4, 37.9), random.uniform(127.0, 127.9)]
        self.max_capacity = 80
        self.avail_time = 0
        self.rchg_speed = [0, 50, 6]  # Different Charging Speed
        self.rchg_cost = [0, 7.5, 0.8225]  # Different Charging Cost
        self.origin = []  # Original Station's Location

    def initialize(self):
        self.now_capacity = self.max_capacity
        self.priority = -1
        self.measures = {}
        self.measures['total_distance'] = 0
        self.measures['total_time'] = 0
        self.measures['total_tardiness'] = 0
        self.served_req = []
        self.can_recharge = True

    def recharge(self, target: Request):
        if not self.doable(target): raise Exception('Infeasible Recharging!')
        target.done = True
        global DIST_FUNC
        req_distance = DIST_FUNC(self.loc, target.loc)
        self.measures['total_distance'] += req_distance
        self.avail_time += req_distance / target.speed  # 이동속도 : 60 고정
        # =======================================================
        recharge_speed = max([x*y for x,y in zip(self.rchg_speed,target.rchg_type)]) # 주유 속도
        recharge_time = target.rchg_amount / recharge_speed  # 주유하는 시간
        self.avail_time = max(self.avail_time, self.measures['total_time'])
        # target.start_time = self.avail_time
        # self.measures['total_tardiness'] += max(0, self.avail_time - target.time_wdw[1])

        self.measures['total_time'] = self.avail_time + recharge_time
        # ==========================================================
        self.avail_time += 0  # Add Recharging Time
        target.loc = self.loc  # 수정 : 일반 Station (car -> Station)

        # ==========추가 한 부분
        self.now_capacity -= target.rchg_amount
        self.avail_time += self.rchg_speed[2]
        # ========================
        self.served_req.append(target.id)

    def doable(self, target: Request) -> bool:  ## hinting 을 주는 방식
        if target.done:
            return False
        elif target.rchg_amount > self.now_capacity:
            return False
        else:
            return True

    def __repr__(self):
        return str('Station # ' + str(self.id))


# ----------------우리가 짜야하는 부분..--------------------------------
class MovableStation(Station):
    def __init__(self, ID, moveSpeed=40):
        Station.__init__(self, ID)
        self.move_speed = moveSpeed  # in km/h (Set Default Value)

    def initialize(self):
        Station.initialize(self)


    def recharge(self, target: Request):
        if not self.doable(target): raise Exception('Infeasible Recharging!')
        target.done = True
        global DIST_FUNC
        req_distance = DIST_FUNC(self.loc, target.loc)  # 수정
        self.measures['total_distance'] += req_distance
        self.avail_time += req_distance / target.speed  # 도착시간
        # =======================================================
        recharge_speed = max([x*y for x,y in zip(self.rchg_speed,target.rchg_type)]) # 주유 속도
        recharge_time = target.rchg_amount / recharge_speed  # 주유하는 시간
        self.avail_time = max(self.avail_time, self.measures['total_time'])
        # target.start_time = self.avail_time
        # self.measures['total_tardiness'] += max(0, self.avail_time - target.time_wdw[1])
        self.measures['total_time'] = self.avail_time + recharge_time
        # ==========================================================
        self.avail_time += 0  # Add Recharging Time
        self.loc = target.loc


        # ==========  주유 가능량 추가 한 부분
        self.now_capacity -= target.rchg_amount
        # ==============================================


        self.served_req.append(target.id)
        print(1)

    def doable(self, target: Request) -> bool:
        if target.done:
            return False
        elif target.rchg_amount > self.now_capacity:
            return False
        else:
            return True

    def __repr__(self):
        return str('Movable Station # ' + str(self.id))


# ----------------우리가 짜야하는 부분..--------------------------------

def get_distance_lat(coord1, coord2):
    R = 6372800  # Earth radius in meters
    lat1, lon1 = coord1
    lat2, lon2 = coord2

    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi / 2) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2

    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a)) /1000 # Returns in meters



