from prob_builder import *
from typing import List
PENALTY = 1000000

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

    def update_priority_req(target_list: List[Request]):
        for req in target_list:
            req.priority = req.time_wdw[0]

    def update_priority_stn(target_list: List[Station], target_req: Request):
        for stn in target_list:
            if stn.doable(target_req):
                stn.can_recharge = True
                stn.priority = stn.avail_time
            else:
                stn.can_recharge = False
                stn.priority = PENALTY
#=====================================================================================
    while any(req.done is False for req in req_list):
        update_priority_req(req_list) # 차량에 대한 우선순위배정
        # 이해하기---------------------------------
        not_completed_reqs = list(filter(lambda x: (x.done is False), req_list))
        not_completed_reqs.sort(key=lambda x: x.priority, reverse=False)
        # 우선순위는 랜덤배정

        # -----------------


        # -----------------

        # 이해하기---------------------------------

        update_priority_stn(stn_list, not_completed_reqs[0]) # 주유소에 대한 우선순위배정
        servable_stn = list(filter(lambda x: x.can_recharge is True, stn_list))
        servable_stn.sort(key=lambda x: x.priority, reverse=False)

        try:
            servable_stn[0].recharge(not_completed_reqs[0])
        except Exception:
            raise Exception('Invalid Logic')
            break
# =====================================================================================
    solution['Snapshop_Requests'] = req_list
    solution['Snapshop_Stations'] = stn_list
    total_distance = 0
    for stn in stn_list:
        total_distance += stn.measures['total_distance']
    solution['Objective'] = total_distance
    return solution