import os.path
import random
from prob_builder import *
from typing import List
import pickle
PENALTY = 1000000

def random_rule_solver(instance: Prob_Instance) -> dict:
    solution = {}
    solution['Problem'] = instance.deepcopy()

    req_list = instance.req_list
    req: Request
    for req in req_list:
        req.initialize()

    stn_list = instance.stn_list
    stn: Station
    for stn in stn_list:
        stn.initialize()


    if not os.path.exists('dist.p'):
        distance_dic = {}

        for req in req_list:
            for st in stn_list:
                distance_dic[dic_key(req.loc, st.loc)] = get_distance_lat(req.loc, st.loc)
                distance_dic[dic_key(st.loc, req.loc)] = get_distance_lat(st.loc, req.loc)

        for req1 in req_list:
            for req2 in req_list:
                if req1.id != req2.id:
                    distance_dic[dic_key(req1.loc, req2.loc)] = get_distance_lat(req1.loc, req2.loc)
                    distance_dic[dic_key(req2.loc, req1.loc)] = get_distance_lat(req2.loc, req1.loc)


        with open('dist.p', 'wb') as file:
            pickle.dump(distance_dic, file)

    else:
        with open('dist.p', 'rb') as file:
            distance_dic = pickle.load(file)

        for req in req_list:
            for st in stn_list:
                if dic_key(req.loc, st.loc) not in distance_dic:
                    distance_dic[dic_key(req.loc, st.loc)] = get_distance_lat(req.loc, st.loc)
                    distance_dic[dic_key(st.loc, req.loc)] = get_distance_lat(st.loc, req.loc)

        for req1 in req_list:
            for req2 in req_list:
                if req1.id != req2.id and (dic_key(req1.loc, req2.loc) not in distance_dic):
                    distance_dic[dic_key(req1.loc, req2.loc)] = get_distance_lat(req1.loc, req2.loc)
                    distance_dic[dic_key(req2.loc, req1.loc)] = get_distance_lat(req2.loc, req1.loc)

        with open('dist.p', 'wb') as file:
            pickle.dump(distance_dic, file)


    def random_priority(target_list: List[Request], station_list: List[Station]):
        for req in target_list:
            req.priority = random.randint(1,1000000)
        for stn in station_list:
            stn.priority = random.randint(1,1000000)

        return min(target_list, key = lambda x: x.priority), min(station_list, key = lambda x: x.priority)


    while any(req.done is False for req in req_list):
        not_completed_reqs = list(filter(lambda x: (x.done is False), req_list))
        servable_stn = list(filter(lambda x: x.can_recharge is True, stn_list))
        pri_req, pri_stn = random_priority(not_completed_reqs,servable_stn) # 랜덤
        try:
             pri_stn.recharge(pri_req)
        except Exception:
            raise Exception('Invalid Logic')
            break

    solution['Snapshop_Requests'] = req_list
    solution['Snapshop_Stations'] = stn_list

    maximum = 0
    for stn in stn_list:
        if stn.measures['total_time'] > maximum:
            maximum = stn.measures['total_time']

    solution['Objective'] = maximum

    return solution

