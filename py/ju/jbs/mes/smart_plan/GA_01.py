import random

# 订单数据：{订单ID: [(工序1机器, 工序1时间), (工序2机器, 工序2时间), ...]}
jobs = {
    'A': [('M1', 3), ('M2', 5)],
    'B': [('M2', 2), ('M1', 4)]
}

# 染色体编码：工序顺序列表，如 ['A1', 'B1', 'A2', 'B2']
def create_individual(jobs):
    operations = []
    for job_id,工序 in jobs.items():
        for i in range(len(工序)):
            operations.append(f"{job_id}{i+1}")  # 生成工序标识
    random.shuffle(operations)  # 随机初始化顺序（需确保同一订单工序顺序？此处简化处理，实际需约束）
    return operations

# 适应度函数：计算Makespan
def calculate_makespan(individual, jobs):
    machine_time = {}  # 记录机器最后结束时间：{机器: 时间}
    job_prev_op = {}    # 记录订单最后工序结束时间：{订单ID: 时间}
    for op in individual:
        job_id = op[0]
        op_idx = int(op[1])-1  # 工序索引（0开始）
        machine, time = jobs[job_id][op_idx]
        # 前序工序结束时间
        prev_time = job_prev_op.get(job_id, 0)
        # 机器可用时间
        machine_available = machine_time.get(machine, 0)
        start_time = max(prev_time, machine_available)
        end_time = start_time + time
        # 更新记录
        job_prev_op[job_id] = end_time
        machine_time[machine] = end_time
    return max(machine_time.values())

# 交叉算子：基于工序的交叉（OXC）
def oxc_crossover(parent1, parent2):
    n = len(parent1)
    start, end = sorted(random.sample(range(n), 2))
    child = [None]*n
    # 保留parent1的中间段
    child[start:end+1] = parent1[start:end+1]
    # 填充parent2的剩余工序（按顺序，且不重复）
    ptr = 0
    for gene in parent2:
        if gene not in child[start:end+1]:
            while child[ptr] is not None:
                ptr += 1
            child[ptr] = gene
            ptr += 1
    return child

# 变异算子：交换两个工序的位置（同一订单工序不交换）
def mutate(individual, jobs):
    individual = individual.copy()
    i, j = random.sample(range(len(individual)), 2)
    # 确保交换的工序不属于同一订单
    if individual[i][0] != individual[j][0]:
        individual[i], individual[j] = individual[j], individual[i]
    return individual

# 遗传算法主流程
def genetic_algorithm(jobs, population_size=100, generations=200):
    # 初始化种群
    population = [create_individual(jobs) for _ in range(population_size)]
    for gen in range(generations):
        # 计算适应度（从小到大排序）
        population_with_fitness = sorted([(ind, calculate_makespan(ind, jobs)) for ind in population], key=lambda x: x[1])
        best_ind, best_fitness = population_with_fitness[0]
        print(f"代{gen+1}: 最优Makespan={best_fitness}, 顺序={best_ind}")
        # 选择（锦标赛选择）
        selected = []
        for _ in range(population_size):
            candidates = random.sample(population_with_fitness, 3)
            selected.append(min(candidates, key=lambda x: x[1])[0])
        # 交叉和变异
        new_population = []
        for i in range(0, population_size, 2):
            parent1 = selected[i]
            parent2 = selected[i+1]
            child1 = oxc_crossover(parent1, parent2)
            child2 = oxc_crossover(parent2, parent1)
            child1 = mutate(child1, jobs)
            child2 = mutate(child2, jobs)
            new_population.extend([child1, child2])
        population = new_population
    # 返回最优解
    best_ind, best_fitness = min([(ind, calculate_makespan(ind, jobs)) for ind in population], key=lambda x: x[1])
    return best_ind, best_fitness

# 运行算法
best_order, min_makespan = genetic_algorithm(jobs)
print("\n最优工序顺序:", best_order)
print("最小完工时间:", min_makespan)