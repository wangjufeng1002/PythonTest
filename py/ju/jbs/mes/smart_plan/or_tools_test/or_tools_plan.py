from ortools.sat.python import cp_model
import datetime

# ===================== 1. 基础配置与模拟数据 =====================
SHIFT_WHITE = 0
SHIFT_NIGHT = 1
MAX_SHIFT = 40  # 最大排产班次（20天）
MAX_INJECTION_SUBTASKS = 15  # 增加子任务数，降低求解失败概率
OVERDUE_WEIGHT = 20  # 超期惩罚权重（大幅提高，优先减少超期）

# 基准日期与订单数据
BASE_DATE = datetime.date(2025, 10, 1)
orders = {
    "O1": {"due_date": datetime.date(2025, 10, 10), "final_product": "P1", "qty": 200},
    "O2": {"due_date": datetime.date(2025, 10, 12), "final_product": "P2", "qty": 300},
    #"O3": {"due_date": datetime.date(2025, 10, 15), "final_product": "P1", "qty": 150}
}
# 转换交货期为班次ID
for order_id, order in orders.items():
    days_diff = (order["due_date"] - BASE_DATE).days
    order["due_shift"] = days_diff * 2 + 1  # 交货期=当天夜班结束

# BOM结构：父物料 → {子物料: (配比, 提前班次)}
bom_structure = {
    "P1": {"S1": (2, 2)},  # 1P1=2S1，组装提前2班
    "P2": {"S2": (1, 2)},  # 1P2=1S2，组装提前2班
    "S1": {"I1": (1, 3)},  # 1S1=1I1，机加提前3班
    "S2": {"I2": (1, 3)}  # 1S2=1I2，机加提前3班
}

# 注塑资源：机台+模具组合的班产能
injection_resources = {
    "M1_M101": {"machine": "M1", "mold": "M101", "white_cap": 100, "night_cap": 90},
    "M1_M102": {"machine": "M1", "mold": "M102", "white_cap": 80, "night_cap": 75},
    "M2_M101": {"machine": "M2", "mold": "M101", "white_cap": 95, "night_cap": 85},
    "M2_M102": {"machine": "M2", "mold": "M102", "white_cap": 85, "night_cap": 80},
}
# 注塑半成品→可用资源映射
injection_semi_mapping = {
    "I1": ["M1_M101", "M2_M101"],  # I1仅用M101模具
    "I2": ["M1_M102", "M2_M102"]  # I2仅用M102模具
}

# 机加/组装班产能
machining_cap = {"white": 200, "night": 180}
assembly_cap = {"white": 300, "night": 280}

# ===================== 2. 任务初始化（区分主任务/子任务） =====================
# 2.1 统计半成品总需求
semi_demand = {}
for order_id, order in orders.items():
    final_product = order["final_product"]
    final_qty = order["qty"]
    # 成品→机加半成品
    if final_product in bom_structure:
        for semi, (ratio, _) in bom_structure[final_product].items():
            demand_qty = final_qty * ratio
            semi_demand[semi] = semi_demand.get(semi, 0) + demand_qty
            # 机加→注塑半成品
            if semi in bom_structure:
                for injection_semi, (ratio2, _) in bom_structure[semi].items():
                    injection_demand = demand_qty * ratio2
                    semi_demand[injection_semi] = semi_demand.get(injection_semi, 0) + injection_demand

# 2.2 定义任务结构（主任务：注塑/机加/组装；子任务：仅注塑）
tasks = {}  # 所有主任务
injection_subtasks = {}  # 注塑子任务（动态拆分用）
task_id = 0

# ① 注塑主任务（记录总需求，不直接生产）
for semi_id, total_qty in semi_demand.items():
    if semi_id.startswith("I"):
        tasks[f"T{task_id}"] = {
            "type": "injection_main",
            "semi_id": semi_id,
            "total_qty": total_qty,
            "available_res": injection_semi_mapping[semi_id],
            "subtask_ids": []  # 关联的子任务ID
        }
        # 为每个注塑主任务预创建子任务
        for subtask_idx in range(MAX_INJECTION_SUBTASKS):
            subtask_id = f"IST{task_id}_{subtask_idx}"
            injection_subtasks[subtask_id] = {
                "main_task_id": f"T{task_id}",
                "semi_id": semi_id,
                "available_res": injection_semi_mapping[semi_id]
            }
            tasks[f"T{task_id}"]["subtask_ids"].append(subtask_id)
        task_id += 1

# ② 机加主任务
for semi_id, total_qty in semi_demand.items():
    if semi_id.startswith("S"):
        tasks[f"T{task_id}"] = {
            "type": "machining",
            "semi_id": semi_id,
            "total_qty": total_qty
        }
        task_id += 1

