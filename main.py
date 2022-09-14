import random
import prob_builder as prob
import solver, j_solver, s_solver, m_solver, j_test, new_solver, dist_solver
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
    random_req = random.randint(5,8)
    random_stn = random.randint(1,2)
    random_Mstn = random.randint(1,2)

    ThisProb = prob.Prob_Instance()
    for i in range(random_req):
        ThisProb.req_list.append(prob.Request(i+1, [random.uniform(37.4, 37.9), random.uniform(127.0, 127.9)], random.uniform(2, 70), random.uniform(0.001, 3.99)))

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
    jae_list, only_dist_list, random_list, test_list = [[], [], []], [[], [], []],[[], [], []],[[], [], []]

    while(i < 10):
        n = random.randint(1,1000)
        random.seed(n)
        Print_LoadProb(n)

        Sample = random_LoadProb(n)
        Solution = solver.random_rule_solver(Sample)
        random_list[0].append(round(Solution['Objective'][0],4))
        random_list[1].append(round(Solution['Objective'][1], 4))
        random_list[2].append(round(Solution['Objective'][2], 4))

        Sample = random_LoadProb(n)
        Jae_Solution = new_solver.rule_solver(Sample)
        jae_list[0].append(round(Jae_Solution['Objective'][0], 4))
        jae_list[1].append(round(Jae_Solution['Objective'][1], 4))
        jae_list[2].append(round(Jae_Solution['Objective'][2], 4))

        Sample =random_LoadProb(n)
        Dist_Solution = dist_solver.rule_solver(Sample)
        only_dist_list[0].append(round(Dist_Solution['Objective'][0], 4))
        only_dist_list[1].append(round(Dist_Solution['Objective'][1], 4))
        only_dist_list[2].append(round(Dist_Solution['Objective'][2], 4))

        i += 1


    solution_dic = {'random': random_list[0],'jaehyuk': jae_list[0],'dist': only_dist_list[0]}
    df = pd.DataFrame(solution_dic)
    df.to_csv("total_time_pd.csv", encoding='cp949')

    solution_dic = {'random': random_list[1], 'jaehyuk': jae_list[1], 'dist': only_dist_list[1]}
    df = pd.DataFrame(solution_dic)
    df.to_csv("wait_time_pd.csv", encoding='cp949')

    solution_dic = {'random': random_list[2], 'jaehyuk': jae_list[2], 'dist': only_dist_list[2]}
    df = pd.DataFrame(solution_dic)
    df.to_csv("total_distance_pd.csv", encoding='cp949')