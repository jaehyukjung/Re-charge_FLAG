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


if __name__ == '__main__':
    random.seed(42)
    Sample = LoadProb()
    Solution = solver.rule_solver(Sample)
    print('Solved and objective value is ' + str(Solution['Objective']))