def subin_rule_solver(instance: Prob_Instance) -> dict:
    print('Solver Start')
    solution = {}
    solution['Problem'] = instance.deepcopy()

    req_list = instance.req_list
    req: Request
    for req in req_list:
        req.initialize()

    stn_list = instance.stn_list
    stn: Station
    for stn in stn_list:
        stn.initialize()

    if not os.path.exists('dist.p'):
        distance_dic = {}

        for req in req_list:
            for st in stn_list:
                distance_dic[dic_key(req.loc, st.loc)] = get_distance_lat(req.loc, st.loc)
                distance_dic[dic_key(st.loc, req.loc)] = get_distance_lat(st.loc, req.loc)

        for req1 in req_list:
            for req2 in req_list:
                if req1.id != req2.id:
                    distance_dic[dic_key(req1.loc, req2.loc)] = get_distance_lat(req1.loc, req2.loc)
                    distance_dic[dic_key(req2.loc, req1.loc)] = get_distance_lat(req2.loc, req1.loc)


        with open('dist.p', 'wb') as file:
            pickle.dump(distance_dic, file)

    else:
        with open('dist.p', 'rb') as file:
            distance_dic = pickle.load(file)

        for req in req_list:
            for st in stn_list:
                if dic_key(req.loc, st.loc) not in distance_dic:
                    distance_dic[dic_key(req.loc, st.loc)] = get_distance_lat(req.loc, st.loc)
                    distance_dic[dic_key(st.loc, req.loc)] = get_distance_lat(st.loc, req.loc)

        for req1 in req_list:
            for req2 in req_list:
                if req1.id != req2.id and (dic_key(req1.loc, req2.loc) not in distance_dic):
                    distance_dic[dic_key(req1.loc, req2.loc)] = get_distance_lat(req1.loc, req2.loc)
                    distance_dic[dic_key(req2.loc, req1.loc)] = get_distance_lat(req2.loc, req1.loc)

        with open('dist.p', 'wb') as file:
            pickle.dump(distance_dic, file)


    def priority(target_list: List[Request], station_list: List[Station]):
        pri_dic = {}
        mstn_list = list(filter(lambda x: isinstance(x, MovableStation), station_list))
        stn_list = list(filter(lambda x: isinstance(x, MovableStation) is False, station_list))

        for req in target_list:
            for stn in mstn_list:
                if stn.doable(req):
                    try:
                        dist = distance_dic[dic_key(stn.loc, req.loc)]  # 위의 딕셔너리에서 값 바로 가져오기
                    except Exception:
                        dist = (get_distance_lat(stn.loc, req.loc))  # 위의 딕셔너리에서 값 바로 가져오기
                else:
                    dist = PENALTY

                dist /= req.rchg_amount
                pri_dic[dist] = [req, stn]

        for req in target_list:
            for stn in stn_list:
                if stn.doable(req):
                    try:
                        dist = distance_dic[dic_key(req.loc, stn.loc)]  # 위의 딕셔너리에서 값 바로 가져오기
                    except Exception:
                        dist = (get_distance_lat(req.loc, stn.loc))  # 위의 딕셔너리에서 값 바로 가져오기
                else:
                    dist = PENALTY

                dist /= req.rchg_amount
                pri_dic[dist] = [req, stn]

        minimum = min(pri_dic.keys())

        return pri_dic[minimum][0], pri_dic[minimum][1]

    def su_priority(target_list: List[Request], station):
        su_list = []
        for req in target_list:
            dist = distance_dic[dic_key(req.loc, station.loc)]
            if dist <= 0.5:
                su_list.append(req)
        return su_list

# ====================================================================================================================
    not_move_station = list(filter(lambda x: isinstance(stn, MovableStation) is False, stn_list))
    move_station = list(filter(lambda x: isinstance(stn, MovableStation) is True, stn_list))

    while any(req.done is False for req in req_list):
        not_completed_reqs = list(filter(lambda x: (x.done is False), req_list))

        for pri_stn in not_move_station:
            reqest_list = su_priority(not_completed_reqs,pri_stn)
            for pri_req in reqest_list:
                try:
                     pri_stn.recharge(pri_req)
                except Exception:
                    raise Exception('Invalid Logic')
                    break

        pri_req, pri_stn = priority(not_completed_reqs, move_station)
        try:
            pri_stn.recharge(pri_req)
        except Exception:
            raise Exception('Invalid Logic')
            break

    solution['Snapshop_Requests'] = req_list
    solution['Snapshop_Stations'] = stn_list

    maximum = 0
    for stn in stn_list:
        if stn.measures['total_time'] > maximum:
            maximum = stn.measures['total_time']

    solution['Objective'] = maximum

    return solution




