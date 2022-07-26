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
    def __init__(self, ID: int):
        self.id = ID
        self.loc = [random.uniform(37.4, 37.9), random.uniform(127.0, 127.9)]
        self.rchg_amount = 15
        self.rchg_type = [0, 0, 1]
        self.time_wdw = [random.randint(5, 15), random.randint(5, 15)]  # 시작가능시간, 최대 완료 시간(수정됨) 랜덤으로 ㅇㅇ
        # ========= 속도 인스턴스 추가
        self.speed = random.uniform(40, 60)

    def initialize(self):  # 초기화 하는 것!
        self.done = False  # 초기 실행은 False
        self.priority = -1
        self.start_time = -1  # 충전시작타임 즉 중간에 낄 수 없음.


class Station:
    def __init__(self, ID: int):
        self.id = ID
        self.loc = [random.uniform(37.4, 37.9), random.uniform(127.0, 127.9)]  # Lat and Long (위도와 경도)
        self.max_capacity = 100
        self.avail_time = 0
        self.rchg_speed = [10, 5, 7]  # Different Charging Speed
        self.rchg_cost = [25, 10, 5]  # Different Charging Cost
        self.origin = []  # Original Station's Location

    def initialize(self):
        self.now_capacity = self.max_capacity
        self.priority = -1
        self.measures = {}
        self.measures['total_distance'] = 0
        self.measures['total_tardiness'] = 0
        self.served_req = []
        self.can_recharge = True

    def recharge(self, target: Request):
        if not self.doable(target): raise Exception('Infeasible Recharging!')
        target.done = True
        global DIST_FUNC
        req_distance = DIST_FUNC(self.loc, target.loc)
        self.measures['total_distance'] += req_distance
        self.avail_time += req_distance / target.speed ##t 수정
        self.avail_time = max(self.avail_time, target.time_wdw[0])
        target.start_time = self.avail_time
        self.measures['total_tardiness'] += max(0, self.avail_time - target.time_wdw[1])
        self.avail_time += 0  # Add Recharging Time

        # ============ 수정한부분
        target.loc = self.loc
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
        # self.measures['total_distance'] += req_distance
        car_req_distance = req_distance * (target.speed / (target.speed + self.move_speed))
        self.avail_time += car_req_distance / target.speed  # 거속시로 구한거  ==> 주유소가 시작할 수 있는시간.
        self.avail_time = max(self.avail_time, target.time_wdw[0])
        target.start_time = self.avail_time
        self.measures['total_tardiness'] += max(0, self.avail_time - target.time_wdw[1])
        self.avail_time += 0  # Add Recharging Time

        # ==============위치 구현한것.================================

        self.loc[0],self.loc[1] ,req_distance = get_between_distance_lat(self, target)
        self.measures['total_distance'] += req_distance

        target.loc = self.loc
        # ==========  주유 가능량 추가 한 부분
        self.now_capacity -= target.rchg_amount
        # ==============================================
        self.avail_time += self.rchg_speed[2]

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

    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))  # Returns in meters


def get_between_distance_lat(st: MovableStation, target: Request):
    dist = get_distance_lat(st.loc, target.loc)
    move_dist = dist * st.move_speed / (st.move_speed + target.speed)  # 실제 이동거리
    map_dist = ((target.loc[0] - st.loc[0]) ** 2 + (target.loc[1] - st.loc[1]) ** 2) ** (1 / 2)  # 좌표상 이동거리

    lat1, lon1 = target.loc[0] - st.loc[0], target.loc[1] - st.loc[1]

    dlambda = math.atan2(lon1, lat1)

    x = st.loc[0] + (move_dist * math.cos(dlambda)) * (map_dist / dist)
    y = st.loc[1] + (move_dist * math.sin(dlambda)) * (map_dist / dist)
    req_dist = dist - move_dist
    return x, y, req_dist  # 좌표 반환을 위한것 즉 위도와 경도 반환
