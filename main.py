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
        ThisProb.stn_list.append(prob.MovableStation(i+random_stn+1, [random.uniform(37.4, 37.9), random.uniform(127.0, 127.9)], moveSpeed=60))
    print(ThisProb.stn_list[0].loc[0])
    print(ThisProb)
    return ThisProb

if __name__ == '__main__':
    random.seed(777)


    random_lst = []
    for i in range(30):
        Sample = LoadProb()
        Solution = solver.random_rule_solver(Sample)
        print(str(i+1) + ' Solved and objective value is ' + str(Solution['Objective']))
        random_lst.append(Solution['Objective'])

    print('Solved and objective Mean value is ' + str(sum(random_lst)/len(random_lst)))

    print('==================================================================== \n\n')
    Sample = LoadProb()
    Solution = solver.rule_solver(Sample)
    print('jaehyuk : Solved and objective value is ' + str(Solution['Objective']))

