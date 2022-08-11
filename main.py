import random
import prob_builder as prob
import solver


def LoadProb():
    ThisProb = prob.Prob_Instance()
    ThisProb.req_list.append(prob.Request(1, [40.75458, -73.9936], 22.599))
    ThisProb.req_list.append(prob.Request(2, [40.80282, -73.9389], 67.3405))
    ThisProb.req_list.append(prob.Request(3, [40.84842, -73.9318], 2.207))
    ThisProb.stn_list.append(prob.Station(1, [40.7956, -73.9738]))
    ThisProb.stn_list.append(prob.MovableStation(2, [40.74629, -73.9966], moveSpeed=60))
    print(ThisProb)
    return ThisProb

def random_LoadProb():
    random_req = random.randint(8,10)
    random_stn = random.randint(2,5)
    random_Mstn = random.randint(2,5)

    ThisProb = prob.Prob_Instance()
    for i in range(random_req):
        ThisProb.req_list.append(prob.Request(i+1, [random.uniform(37.4, 37.9), random.uniform(127.0, 127.9)], random.uniform(2, 50)))

    for i in range(random_stn):
        ThisProb.stn_list.append(prob.Station(i+1, [random.uniform(37.4, 37.9), random.uniform(127.0, 127.9)]))

    for i in range(random_Mstn):
        ThisProb.stn_list.append(prob.MovableStation(i+random_stn, [random.uniform(37.4, 37.9), random.uniform(127.0, 127.9)], moveSpeed=60))

    print(ThisProb)
    return ThisProb

if __name__ == '__main__':
    random.seed(777)
    Sample = random_LoadProb()
    Solution = solver.rule_solver(Sample)
    print('Solved and objective value is ' + str(Solution['Objective']))
