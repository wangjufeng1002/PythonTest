import random
import numpy as np
from deap import base, creator, tools, algorithms

# -------------------------- 1. 定义问题参数 --------------------------
# 任务参数：索引=任务ID（0-9对应T0-T9），值=(加工时间, 依赖任务列表, 可选设备列表)
# 设备用0-2表示（M0=0, M1=1, M2=2）
TASKS = [
    (4, [], [0]),  # T0: 4h, 无依赖, 仅M0
    (3, [], [1]),  # T1: 3h, 无依赖, 仅M1
    (5, [0], [0, 2]),  # T2: 5h, 依赖T0, M0/M2
    (6, [1], [1, 2]),  # T3: 6h, 依赖T1, M1/M2
    (2, [], [0, 1, 2]),  # T4: 2h, 无依赖, 所有设备
    (4, [2], [0, 2]),  # T5: 4h, 依赖T2, M0/M2
    (3, [3], [1]),  # T6: 3h, 依赖T3, 仅M1
    (5, [4], [0, 1]),  # T7: 5h, 依赖T4, M0/M1
    (6, [5], [2]),  # T8: 6h, 依赖T5, 仅M2
    (4, [6, 7], [2])  # T9: 4h, 依赖T6+T7, 仅M2
]
NUM_TASKS = len(TASKS)
NUM_MACHINES = 3  # M0-M2

# -------------------------- 2. DEAP工具箱初始化 --------------------------
# 定义适应度函数（最小化目标：总工期+冲突惩罚）
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))  # weights=-1表示最小化
# 定义个体（列表类型，关联适应度）
creator.create("Individual", list, fitness=creator.FitnessMin)

# 创建工具箱
toolbox = base.Toolbox()

# 注册个体生成：每个任务的优先级是0-99的随机整数
toolbox.register("attr_priority", random.randint, 0, 99)
# 注册种群生成：个体长度=任务数，种群=多个个体
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_priority, n=NUM_TASKS)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)


# -------------------------- 3. 适应度函数实现（核心解码逻辑） --------------------------
def evaluate(individual):
    """
    评估个体：解码优先级→生成排程→计算总工期+冲突惩罚
    :param individual: 个体（优先级数组）
    :return: 适应度值（总工期+冲突惩罚）
    """
    # 1. 按优先级排序任务（优先级越小越先执行），生成任务候选顺序
    task_priority = [(task_id, priority) for task_id, priority in enumerate(individual)]
    task_candidate_order = [t[0] for t in sorted(task_priority, key=lambda x: x[1])]

    # 2. 解码：生成满足依赖约束的可行排程顺序（过滤掉未完成前序的任务）
    feasible_order = []
    completed_tasks = set()  # 已完成的任务
    while len(feasible_order) < NUM_TASKS:
        for task_id in task_candidate_order:
            if task_id not in feasible_order:
                # 检查依赖：所有前序任务是否已完成
                dependencies = TASKS[task_id][1]
                if all(dep in completed_tasks for dep in dependencies):
                    feasible_order.append(task_id)
                    completed_tasks.add(task_id)
                    break

    # 3. 资源分配：为每个任务分配最早可用的兼容设备，计算S/E时间
    machine_end_time = [0.0] * NUM_MACHINES  # 每台设备的最早可用时间
    task_s = [0.0] * NUM_TASKS  # 任务开始时间
    task_e = [0.0] * NUM_TASKS  # 任务结束时间
    task_machine = [-1] * NUM_TASKS  # 任务分配的设备
    conflict_penalty = 0.0  # 冲突惩罚（每冲突1次+10h）

    for task_id in feasible_order:
        process_time, dependencies, allowed_machines = TASKS[task_id]

        # 计算任务的最早可能开始时间（需满足：前序任务完成 + 设备可用）
        max_predecessor_e = max([task_e[dep] for dep in dependencies]) if dependencies else 0.0

        # 遍历兼容设备，选择最早可用的设备
        best_machine = None
        earliest_start = float('inf')
        for machine in allowed_machines:
            # 设备的最早可用时间
            machine_available = machine_end_time[machine]
            # 任务的最早开始时间=max(前序完成时间, 设备可用时间)
            start_time = max(max_predecessor_e, machine_available)
            if start_time < earliest_start:
                earliest_start = start_time
                best_machine = machine

        # 分配设备并记录时间（检测冲突：理论上不会冲突，此处为保险）
        if best_machine is None:
            conflict_penalty += 100.0  # 无可用设备，严重冲突
            continue

        # 检查冲突（同一设备同一时间是否有其他任务）
        for t in feasible_order[:feasible_order.index(task_id)]:
            if task_machine[t] == best_machine and not (
                    task_e[t] <= earliest_start or task_s[t] >= earliest_start + process_time):
                conflict_penalty += 10.0

        # 更新任务和设备状态
        task_s[task_id] = earliest_start
        task_e[task_id] = earliest_start + process_time
        task_machine[task_id] = best_machine
        machine_end_time[best_machine] = task_e[task_id]

    # 4. 计算适应度：总工期（所有任务的最大结束时间）+ 冲突惩罚
    total_makespan = max(task_e) if task_e else 0.0
    fitness = total_makespan + conflict_penalty
    return (fitness,)  # DEAP要求返回元组