# 재혁
def rule_solver(instance: Prob_Instance) -> dict:
    print('Solver Start')
    solution = {}
    solution['Problem'] = instance.deepcopy()

    req_list = instance.req_list
    req: Request
    for req in req_list:
        req.initialize()

    stn_list = instance.stn_list
    stn: Station
    for stn in stn_list:
        stn.initialize()

    if not os.path.exists('dist.p'):
        distance_dic = {}

        for req in req_list:
            for st in stn_list:
                distance_dic[dic_key(req.loc, st.loc)] = get_distance_lat(req.loc, st.loc)
                distance_dic[dic_key(st.loc, req.loc)] = get_distance_lat(st.loc, req.loc)

        for req1 in req_list:
            for req2 in req_list:
                if req1.id != req2.id:
                    distance_dic[dic_key(req1.loc, req2.loc)] = get_distance_lat(req1.loc, req2.loc)
                    distance_dic[dic_key(req2.loc, req1.loc)] = get_distance_lat(req2.loc, req1.loc)


        with open('dist.p', 'wb') as file:
            pickle.dump(distance_dic, file)

    else:
        with open('dist.p', 'rb') as file:
            distance_dic = pickle.load(file)

        for req in req_list:
            for st in stn_list:
                if dic_key(req.loc, st.loc) not in distance_dic:
                    distance_dic[dic_key(req.loc, st.loc)] = get_distance_lat(req.loc, st.loc)
                    distance_dic[dic_key(st.loc, req.loc)] = get_distance_lat(st.loc, req.loc)

        for req1 in req_list:
            for req2 in req_list:
                if req1.id != req2.id and (dic_key(req1.loc, req2.loc) not in distance_dic):
                    distance_dic[dic_key(req1.loc, req2.loc)] = get_distance_lat(req1.loc, req2.loc)
                    distance_dic[dic_key(req2.loc, req1.loc)] = get_distance_lat(req2.loc, req1.loc)

        with open('dist.p', 'wb') as file:
            pickle.dump(distance_dic, file)

    def priority(target_list: List[Request], station_list: List[Station]):
        pri_dic = {}
        mpri_dic = {}
        for req in target_list:
            for stn in station_list:
                if stn.doable(req):
                    if isinstance(stn, MovableStation):
                        try:
                            dist = distance_dic[dic_key(stn.loc, req.loc)]  # 위의 딕셔너리에서 값 바로 가져오기
                        except Exception:
                            dist = (get_distance_lat(stn.loc, req.loc))  # 위의 딕셔너리에서 값 바로 가져오기

                        mpri_dic[dist] = [req, stn]
                    else:
                        try:
                            dist = distance_dic[dic_key(req.loc, stn.loc)] # 위의 딕셔너리에서 값 바로 가져오기
                        except Exception:
                            dist = (get_distance_lat(req.loc, stn.loc)) # 위의 딕셔너리에서 값 바로 가져오기

                        pri_dic[dist] = [req, stn]
                else:
                    dist = PENALTY

        if min(pri_dic.keys()) >= min(mpri_dic.keys()) and pri_dic[min(pri_dic.keys())][1].measures['total_time'] >= mpri_dic[min(mpri_dic.keys())][1].measures['total_time']:
            minimum = min(mpri_dic.keys())
            return mpri_dic[minimum][0], mpri_dic[minimum][1]

        else:
            minimum = min(pri_dic.keys())
            return pri_dic[minimum][0], pri_dic[minimum][1]

    while any(req.done is False for req in req_list):
        not_completed_reqs = list(filter(lambda x: (x.done is False), req_list))
        servable_stn = list(filter(lambda x: x.can_recharge is True, stn_list))
        pri_req, pri_stn = priority(not_completed_reqs,servable_stn) # 재혁

        try:
             pri_stn.recharge(pri_req)
        except Exception:
            raise Exception('Invalid Logic')
            break

    solution['Snapshop_Requests'] = req_list
    solution['Snapshop_Stations'] = stn_list

    maximum = 0
    for stn in stn_list:
        if stn.measures['total_time'] > maximum:
            maximum = stn.measures['total_time']

    solution['Objective'] = maximum

    return solution


