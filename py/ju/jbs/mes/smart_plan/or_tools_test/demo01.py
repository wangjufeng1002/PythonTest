# 1. 导入 OR-Tools 的线性规划求解器模块
from ortools.linear_solver import pywraplp

# 2. 创建求解器（指定求解器类型，这里用 CBC 求解器，支持整数规划）
solver = pywraplp.Solver.CreateSolver('CBC')
if not solver:
    print("无法创建求解器，可能是环境问题！")
    exit()

# 3. 定义决策变量（非负整数变量）
# 参数说明：变量名、下界、上界、变量类型（INTEGER 整数 / CONTINUOUS 连续）
x = solver.IntVar(0, solver.infinity(), 'Product_A')  # A产品数量，下界0，上界无穷大
y = solver.IntVar(0, solver.infinity(), 'Product_B')  # B产品数量，下界0，上界无穷大

print('变量数量：', solver.NumVariables())  # 输出变量数量，预期为2

# 4. 定义约束条件
# 约束1：2x + y ≤ 10
constraint1 = solver.Add(2 * x + y <= 10, 'Constraint_RawMaterial1')
# 约束2：x + 3y ≤ 12
constraint2 = solver.Add(x + 3 * y <= 12, 'Constraint_RawMaterial2')

print('约束条件数量：', solver.NumConstraints())  # 输出约束数量，预期为2

# 5. 定义目标函数（最大化总利润 5x + 4y）
solver.Maximize(5 * x + 4 * y)

# 6. 调用求解器求解
print('求解状态：', solver.Solve())  # 求解状态为 0 表示求解成功

# 7. 解析求解结果
if solver.Solve() == pywraplp.Solver.OPTIMAL:
    print('\n==== 最优解结果 ====')
    print(f'最大总利润：{solver.Objective().Value():.2f} 元')
    print(f'生产 A 产品数量：{x.solution_value()} 件')
    print(f'生产 B 产品数量：{y.solution_value()} 件')
    print('\n==== 约束条件满足情况 ====')
    print(f'原料 1 消耗：{2 * x.solution_value() + y.solution_value()} 单位（上限10单位）')
    print(f'原料 2 消耗：{x.solution_value() + 3 * y.solution_value()} 单位（上限12单位）')
else:
    print('未找到最优解，可能问题无可行解或无界！')