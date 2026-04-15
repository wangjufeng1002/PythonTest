import random
import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from deap import base, creator, tools, algorithms
from dataclasses import dataclass
from typing import List, Dict


# -------------------------- 1. 定义数据结构（任务和资源）--------------------------
@dataclass
class Task:
    task_id: str  # 任务ID
    duration: float  # 持续时间（小时）
    priority: int = 1  # 优先级（1-5，仅用于后续扩展，本示例暂不生效）


@dataclass
class Resource:
    resource_id: str  # 资源ID
    available_time: datetime.datetime = datetime.datetime.now()  # 资源下次可用时间


# -------------------------- 2. 初始化排产数据 --------------------------
# 任务列表（5个任务，持续时间1-6小时）
tasks = [
    Task("T1", 4, priority=3),
    Task("T2", 2, priority=5),
    Task("T3", 6, priority=2),
    Task("T4", 3, priority=4),
    Task("T5", 5, priority=1)
]

# 资源列表（2台设备）
resources = [
    Resource("R1"),
    Resource("R2")
]

# 任务索引映射（DEAP中用索引表示任务，方便遗传操作）
task_indices = list(range(len(tasks)))  # [0,1,2,3,4] 对应 T1-T5


# -------------------------- 3. DEAP 算法配置 --------------------------
# 3.1 定义适应度函数（多目标：最小化总工期 + 最小化资源负载方差）
def evaluate(individual: List[int]) -> tuple:
    """
    适应度函数：计算排产方案的两个目标值
    :param individual: 染色体（任务执行顺序，如 [1,3,0,2,4] 表示 T2→T4→T1→T3→T5）
    :return: (总工期, 资源负载方差) → 越小越优
    """
    # 重置资源可用时间（每次评估都重新初始化）
    resource_available = {res.resource_id: datetime.datetime.now() for res in resources}
    task_end_times = {}  # 记录每个任务的结束时间

    # 按染色体的任务顺序分配资源
    for idx in individual:
        task = tasks[idx]
        # 选择当前最早可用的资源（贪心分配资源）
        best_res = min(resources, key=lambda r: resource_available[r.resource_id])
        # 任务开始时间 = 资源可用时间（不早于当前时间）
        start_time = max(resource_available[best_res.resource_id], datetime.datetime.now())
        # 任务结束时间 = 开始时间 + 持续时间
        end_time = start_time + datetime.timedelta(hours=task.duration)
        # 更新记录
        task_end_times[task.task_id] = end_time
        resource_available[best_res.resource_id] = end_time

    # 目标1：计算总工期（最后完成任务的结束时间 - 项目开始时间）
    project_start = datetime.datetime.now()
    project_end = max(task_end_times.values())
    total_duration = (project_end - project_start).total_seconds() / 3600  # 转为小时

    # 目标2：计算资源负载方差（资源工作总时间的差异，越小越均衡）
    resource_work_time = []
    for res in resources:
        work_time = (resource_available[res.resource_id] - project_start).total_seconds() / 3600
        resource_work_time.append(work_time)
    load_variance = np.var(resource_work_time)  # 方差

    return (total_duration, load_variance)


# 3.2 创建DEAP问题框架（多目标最小化）
# 定义适应度类：weights=(-1.0, -1.0) 表示两个目标均最小化
creator.create("FitnessMin", base.Fitness, weights=(-1.0, -1.0))
# 定义个体类：基于列表（染色体），关联适应度
creator.create("Individual", list, fitness=creator.FitnessMin)

# 3.3 初始化工具集（遗传操作配置）
toolbox = base.Toolbox()

# 染色体生成：任务索引的随机排列（每个任务仅出现一次）
toolbox.register("indices", random.sample, task_indices, len(task_indices))
# 个体生成：用任务索引初始化个体
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)
# 种群生成：批量生成个体（种群大小可调整）
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# 遗传操作：交叉、变异、选择
toolbox.register("mate", tools.cxTwoPoint)  # 两点交叉（任务顺序交换）
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)  # 随机打乱变异（概率5%）
toolbox.register("select", tools.selNSGA2)  # 非支配排序选择（多目标优化核心）
toolbox.register("evaluate", evaluate)  # 绑定适应度函数


