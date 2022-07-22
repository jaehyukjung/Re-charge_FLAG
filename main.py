import prob_builder as prob
import solver

def LoadProb():
    ThisProb = prob.Prob_Instance()
    temp1 = prob.Request()
    ThisProb.req_list.append(prob.Request(1))
    ThisProb.req_list.append(prob.Request(2))
    ThisProb.req_list.append(prob.Request(3))
    ThisProb.stn_list.append(prob.Station(1))
    ThisProb.stn_list.append(prob.MovableStation(2, moveSpeed=35))
    ThisProb.stn_list.append(prob.Station(3))
    print(ThisProb)
    return ThisProb


if __name__ == '__main__':
    random.seed(42)
    Sample = LoadProb() ## 문제정의
    Solution = solver.rule_solver(Sample)  ## 문제 풀이(solver에다 대입) (go to => ctrl B)
    print('Solved and objective value is ' + str(Solution['Objective'])) ## 해답 출력