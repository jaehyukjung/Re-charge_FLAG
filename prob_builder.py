import copy
import requests
import json

global DIST_FUNC


class Prob_Instance:  # 프린트 함수르 통해 출력할 때 어떻게 할 지를 설명한는 내용
    def __init__(self):
        self.objective = 'Total_Time'
        self.req_list = []
        self.stn_list = []
        global DIST_FUNC
        DIST_FUNC = get_distance_lat

    def __repr__(self):
        return str('Objective - ' + self.objective + ', Station - ' + str(self.stn_list.__len__()) + ', Request - ' + str(self.req_list.__len__()))

    def deepcopy(self):
        return copy.deepcopy(self)


class Request:
    def __init__(self, ID: int, Loc, Rchg_amount):
        self.id = ID
        self.loc = Loc # [random.uniform(37.4, 37.9), random.uniform(127.0, 127.9)]  # 입력 변수로 변경
        self.rchg_amount = Rchg_amount
        self.rchg_type = [0, 1, 1]  # 초고속 고속 완속 - 현재는 초고속만 고려
        self.time_wdw = [0, 10000000]  # time window -> 현재는 고려 X
        self.speed = 60

    def initialize(self):
        self.done = False
        self.priority = -1
        self.start_time = -1  # 충전 시작 시간


class Station:
    def __init__(self, ID: int, Loc):
        self.id = ID
        self.loc = Loc  #[random.uniform(37.4, 37.9), random.uniform(127.0, 127.9)]
        self.max_capacity = 80
        self.avail_time = 0
        self.rchg_speed = [100, 50, 6]  # Different Charging Speed
        self.rchg_cost = [0, 7.5, 0.8225]  # Different Charging Cost
        self.origin = []  # Original Station's Location


    def initialize(self):
        self.now_capacity = self.max_capacity
        self.priority = -1
        self.measures = {}
        self.measures['total_distance'] = 0
        self.measures['total_tardiness'] = 0
        self.served_req = []
        self.can_recharge = True
        self.measures['total_time'] = 0 # 추가

    def recharge(self, target: Request):
        if not self.doable(target): raise Exception('Infeasible Recharging!')
        target.done = True
        global DIST_FUNC
        req_distance = DIST_FUNC(target.loc, self.loc)
        self.measures['total_distance'] += req_distance
        self.avail_time = req_distance / 60  # 이동속도 : 60 고정  # 도착시간
        recharge_speed = max([x*y for x,y in zip(self.rchg_speed,target.rchg_type)]) # 주유 속도
        recharge_time = target.rchg_amount / recharge_speed  # 주유하는 시간
        self.avail_time = max(self.avail_time, self.measures['total_time'])
        target.start_time = self.avail_time
        # self.measures['total_tardiness'] += max(0, self.avail_time - target.time_wdw[1])
        self.measures['total_time'] = self.avail_time + recharge_time  # 종료된 시간
        self.avail_time += 0  # Add Recharging Time
        target.loc = self.loc  # 수정 : 일반 Station (car -> Station)
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
        self.move_speed = moveSpeed  # in km/h (Set Default Value)

    def initialize(self):
        Station.initialize(self)


    def recharge(self, target: Request):
        if not self.doable(target): raise Exception('Infeasible Recharging!')
        target.done = True
        global DIST_FUNC
        req_distance = DIST_FUNC(self.loc, target.loc)  # 수정
        self.measures['total_distance'] += req_distance
        self.avail_time = req_distance / target.speed  # 도착시간
        recharge_speed = max([x*y for x,y in zip(self.rchg_speed,target.rchg_type)]) # 주유 속도
        recharge_time = target.rchg_amount / recharge_speed  # 주유하는 시간
        # target.start_time = self.avail_time
        # self.measures['total_tardiness'] += max(0, self.avail_time - target.time_wdw[1])
        self.measures['total_time'] += (self.avail_time + recharge_time)
        self.avail_time += 0  # Add Recharging Time
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
    lat1, lon1 = coord1
    lat2, lon2 = coord2

    r = requests.get(
        f"http://router.project-osrm.org/route/v1/car/{lon1},{lat1};{lon2},{lat2}?overview=full""")
    routes = json.loads(r.content)
    route_1 = routes.get("routes")[0]
    dist = route_1["distance"]

    return dist/1000  # Returns in kilometers