# -------------------------- 4. 运行遗传算法 --------------------------
def run_ga_scheduler(
        pop_size: int = 50,  # 种群大小（默认50，越大搜索范围越广但耗时越长）
        n_generations: int = 100  # 迭代次数（默认100，越多越可能找到最优解）
) -> tuple:
    """运行DEAP遗传算法，返回最优排产方案和种群"""
    # 初始化种群
    population = toolbox.population(n=pop_size)

    # 运行遗传算法（eaMuPlusLambda：父代+子代共同进化）
    algorithms.eaMuPlusLambda(
        population, toolbox,
        mu=pop_size,  # 父代种群大小
        lambda_=pop_size * 2,  # 子代种群大小（每次生成2倍父代的子代）
        cxpb=0.7,  # 交叉概率（70%）
        mutpb=0.2,  # 变异概率（20%）
        ngen=n_generations,  # 迭代次数
        verbose=True,  # 打印迭代日志
        halloffame=tools.HallOfFame(1)  # 保存最优个体
    )

    # 获取最优个体（多目标帕累托前沿的最优解）
    best_individual = tools.selBest(population, 1)[0]
    return best_individual, population


# -------------------------- 5. 解析最优解为排产结果 --------------------------
def parse_schedule(best_individual: List[int]) -> List[Dict]:
    """将最优个体（任务顺序）解析为结构化排产结果"""
    resource_available = {res.resource_id: datetime.datetime.now() for res in resources}
    schedule_results = []

    for idx in best_individual:
        task = tasks[idx]
        # 分配最早可用资源
        best_res = min(resources, key=lambda r: resource_available[r.resource_id])
        start_time = max(resource_available[best_res.resource_id], datetime.datetime.now())
        end_time = start_time + datetime.timedelta(hours=task.duration)

        # 记录结果
        schedule_results.append({
            "task_id": task.task_id,
            "resource_id": best_res.resource_id,
            "start_time": start_time,
            "end_time": end_time,
            "duration": task.duration
        })

        # 更新资源可用时间
        resource_available[best_res.resource_id] = end_time

    return schedule_results


# -------------------------- 6. 可视化排产结果（甘特图）--------------------------
def plot_gantt(schedule_results: List[Dict]):
    """用甘特图可视化排产结果"""
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 支持中文
    fig, ax = plt.subplots(figsize=(12, 6))

    # 资源颜色映射
    resource_colors = {"R1": "#3498db", "R2": "#e74c3c"}
    y_pos = {"R1": 0.5, "R2": 1.5}  # 资源在y轴的位置

    # 绘制甘特图
    for res in schedule_results:
        task_id = res["task_id"]
        resource_id = res["resource_id"]
        start = res["start_time"]
        end = res["end_time"]
        duration = res["duration"]

        # 绘制任务条
        ax.barh(
            y=y_pos[resource_id],
            width=(end - start).total_seconds() / 3600,
            left=mdates.date2num(start),
            height=0.6,
            color=resource_colors[resource_id],
            alpha=0.8,
            label=resource_id if task_id == schedule_results[0]["task_id"] else ""
        )

        # 添加任务标签
        ax.text(
            mdates.date2num(start) + duration / 2,
            y_pos[resource_id],
            task_id,
            ha="center", va="center",
            fontsize=10, fontweight="bold"
        )

    # 图表配置
    ax.set_yticks([y_pos[res] for res in resource_colors.keys()])
    ax.set_yticklabels(resource_colors.keys(), fontsize=12)
    ax.set_xlabel("时间", fontsize=12)
    ax.set_ylabel("资源", fontsize=12)
    ax.set_title("DEAP 遗传算法排产结果（甘特图）", fontsize=14, fontweight="bold")

    # 格式化x轴时间
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M"))
    plt.xticks(rotation=45)

    # 添加网格和图例
    ax.grid(axis="x", alpha=0.3)
    ax.legend(loc="upper right")

    plt.tight_layout()
    plt.show()


# -------------------------- 7. 主流程运行 --------------------------
if __name__ == "__main__":
    # 1. 运行DEAP遗传算法
    best_ind, population = run_ga_scheduler(pop_size=50, n_generations=100)

    # 2. 解析最优排产结果
    schedule = parse_schedule(best_ind)

    # 3. 打印结果
    print("\n" + "-" * 80)
    print("DEAP 最优排产结果：")
    print("-" * 80)
    print(f"{'任务ID':<8} {'资源ID':<8} {'开始时间':<25} {'结束时间':<25} {'持续时间（小时）'}")
    print("-" * 80)
    for res in schedule:
        start_str = res["start_time"].strftime("%Y-%m-%d %H:%M:%S")
        end_str = res["end_time"].strftime("%Y-%m-%d %H:%M:%S")
        print(f"{res['task_id']:<8} {res['resource_id']:<8} {start_str:<25} {end_str:<25} {res['duration']}")

    # 4. 计算并打印优化目标值
    total_duration, load_variance = evaluate(best_ind)
    print("\n优化目标达成情况：")
    print(f"总工期：{total_duration:.2f} 小时")
    print(f"资源负载方差：{load_variance:.4f}（越小越均衡）")

    # 5. 可视化甘特图
    plot_gantt(schedule)
