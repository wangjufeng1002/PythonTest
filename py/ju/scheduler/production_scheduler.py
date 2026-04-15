from ortools.sat.python import cp_model


def create_scheduler():
    # 1. 定义问题数据
    # 任务信息：(任务ID, 处理时间, 可选设备列表)
    tasks = [
        (0, 3, [0, 1]),  # 任务0：需3小时，可在设备0或1上执行
        (1, 2, [0]),  # 任务1：需2小时，只能在设备0上执行
        (2, 4, [1]),  # 任务2：需4小时，只能在设备1上执行
        (3, 1, [0, 1]),  # 任务3：需1小时，可在设备0或1上执行
        (4, 5, [0, 1])  # 任务4：需5小时，可在设备0或1上执行
    ]
    # 任务依赖：(前置任务ID, 后置任务ID) → 后置任务必须在前置任务完成后开始
    dependencies = [(0, 3)]  # 任务3必须在任务0完成后开始

    num_machines = 2  # 设备数量（0和1）
    all_machines = range(num_machines)
    all_tasks = range(len(tasks))

    # 2. 创建模型
    model = cp_model.CpModel()

    # 3. 定义变量
    # 每个任务的开始时间、完成时间
    start = {i: model.NewIntVar(0, 100, f'start_{i}') for i in all_tasks}  # 假设最大时间100
    end = {i: model.NewIntVar(0, 100, f'end_{i}') for i in all_tasks}
    # 每个任务分配的设备（0或1）
    machine = {i: model.NewIntVar(0, num_machines - 1, f'machine_{i}') for i in all_tasks}
    # 最大完成时间（优化目标）
    makespan = model.NewIntVar(0, 100, 'makespan')

    # 4. 添加基础约束
    for i in all_tasks:
        task_id, duration, allowed_machines = tasks[i]
        # 约束1：完成时间 = 开始时间 + 处理时间
        model.Add(end[i] == start[i] + duration)
        # 约束2：任务必须分配到允许的设备上
        model.Add(machine[i] in allowed_machines)
        # 约束3：最大完成时间 >= 所有任务的完成时间
        model.Add(makespan >= end[i])

    # 5. 添加资源冲突约束（同一设备上的任务时间不重叠）
    for m in all_machines:
        # 收集分配到设备m的所有任务
        tasks_on_machine = [i for i in all_tasks if model.NewBoolVar(f'on_machine_{i}_{m}').EqualTo(machine[i] == m)]
        # 对设备m上的任务，按开始时间排序，确保前一个任务完成后下一个才开始
        for i in range(len(tasks_on_machine)):
            for j in range(i + 1, len(tasks_on_machine)):
                t1 = tasks_on_machine[i]
                t2 = tasks_on_machine[j]
                # 两种可能：t1在t2前完成 或 t2在t1前完成
                model.Add(end[t1] <= start[t2]) or (model.Add(end[t2] <= start[t1]))

    # 6. 添加任务依赖约束
    for (prev, curr) in dependencies:
        model.Add(start[curr] >= end[prev])  # 后置任务开始时间 >= 前置任务完成时间

    # 7. 设置优化目标：最小化最大完成时间
    model.Minimize(makespan)

    # 8. 求解
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    # 9. 输出结果
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print(f"排产结果（总完成时间：{solver.Value(makespan)}小时）：")
        print("任务ID | 开始时间 | 完成时间 | 设备")
        print("-" * 35)
        for i in all_tasks:
            print(
                f"   {i:2d}   |    {solver.Value(start[i]):2d}    |    {solver.Value(end[i]):2d}    |   {solver.Value(machine[i])}")
    else:
        print("未找到可行的排产方案")


if __name__ == "__main__":
    create_scheduler()
