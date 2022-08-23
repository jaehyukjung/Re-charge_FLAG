import random
import prob_builder as prob
import solver, j_solver, s_solver, m_solver
import pandas as pd


def LoadProb():
    ThisProb = prob.Prob_Instance()
    ThisProb.req_list.append(prob.Request(1, [40.75458, -73.9936], 22.599))
    ThisProb.req_list.append(prob.Request(2, [40.80282, -73.9389], 67.3405))
    ThisProb.req_list.append(prob.Request(3, [40.84842, -73.9318], 238.207))
    ThisProb.req_list.append(prob.Request(4, [40.81842, -73.9468], 24.207))
    ThisProb.req_list.append(prob.Request(5, [40.82842, -73.9358], 9.207))
    ThisProb.req_list.append(prob.Request(6, [40.83842, -73.9848], 2.207))
    ThisProb.req_list.append(prob.Request(7, [40.74842, -73.9938], 27.207))
    ThisProb.req_list.append(prob.Request(8, [40.89842, -73.9628], 2.207))


    ThisProb.stn_list.append(prob.Station(1, [40.7956, -73.9738]))
    ThisProb.stn_list.append(prob.Station(3, [40.8486, -73.9328]))
    ThisProb.stn_list.append(prob.MovableStation(2, [40.74629, -73.9966], moveSpeed=60))

    return ThisProb

def Print_LoadProb():
    print(LoadProb())

if __name__ == '__main__':
    random.seed(7)
    Print_LoadProb()

    random_lst = []
    print('Random Solver Start')
    for i in range(30):
        Sample = LoadProb()
        Solution = solver.random_rule_solver(Sample)
        # print(' Solved and objective value is ' + str(Solution['Objective']))
        random_lst.append(round(Solution['Objective'],4))
    mean = sum(random_lst)/len(random_lst)
    random_lst.append(mean)
    print('Solved and objective Mean value is ' + str(mean) + '\n')

    Sample = LoadProb()
    Jae_Solution = j_solver.rule_solver(Sample)
    print('jaehyuk : Solved and objective value is ' + str(Jae_Solution['Objective']) + '\n')

    Sample = LoadProb()
    Su_Solution = s_solver.subin_rule_solver(Sample)
    print('subin : Solved and objective value is ' + str(Su_Solution['Objective']) + '\n')

    Sample = LoadProb()
    Min_Solution = m_solver.minseok_rule_solver(Sample)
    print('minseok : Solved and objective value is ' + str(Min_Solution['Objective']))

    df = pd.DataFrame({"random": random_lst,
                       "재혁": round(Jae_Solution['Objective'], 4),
                       "수빈": round(Su_Solution['Objective'], 4),
                        "민석": round(Min_Solution['Objective'], 4)})
    df.to_csv("output_pd.csv")