# ③ 组装主任务（按订单拆分，固定任务）
for order_id, order in orders.items():
    tasks[f"T{task_id}"] = {
        "type": "assembly",
        "semi_id": order["final_product"],
        "total_qty": order["qty"],
        "order_id": order_id,
        "due_shift": order["due_shift"]
    }
    task_id += 1

# ===================== 3. 初始化CP-SAT模型 =====================
model = cp_model.CpModel()

# ===================== 4. 定义变量 =====================
# 4.1 主任务变量
t_start = {}  # 主任务开始班次（机加/组装）
t_end = {}  # 主任务结束班次（机加/组装）
t_prod_shifts = {}  # 主任务生产班次数量（机加/组装）
t_qty = {}  # 主任务产量（机加/组装）
t_inventory = {}  # 主任务库存持有班次
t_shift_cap = {}  # 修复点：单独定义班产能变量，避免作用域问题
order_delay = {}  # 订单延期班次（允许为正，即超期）

# 初始化主任务变量
for task_id, task in tasks.items():
    if task["type"] == "injection_main":
        continue  # 注塑主任务无时间变量，仅关联子任务
    # 机加/组装任务变量（放宽结束班次上限，允许超期）
    t_start[task_id] = model.NewIntVar(0, MAX_SHIFT, f"t_start_{task_id}")
    t_end[task_id] = model.NewIntVar(0, MAX_SHIFT + 20, f"t_end_{task_id}")  # 允许超期20个班次（10天）
    t_prod_shifts[task_id] = model.NewIntVar(1, MAX_SHIFT, f"t_prod_shifts_{task_id}")
    model.Add(t_prod_shifts[task_id] == t_end[task_id] - t_start[task_id])
    t_qty[task_id] = model.NewIntVar(task["total_qty"], task["total_qty"] * 2, f"t_qty_{task_id}")
    t_inventory[task_id] = model.NewIntVar(0, MAX_SHIFT + 20, f"t_inventory_{task_id}")
    # 修复点：显式初始化班产能变量
    t_shift_cap[task_id] = model.NewIntVar(1, 300, f"t_shift_cap_{task_id}")

# 订单延期变量（允许超期，上限放宽）
for order_id in orders.keys():
    order_delay[order_id] = model.NewIntVar(0, MAX_SHIFT + 20, f"order_delay_{order_id}")

# 4.2 注塑子任务变量（动态拆分核心）
ist_start = {}  # 子任务开始班次（1个班次=1个子任务）
ist_end = {}  # 子任务结束班次（start+1，仅占用1个班次）
ist_enabled = {}  # 子任务是否启用（0=禁用，1=启用）
ist_resource = {}  # 子任务资源分配（资源索引）
ist_shift_cap = {}  # 子任务班产能
ist_qty = {}  # 子任务产量

for subtask_id, subtask in injection_subtasks.items():
    # 时间变量：子任务仅占用1个班次（end = start + 1）
    ist_start[subtask_id] = model.NewIntVar(0, MAX_SHIFT + 20, f"ist_start_{subtask_id}")  # 允许超期排产
    ist_end[subtask_id] = model.NewIntVar(0, MAX_SHIFT + 20, f"ist_end_{subtask_id}")
    model.Add(ist_end[subtask_id] == ist_start[subtask_id] + 1)

    # 启用变量：0=禁用（产量=0），1=启用（产量>0）
    ist_enabled[subtask_id] = model.NewBoolVar(f"ist_enabled_{subtask_id}")

    # 资源分配变量
    res_count = len(subtask["available_res"])
    ist_resource[subtask_id] = model.NewIntVar(0, res_count - 1, f"ist_resource_{subtask_id}")

    # 班产能变量
    ist_shift_cap[subtask_id] = model.NewIntVar(1, 200, f"ist_shift_cap_{subtask_id}")

    # 产量变量：禁用时产量=0，启用时≤班产能
    ist_qty[subtask_id] = model.NewIntVar(0, 200, f"ist_qty_{subtask_id}")
    model.Add(ist_qty[subtask_id] == 0).OnlyEnforceIf(ist_enabled[subtask_id].Not())
    model.Add(ist_qty[subtask_id] > 0).OnlyEnforceIf(ist_enabled[subtask_id])

