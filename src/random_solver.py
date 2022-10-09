import random
from prob_builder import *
from typing import List
from distance import distance_diction

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

    distance_dic = distance_diction(req_list, stn_list)

    def random_priority(target, station_list: List[Station]):
        for stn in station_list:
            stn.priority = random.randint(1,1000000)

        return target, min(station_list, key = lambda x: x.priority)

    for req in req_list:
        for stn in stn_list:
            if isinstance(stn, MovableStation):
                req.dist_list.append(distance_dic[dic_key(stn.loc, req.loc)])
            else:
                req.dist_list.append(distance_dic[dic_key(req.loc, stn.loc)])

        spare_time = (sum(req.dist_list)/len(req.dist_list)) / req.speed

        req.time_wdw[1] += spare_time

    while any(req.done is False for req in req_list):
        not_completed_reqs = list(filter(lambda x: (x.done is False), req_list))
        pri_req = min(not_completed_reqs,key = lambda x: (x.start_time))
        servable_stn = list(filter(lambda x: x.can_recharge is True, stn_list))
        pri_req, pri_stn = random_priority(pri_req,servable_stn) # 랜덤
        try:
             pri_stn.recharge(pri_req)
        except Exception:
            raise Exception('Invalid Logic')
            break

    solution['Snapshop_Requests'] = req_list
    solution['Snapshop_Stations'] = stn_list

    total_wait = 0
    total_distance = 0
    total_tardiness = 0

    for stn in stn_list:
        total_distance += stn.measures['total_distance']
        total_wait += stn.measures['total_wait']

    for req in req_list:
        total_tardiness += req.tardiness

    solution['Objective'] = []
    solution['Objective'].append(total_tardiness)
    solution['Objective'].append(total_wait)
    solution['Objective'].append((total_distance))
    return solution