def minseok_rule_solver(instance: Prob_Instance) -> dict:
    print('Solver Start')
    solution = {}
    solution['Problem'] = instance.deepcopy()

    req_list = instance.req_list
    req: Request
    for req in req_list:
        req.initialize()

    stn_list = instance.stn_list
    stn: Station
    for stn in stn_list:
        stn.initialize()

    if not os.path.exists('dist.p'):
        distance_dic = {}

        for req in req_list:
            for st in stn_list:
                distance_dic[dic_key(req.loc, st.loc)] = get_distance_lat(req.loc, st.loc)
                distance_dic[dic_key(st.loc, req.loc)] = get_distance_lat(st.loc, req.loc)

        for req1 in req_list:
            for req2 in req_list:
                if req1.id != req2.id:
                    distance_dic[dic_key(req1.loc, req2.loc)] = get_distance_lat(req1.loc, req2.loc)
                    distance_dic[dic_key(req2.loc, req1.loc)] = get_distance_lat(req2.loc, req1.loc)


        with open('dist.p', 'wb') as file:
            pickle.dump(distance_dic, file)

    else:
        with open('dist.p', 'rb') as file:
            distance_dic = pickle.load(file)

        for req in req_list:
            for st in stn_list:
                if dic_key(req.loc, st.loc) not in distance_dic:
                    distance_dic[dic_key(req.loc, st.loc)] = get_distance_lat(req.loc, st.loc)
                    distance_dic[dic_key(st.loc, req.loc)] = get_distance_lat(st.loc, req.loc)

        for req1 in req_list:
            for req2 in req_list:
                if req1.id != req2.id and (dic_key(req1.loc, req2.loc) not in distance_dic):
                    distance_dic[dic_key(req1.loc, req2.loc)] = get_distance_lat(req1.loc, req2.loc)
                    distance_dic[dic_key(req2.loc, req1.loc)] = get_distance_lat(req2.loc, req1.loc)

        with open('dist.p', 'wb') as file:
            pickle.dump(distance_dic, file)

    def priority(target_list: List[Request], station_list: List[Station]):
        pri_dic = {}
        for req in target_list:
            for stn in station_list:
                if stn.doable(req):
                    if isinstance(stn, MovableStation):
                        try:
                            dist = distance_dic[dic_key(stn.loc, req.loc)]  # 위의 딕셔너리에서 값 바로 가져오기
                        except Exception:
                            dist = (get_distance_lat(stn.loc, req.loc))  # 위의 딕셔너리에서 값 바로 가져오기
                    else:
                        try:
                            dist = distance_dic[dic_key(req.loc, stn.loc)] # 위의 딕셔너리에서 값 바로 가져오기
                        except Exception:
                            dist = (get_distance_lat(req.loc, stn.loc)) # 위의 딕셔너리에서 값 바로 가져오기
                else:
                    dist = PENALTY

                pri_dic[dist] = [req, stn]

        minimum = min(pri_dic.keys())

        return pri_dic[minimum][0], pri_dic[minimum][1]

    while any(req.done is False for req in req_list):
        not_completed_reqs = list(filter(lambda x: (x.done is False), req_list))
        servable_stn = list(filter(lambda x: x.can_recharge is True, stn_list))
        maximum = max(servable_stn, key=lambda x: x.max_capacity)
        max_capa_list = list(filter(lambda x: x.max_capacity == maximum.max_capacity, servable_stn))
        pri_req, pri_stn = priority(not_completed_reqs, max_capa_list)# 재혁

        try:
             pri_stn.recharge(pri_req)
        except Exception:
            raise Exception('Invalid Logic')
            break

    solution['Snapshop_Requests'] = req_list
    solution['Snapshop_Stations'] = stn_list

    maximum = 0
    for stn in stn_list:
        if stn.measures['total_time'] > maximum:
            maximum = stn.measures['total_time']

    solution['Objective'] = maximum

    return solution


