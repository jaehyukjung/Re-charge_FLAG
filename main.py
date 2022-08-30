import random
import prob_builder as prob
import solver, j_solver, s_solver, m_solver
import pandas as pd


def LoadProb():
    ThisProb = prob.Prob_Instance()
    ThisProb.req_list.append(prob.Request(1, [40.75458, -73.9936], 22.599))
    ThisProb.req_list.append(prob.Request(2, [40.80282, -73.9389], 67.3405))
    ThisProb.req_list.append(prob.Request(3, [40.84842, -73.9318], 52.207))
    ThisProb.req_list.append(prob.Request(4, [40.81842, -73.9468], 92.207))
    ThisProb.req_list.append(prob.Request(5, [40.82842, -73.9358], 42.207))
    ThisProb.req_list.append(prob.Request(6, [40.83842, -73.9848], 32.207))
    ThisProb.req_list.append(prob.Request(7, [40.74842, -73.9938], 42.207))
    ThisProb.req_list.append(prob.Request(8, [40.89842, -73.9628], 2.207))


    ThisProb.stn_list.append(prob.Station(1, [40.7956, -73.9738]))
    ThisProb.stn_list.append(prob.Station(3, [40.8486, -73.9328]))
    ThisProb.stn_list.append(prob.MovableStation(2, [40.74629, -73.9966], moveSpeed=60))

    return ThisProb
def random_LoadProb(n):
    random.seed(n)
    random_req = random.randint(3,5)
    random_stn = random.randint(1,3)
    random_Mstn = random.randint(1,3)

    ThisProb = prob.Prob_Instance()
    for i in range(random_req):
        ThisProb.req_list.append(prob.Request(i+1, [random.uniform(37.4, 37.9), random.uniform(127.0, 127.9)], random.uniform(2, 70)))

    for i in range(random_stn):
        ThisProb.stn_list.append(prob.Station(i+1, [random.uniform(37.4, 37.9), random.uniform(127.0, 127.9)]))

    for i in range(random_Mstn):
        ThisProb.stn_list.append(prob.MovableStation(i+random_stn+1, [random.uniform(37.4, 37.9), random.uniform(127.0, 127.9)], moveSpeed=60))

    return ThisProb

def Print_LoadProb(n):
    print(random_LoadProb(n))

if __name__ == '__main__':

    random.seed(42)
    i = 0
    jae_list, su_list, min_list, random_list = [], [], [], []

    while(i < 10):
        n = random.randint(1,1000)
        random.seed(n)
        Print_LoadProb(n)

        # print('Random Solver Start')
        # for i in range(30):
        Sample = random_LoadProb(n)
        Solution = solver.random_rule_solver(Sample)
        random_list.append(round(Solution['Objective'],4))
        # mean = sum(random_lst)/len(random_lst)
        # random_lst.append(mean)
        # print('Solved and objective Mean value is ' + str(mean) + '\n')

        Sample = random_LoadProb(n)
        Jae_Solution = j_solver.rule_solver(Sample)
        jae_list.append(round(Jae_Solution['Objective'], 4))

        Sample = random_LoadProb(n)
        Su_Solution = s_solver.subin_rule_solver(Sample)
        su_list.append(round(Su_Solution['Objective'], 4))

        Sample =random_LoadProb(n)
        Min_Solution = m_solver.minseok_rule_solver(Sample)
        min_list.append(round(Min_Solution['Objective'], 4))


        i += 1

    df = pd.DataFrame({"random": random_list,
                       "재혁": jae_list,
                       "수빈": su_list,
                        "민석": min_list})
    df.to_csv("output_pd.csv", encoding='cp949')