# 注册适应度函数
toolbox.register("evaluate", evaluate)

# -------------------------- 4. 遗传操作注册 --------------------------
toolbox.register("mate", tools.cxTwoPoint)  # 两点交叉
toolbox.register("mutate", tools.mutUniformInt, low=0, up=99, indpb=0.1)  # 变异概率10%
toolbox.register("select", tools.selTournament, tournsize=3)  # 锦标赛选择（3个个体竞争）


# -------------------------- 5. 进化算法运行 --------------------------
def main():
    random.seed(42)  # 固定种子，可复现

    # 初始化种群（种群大小=50）
    pop = toolbox.population(n=50)
    # 进化参数（可调整）
    NGEN = 100  # 迭代次数
    CXPB = 0.7  # 交叉概率
    MUTPB = 0.2  # 变异概率

    # 记录最优解
    best_ind = None
    best_fitness = float('inf')

    print("开始进化...")
    for gen in range(NGEN):
        # 1. 选择下一代（父代）
        offspring = toolbox.select(pop, len(pop))
        offspring = list(map(toolbox.clone, offspring))

        # 2. 交叉（CXPB概率）
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < CXPB:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        # 3. 变异（MUTPB概率）
        for mutant in offspring:
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        # 4. 评估未计算适应度的个体
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # 5. 更新种群（子代替换父代）
        pop[:] = offspring

        # 6. 记录并打印当前最优解
        current_best = tools.selBest(pop, 1)[0]
        current_fitness = current_best.fitness.values[0]
        if current_fitness < best_fitness:
            best_fitness = current_fitness
            best_ind = toolbox.clone(current_best)

        if (gen + 1) % 10 == 0:
            print(
                f"第{gen + 1}代 | 最优适应度：{current_fitness:.2f} | 总工期：{current_fitness - (current_fitness - max([TASKS[t][0] for t in range(NUM_TASKS)])):.2f}")

    # -------------------------- 6. 输出最优排程结果 --------------------------
    print("\n" + "=" * 50)
    print("进化完成！最优排程结果：")
    print(f"最优适应度值：{best_fitness:.2f}")
    print(f"最优优先级编码：{best_ind}")

    # 解码最优个体，输出详细排程
    _, _, task_s, task_e, task_machine = decode_best_ind(best_ind)
    print("\n详细排程表：")
    print(f"{'任务ID':<6} {'依赖任务':<10} {'加工时间':<8} {'分配设备':<8} {'开始时间':<8} {'结束时间':<8}")
    for task_id in range(NUM_TASKS):
        dependencies = TASKS[task_id][1]
        dep_str = ",".join(map(str, dependencies)) if dependencies else "无"
        machine_str = f"M{task_machine[task_id]}"
        print(
            f"T{task_id:<4} {dep_str:<10} {TASKS[task_id][0]:<8} {machine_str:<8} {task_s[task_id]:<8.1f} {task_e[task_id]:<8.1f}")
    print(f"\n总工期：{max(task_e):.1f}h")
    print(f"资源冲突：{'无' if (best_fitness - max(task_e)) < 1e-6 else '有'}")


def decode_best_ind(best_ind):
    """解码最优个体，返回详细排程信息（复用evaluate中的解码逻辑）"""
    task_priority = [(task_id, priority) for task_id, priority in enumerate(best_ind)]
    task_candidate_order = [t[0] for t in sorted(task_priority, key=lambda x: x[1])]

    feasible_order = []
    completed_tasks = set()
    while len(feasible_order) < NUM_TASKS:
        for task_id in task_candidate_order:
            if task_id not in feasible_order:
                dependencies = TASKS[task_id][1]
                if all(dep in completed_tasks for dep in dependencies):
                    feasible_order.append(task_id)
                    completed_tasks.add(task_id)
                    break

    machine_end_time = [0.0] * NUM_MACHINES
    task_s = [0.0] * NUM_TASKS
    task_e = [0.0] * NUM_TASKS
    task_machine = [-1] * NUM_TASKS

    for task_id in feasible_order:
        process_time, dependencies, allowed_machines = TASKS[task_id]
        max_predecessor_e = max([task_e[dep] for dep in dependencies]) if dependencies else 0.0

        best_machine = None
        earliest_start = float('inf')
        for machine in allowed_machines:
            machine_available = machine_end_time[machine]
            start_time = max(max_predecessor_e, machine_available)
            if start_time < earliest_start:
                earliest_start = start_time
                best_machine = machine

        task_s[task_id] = earliest_start
        task_e[task_id] = earliest_start + process_time
        task_machine[task_id] = best_machine
        machine_end_time[best_machine] = task_e[task_id]

    return feasible_order, task_priority, task_s, task_e, task_machine


if __name__ == "__main__":
    main()