def minseok_rule_solver2(instance: Prob_Instance) -> dict:
    print('Solver Start')
    solution = {}
    solution['Problem'] = instance.deepcopy()

    req_list = instance.req_list
    req: Request
    for req in req_list:
        req.initialize()

    stn_list = instance.stn_list
    stn: Station
    for stn in stn_list:
        stn.initialize()

    if not os.path.exists('dist.p'):
        distance_dic = {}

        for req in req_list:
            for st in stn_list:
                distance_dic[dic_key(req.loc, st.loc)] = get_distance_lat(req.loc, st.loc)
                distance_dic[dic_key(st.loc, req.loc)] = get_distance_lat(st.loc, req.loc)

        for req1 in req_list:
            for req2 in req_list:
                if req1.id != req2.id:
                    distance_dic[dic_key(req1.loc, req2.loc)] = get_distance_lat(req1.loc, req2.loc)
                    distance_dic[dic_key(req2.loc, req1.loc)] = get_distance_lat(req2.loc, req1.loc)


        with open('dist.p', 'wb') as file:
            pickle.dump(distance_dic, file)

    else:
        with open('dist.p', 'rb') as file:
            distance_dic = pickle.load(file)

        for req in req_list:
            for st in stn_list:
                if dic_key(req.loc, st.loc) not in distance_dic:
                    distance_dic[dic_key(req.loc, st.loc)] = get_distance_lat(req.loc, st.loc)
                    distance_dic[dic_key(st.loc, req.loc)] = get_distance_lat(st.loc, req.loc)

        for req1 in req_list:
            for req2 in req_list:
                if req1.id != req2.id and (dic_key(req1.loc, req2.loc) not in distance_dic):
                    distance_dic[dic_key(req1.loc, req2.loc)] = get_distance_lat(req1.loc, req2.loc)
                    distance_dic[dic_key(req2.loc, req1.loc)] = get_distance_lat(req2.loc, req1.loc)

        with open('dist.p', 'wb') as file:
            pickle.dump(distance_dic, file)

    def priority(target_list: List[Request], station_list: List[Station]):
        pri_dic = {}
        for req in target_list:
            for stn in station_list:
                if stn.doable(req):
                    if isinstance(stn, MovableStation):
                        try:
                            dist = distance_dic[dic_key(stn.loc, req.loc)]  # 위의 딕셔너리에서 값 바로 가져오기
                        except Exception:
                            dist = (get_distance_lat(stn.loc, req.loc))  # 위의 딕셔너리에서 값 바로 가져오기
                    else:
                        try:
                            dist = distance_dic[dic_key(req.loc, stn.loc)] # 위의 딕셔너리에서 값 바로 가져오기
                        except Exception:
                            dist = (get_distance_lat(req.loc, stn.loc)) # 위의 딕셔너리에서 값 바로 가져오기
                else:
                    dist = PENALTY

                pri_dic[dist] = [req, stn]

        minimum = min(pri_dic.keys())

        return pri_dic[minimum][0], pri_dic[minimum][1]


    # def min_priority(target_list: List[Request], station_list: List[Station]):
    #     maximum = max(station_list, key=lambda x: x.max_capacity)
    #     max_capa_list = list(filter(lambda x: x.max_capacity == maximum, station_list))
    #     return priority(target_list, max_capa_list)


    while any(req.done is False for req in req_list):
        not_completed_reqs = list(filter(lambda x: (x.done is False), req_list))
        servable_stn = list(filter(lambda x: x.can_recharge is True, stn_list))
        maximum = max(servable_stn, key=lambda x: x.max_capacity)
        max_capa_list = list(filter(lambda x: x.max_capacity == maximum.max_capacity, servable_stn))
        pri_req, pri_stn = priority(not_completed_reqs, max_capa_list)# 재혁

        try:
             pri_stn.recharge(pri_req)
        except Exception:
            raise Exception('Invalid Logic')
            break

    solution['Snapshop_Requests'] = req_list
    solution['Snapshop_Stations'] = stn_list

    maximum = 0
    for stn in stn_list:
        if stn.measures['total_time'] > maximum:
            maximum = stn.measures['total_time']

    solution['Objective'] = maximum

    return solution