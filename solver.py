import os.path

import prob_builder
from prob_builder import *
from typing import List
import time
import pickle

PENALTY = 1000000


def rule_solver(instance: Prob_Instance) -> dict:
    print('Solver Start')
    total_algorithm_start = time.time()

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

    # ===================================================================================================
    distance_start = time.time()
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

        # for req1 in stn_list:
        #     for req2 in stn_list:
        #         if req1.id != req2.id:
        #             distance_dic[dic_key(req1.loc, req2.loc)] = get_distance_lat(req1.loc, req2.loc)
        #             distance_dic[dic_key(req2.loc, req1.loc)] = get_distance_lat(req2.loc, req1.loc)
        with open('dist.p', 'wb') as file:
            pickle.dump(distance_dic, file)
    else:
        with open('dist.p', 'rb') as file:
            distance_dic = pickle.load(file)
    distance_end = time.time()
    # ===================================================================================================
    start = time.time()

    def update_priority_req(target_list: List[Request], station_list: List[Station]):
        for req in target_list:
            req_lst = []
            for stn in station_list:
                if isinstance(stn, MovableStation):
                    try:
                        req_lst.append(distance_dic[dic_key(stn.loc, req.loc)])  # 위의 딕셔너리에서 값 바로 가져오기
                    except Exception:
                        req_lst.append(get_distance_lat(stn.loc, req.loc))  # 위의 딕셔너리에서 값 바로 가져오기
                else:
                    try:
                        req_lst.append(distance_dic[dic_key(req.loc, stn.loc)])  # 위의 딕셔너리에서 값 바로 가져오기
                    except Exception:
                        req_lst.append(get_distance_lat(req.loc, stn.loc))  # 위의 딕셔너리에서 값 바로 가져오기

            dist = min(req_lst)
            req.priority = dist / req.rchg_amount

    def update_priority_stn(target_list: List[Station], target_req: Request):
        for stn in target_list:
            if stn.doable(target_req):
                stn.can_recharge = True
                if isinstance(stn, MovableStation):
                    try:
                        stn.priority = (distance_dic[dic_key(stn.loc, target_req.loc)])  # 위의 딕셔너리에서 값 바로 가져오기
                    except Exception:
                        stn.priority = get_distance_lat(stn.loc, target_req.loc)
                else:
                    try:
                        stn.priority = (distance_dic[dic_key(target_req.loc, stn.loc)])  # 위의 딕셔너리에서 값 바로 가져오기
                    except Exception:
                        stn.priority = get_distance_lat(target_req.loc, stn.loc)
            else:
                stn.can_recharge = False
                stn.priority = PENALTY

# ====================================================================================================================
    def priority(target_list: List[Request], station_list: List[Station]):
        minimum = 10000
        dist = 0
        pri_ans = []
        for req in target_list:
            for stn in station_list:
                if stn.doable(req):
                    stn.can_recharge = True
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
                    stn.can_recharge = False
                    stn.priority = PENALTY

                if dist < minimum:
                    minimum = dist
                    pri_ans.clear()
                    pri_ans.append(req)
                    pri_ans.append(stn)

        return pri_ans[0], pri_ans[1]
# ====================================================================================================================

    while any(req.done is False for req in req_list):
        not_completed_reqs = list(filter(lambda x: (x.done is False), req_list))
        # update_priority_req(not_completed_reqs, stn_list)  # 여기 등장.
        # not_completed_reqs.sort(key=lambda x: x.priority, reverse=False)


        servable_stn = list(filter(lambda x: x.can_recharge is True, stn_list))
        # update_priority_stn(servable_stn, not_completed_reqs[0])
        # servable_stn.sort(key=lambda x: x.priority, reverse=False)

        pri_req, pri_stn = priority(not_completed_reqs,servable_stn)

        try:
             # servable_stn[0].recharge(not_completed_reqs[0])
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

    total_algorithm_end = time.time()

    print(f"total_time :{total_algorithm_end - total_algorithm_start:.4f} ")
    print(f"distance_time : {distance_end - distance_start:.4f}")
    print(f"algorithm_time : {(total_algorithm_end - total_algorithm_start) - (distance_end - distance_start):.4f}")

    return solution
