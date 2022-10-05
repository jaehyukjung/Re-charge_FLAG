import random
import prob_builder as prob
import solver, old_solver_1, old_solver_4, old_solver_3, old_solver_2, new_solver, dist_solver
import pandas as pd

def random_LoadProb(n):
    random.seed(n)
    random_req = random.randint(5,11)
    random_stn = random.randint(3,5)
    random_Mstn = random.randint(1,2)

    ThisProb = prob.Prob_Instance()
    for i in range(random_req):
        ThisProb.req_list.append(prob.Request(i+1, [random.uniform(37.4, 37.9), random.uniform(127.0, 127.9)], random.uniform(2, 70), random.uniform(0.001, 3.99)))
    for i in range(int(random_req/2)):
        ThisProb.req_list.append(prob.Request(random_req+1+i, [random.uniform(37.4, 37.9), random.uniform(127.0, 127.9)], random.uniform(2, 70), random.uniform(1.001, 1.99)))

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
    jae_list, only_dist_list, random_list = [[], [], []], [[], [], []],[[], [], []]

    while(i < 30):
        n = random.randint(1,1000)
        random.seed(n)
        Print_LoadProb(n)

        Sample = random_LoadProb(n)
        Solution = solver.random_rule_solver(Sample)
        for j in range(3):
            random_list[j].append(round(Solution['Objective'][j],4))

        Sample = random_LoadProb(n)
        Jae_Solution = new_solver.rule_solver(Sample)
        for j in range(3):
            jae_list[j].append(round(Jae_Solution['Objective'][j], 4))

        Sample = random_LoadProb(n)
        Dist_Solution = dist_solver.rule_solver(Sample)
        for j in range(3):
            only_dist_list[j].append(round(Dist_Solution['Objective'][j], 4))

        i += 1


    solution_dic = {'random': random_list[0],'solver': jae_list[0],'dist': only_dist_list[0]}
    df = pd.DataFrame(solution_dic)
    df.to_csv("tardiness_time_pd.csv", encoding='cp949')

    solution_dic = {'random': random_list[1], 'solver': jae_list[1], 'dist': only_dist_list[1]}
    df = pd.DataFrame(solution_dic)
    df.to_csv("wait_time_pd.csv", encoding='cp949')

    solution_dic = {'random': random_list[2], 'solver': jae_list[2], 'dist': only_dist_list[2]}
    df = pd.DataFrame(solution_dic)
    df.to_csv("total_distance_pd.csv", encoding='cp949')