# ===================== 5. 添加核心约束 =====================
# 5.1 注塑子任务约束（动态拆分核心）
# 5.1.1 子任务资源+班次无冲突
machine_mold_shift_occ = {}
for subtask_id, subtask in injection_subtasks.items():
    res_ids = subtask["available_res"]
    # 遍历子任务可能的资源
    for res_idx, res_id in enumerate(res_ids):
        res_info = injection_resources[res_id]
        machine = res_info["machine"]
        mold = res_info["mold"]

        # 资源选择布尔变量
        is_res = model.NewBoolVar(f"is_res_{subtask_id}_{res_idx}")
        model.Add(ist_resource[subtask_id] == res_idx).OnlyEnforceIf(is_res)

        # 班次占用布尔变量（仅启用且选择该资源时占用）
        for shift in range(MAX_SHIFT + 20):  # 覆盖超期班次
            is_occ = model.NewBoolVar(f"is_occ_{subtask_id}_{shift}")
            model.Add(shift >= ist_start[subtask_id]).OnlyEnforceIf(is_occ)
            model.Add(shift < ist_end[subtask_id]).OnlyEnforceIf(is_occ)

            # 合并启用+资源+班次占用
            occ_res = model.NewBoolVar(f"occ_res_{subtask_id}_{res_idx}_{shift}")
            model.AddBoolAnd([ist_enabled[subtask_id], is_res, is_occ]).OnlyEnforceIf(occ_res)

            # 记录机台+模具+班次占用
            key = (machine, mold, shift)
            if key not in machine_mold_shift_occ:
                machine_mold_shift_occ[key] = []
            machine_mold_shift_occ[key].append(occ_res)

# 约束：同一机台+模具+班次只能被1个子任务占用
for key, occ_list in machine_mold_shift_occ.items():
    model.Add(sum(occ_list) <= 1)

# 5.1.2 子任务班产能约束（根据资源+班次类型动态赋值）
for subtask_id, subtask in injection_subtasks.items():
    res_ids = subtask["available_res"]
    # 遍历可用资源
    for res_idx, res_id in enumerate(res_ids):
        res_info = injection_resources[res_id]
        is_res = model.NewBoolVar(f"is_res_{subtask_id}_{res_idx}")
        model.Add(ist_resource[subtask_id] == res_idx).OnlyEnforceIf(is_res)

        # 模运算判断班次类型（白班=偶数，夜班=奇数）
        remainder = model.NewIntVar(0, 1, f"remainder_{subtask_id}")
        model.AddModuloEquality(remainder, ist_start[subtask_id], 2)

        # 白班产能约束
        is_white = model.NewBoolVar(f"is_white_{subtask_id}")
        model.Add(remainder == 0).OnlyEnforceIf(is_white)
        model.Add(ist_shift_cap[subtask_id] == res_info["white_cap"]).OnlyEnforceIf(is_res, is_white)

        # 夜班产能约束
        is_night = model.NewBoolVar(f"is_night_{subtask_id}")
        model.Add(remainder == 1).OnlyEnforceIf(is_night)
        model.Add(ist_shift_cap[subtask_id] == res_info["night_cap"]).OnlyEnforceIf(is_res, is_night)

    # 子任务产量 ≤ 班产能（仅启用时生效）
    model.Add(ist_qty[subtask_id] <= ist_shift_cap[subtask_id]).OnlyEnforceIf(ist_enabled[subtask_id])

# 5.1.3 注塑主任务总需求约束（子任务产量之和 ≥ 总需求）
for task_id, task in tasks.items():
    if task["type"] != "injection_main":
        continue
    # 汇总关联子任务的产量
    subtask_qtys = [ist_qty[sid] for sid in task["subtask_ids"]]
    total_sub_qty = model.NewIntVar(0, task["total_qty"] * 2, f"total_sub_qty_{task_id}")
    model.Add(total_sub_qty == sum(subtask_qtys))
    # 总产量 ≥ 主任务需求（核心工业约束，必须满足）
    model.Add(total_sub_qty >= task["total_qty"])

# 5.2 机加任务约束（修复AddMultiplicationEquality参数）
for task_id, task in tasks.items():
    if task["type"] != "machining":
        continue
    total_cap = model.NewIntVar(1, 10000, f"total_cap_{task_id}")
    # 班产能约束（模运算判断白班/夜班）
    cap_white = machining_cap["white"]
    cap_night = machining_cap["night"]
    remainder = model.NewIntVar(0, 1, f"remainder_{task_id}")
    model.AddModuloEquality(remainder, t_start[task_id], 2)

    is_white = model.NewBoolVar(f"is_white_{task_id}")
    model.Add(remainder == 0).OnlyEnforceIf(is_white)
    # 修复点：单独赋值班产能变量，不再用海象运算符
    model.Add(t_shift_cap[task_id] == cap_white).OnlyEnforceIf(is_white)

    is_night = model.NewBoolVar(f"is_night_{task_id}")
    model.Add(remainder == 1).OnlyEnforceIf(is_night)
    model.Add(t_shift_cap[task_id] == cap_night).OnlyEnforceIf(is_night)

    # 修复点：参数为合法的IntVar变量，无作用域问题
    model.AddMultiplicationEquality(total_cap, t_shift_cap[task_id], t_prod_shifts[task_id])
    model.Add(t_qty[task_id] <= total_cap)

# 5.3 组装任务约束（允许超期核心修改：移除硬约束）
for task_id, task in tasks.items():
    if task["type"] != "assembly":
        continue
    # 班产能约束
    total_cap = model.NewIntVar(1, 10000, f"total_cap_{task_id}")
    cap_white = assembly_cap["white"]
    cap_night = assembly_cap["night"]
    remainder = model.NewIntVar(0, 1, f"remainder_{task_id}")
    model.AddModuloEquality(remainder, t_start[task_id], 2)

    is_white = model.NewBoolVar(f"is_white_{task_id}")
    model.Add(remainder == 0).OnlyEnforceIf(is_white)
    # 修复点：单独赋值班产能变量
    model.Add(t_shift_cap[task_id] == cap_white).OnlyEnforceIf(is_white)

    is_night = model.NewBoolVar(f"is_night_{task_id}")
    model.Add(remainder == 1).OnlyEnforceIf(is_night)
    model.Add(t_shift_cap[task_id] == cap_night).OnlyEnforceIf(is_night)

    # 修复点：AddMultiplicationEquality参数正确
    model.AddMultiplicationEquality(total_cap, t_shift_cap[task_id], t_prod_shifts[task_id])
    model.Add(t_qty[task_id] <= total_cap)

    # 允许超期核心修改：删除硬约束「t_end <= due_shift」
    # 仅保留延期计算，不限制结束时间
    model.AddMaxEquality(order_delay[task["order_id"]], [0, t_end[task_id] - task["due_shift"]])

# 5.4 上下级任务依赖（倒排核心，保留但放宽时间上限）
# 建立物料→任务ID映射
semi_to_task = {task["semi_id"]: task_id for task_id, task in tasks.items()}
for parent_semi, children in bom_structure.items():
    for child_semi, (ratio, lead_shift) in children.items():
        # 找到父/子任务ID
        parent_task_id = semi_to_task.get(parent_semi)
        child_task_id = semi_to_task.get(child_semi)
        if not parent_task_id or not child_task_id:
            continue

        # 父任务=机加/组装：直接关联时间约束
        if tasks[parent_task_id]["type"] in ["machining", "assembly"]:
            # 子任务=注塑主任务：关联所有子任务的结束时间 ≤ 父任务开始 - 提前班次
            if tasks[child_task_id]["type"] == "injection_main":
                for subtask_id in tasks[child_task_id]["subtask_ids"]:
                    model.Add(ist_end[subtask_id] <= t_start[parent_task_id] - lead_shift)
            # 子任务=机加：直接关联时间约束
            else:
                model.Add(t_end[child_task_id] <= t_start[parent_task_id] - lead_shift)
                model.Add(t_inventory[child_task_id] == t_start[parent_task_id] - t_end[child_task_id])

        # 产能配比约束
        if tasks[parent_task_id]["type"] in ["machining", "assembly"] and tasks[child_task_id][
            "type"] != "injection_main":
            model.Add(t_qty[child_task_id] >= t_qty[parent_task_id] * ratio)

# ===================== 6. 优化目标（允许超期核心：提高超期惩罚权重） =====================
# 目标1：最小化注塑子任务数量（减少资源占用）
total_ist_enabled = model.NewIntVar(0, MAX_INJECTION_SUBTASKS, "total_ist_enabled")
ist_enabled_list = [ist_enabled[sid] for sid in injection_subtasks.keys()]
model.Add(total_ist_enabled == sum(ist_enabled_list))

# 目标2：最小化库存持有班次
total_inventory = model.NewIntVar(0, (MAX_SHIFT + 20) * len(tasks), "total_inventory")
inventory_list = [t_inventory[tid] for tid in tasks.keys() if tasks[tid]["type"] != "injection_main"]
model.Add(total_inventory == sum(inventory_list))

# 目标3：最小化订单超期（大幅提高权重，优先减少超期）
total_delay = model.NewIntVar(0, (MAX_SHIFT + 20) * len(orders), "total_delay")
delay_list = [order_delay[oid] for oid in orders.keys()]
model.Add(total_delay == sum(delay_list))

# 多目标加权（优先级：最少超期 > 最少子任务 > 最少库存）
model.Minimize(OVERDUE_WEIGHT * total_delay + 5 * total_ist_enabled + 3 * total_inventory)

# ===================== 7. 求解器配置（确保返回可行解） =====================
solver = cp_model.CpSolver()
solver.parameters.max_time_in_seconds = 180.0  # 延长超时时间
solver.parameters.num_search_workers = 8
solver.parameters.search_branching = cp_model.PORTFOLIO_SEARCH
solver.parameters.optimize_with_core = False  # 禁用核心优化，优先找可行解
solver.parameters.enumerate_all_solutions = False  # 不枚举所有解，快速返回可行解

# 求解
status = solver.Solve(model)


# ===================== 8. 结果输出 =====================
def shift_to_human(shift_id):
    """班次ID转人类可读格式"""
    day = shift_id // 2 + 1
    shift_type = "白班" if shift_id % 2 == 0 else "夜班"
    return f"第{day}天{shift_type}"


# 输出结果
if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
    print("=" * 80)
    print("✅ 排产求解成功！状态：", solver.StatusName(status))
    print("=" * 80)

    # 1. 注塑子任务结果（仅显示启用的）
    print("\n🔧 注塑子任务排产结果（动态拆分）：")
    print("-" * 80)
    header = f"{'子任务ID':<12} {'半成品':<8} {'启用':<6} {'资源':<15} {'开始班次':<12} {'结束班次':<12} {'产量':<8}"
    print(header)
    print("-" * 80)
    for subtask_id, subtask in injection_subtasks.items():
        enabled = solver.Value(ist_enabled[subtask_id])
        if enabled == 0:
            continue  # 仅显示启用的子任务
        start = solver.Value(ist_start[subtask_id])
        end = solver.Value(ist_end[subtask_id])
        qty = solver.Value(ist_qty[subtask_id])
        res_idx = solver.Value(ist_resource[subtask_id])
        res_id = subtask["available_res"][res_idx]
        res_detail = injection_resources[res_id]
        res_str = f"{res_detail['machine']}+{res_detail['mold']}"

        print(
            f"{subtask_id:<12} {subtask['semi_id']:<8} {enabled:<6} {res_str:<15} {shift_to_human(start):<12} {shift_to_human(end):<12} {qty:<8}")

    # 2. 机加/组装任务结果
    print("\n🏭 机加/组装任务排产结果：")
    print("-" * 80)
    header = f"{'任务ID':<8} {'物料':<8} {'类型':<10} {'产量':<8} {'开始班次':<12} {'结束班次':<12} {'库存班次':<10}"
    print(header)
    print("-" * 80)
    for task_id, task in tasks.items():
        if task["type"] == "injection_main":
            continue
        start = solver.Value(t_start[task_id])
        end = solver.Value(t_end[task_id])
        qty = solver.Value(t_qty[task_id])
        inventory = solver.Value(t_inventory[task_id]) if task["type"] != "assembly" else 0

        print(
            f"{task_id:<8} {task['semi_id']:<8} {task['type']:<10} {qty:<8} {shift_to_human(start):<12} {shift_to_human(end):<12} {inventory:<10}")

    # 3. 订单结果（突出显示超期）
    print("\n📄 订单排产结果（允许超期）：")
    print("-" * 80)
    header = f"{'订单ID':<8} {'交货期班次':<12} {'组装结束班次':<12} {'超期班次':<8} {'超期状态':<10}"
    print(header)
    print("-" * 80)
    for order_id, order in orders.items():
        # 找到订单对应的组装任务
        assembly_task_id = \
        [tid for tid, task in tasks.items() if task["type"] == "assembly" and task["order_id"] == order_id][0]
        due_shift = order["due_shift"]
        end_shift = solver.Value(t_end[assembly_task_id])
        delay = solver.Value(order_delay[order_id])
        delay_status = "✅ 未超期" if delay == 0 else f"❌ 超期{delay}班"

        print(
            f"{order_id:<8} {shift_to_human(due_shift):<12} {shift_to_human(end_shift):<12} {delay:<8} {delay_status:<10}")

    # 4. 核心指标
    print("\n📊 核心优化指标：")
    print(f"启用的注塑子任务数量：{solver.Value(total_ist_enabled)}")
    print(f"总库存持有班次：{solver.Value(total_inventory)}")
    print(f"总订单超期班次：{solver.Value(total_delay)}")
else:
    # 兜底：即使求解器返回其他状态，也尝试提取可行解（极少出现）
    print("⚠️  求解器未返回最优/可行解，但尝试提取结果：")
    print("状态：", solver.StatusName(status))
    # 可添加降级逻辑，比如输出部分计算结果
    pass