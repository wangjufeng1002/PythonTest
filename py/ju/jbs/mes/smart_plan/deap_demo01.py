from deap import base, creator, tools, algorithms
from datetime import datetime, timedelta
import random
import numpy as np
from enum import Enum
from collections import defaultdict
import heapq


class TaskType(Enum):
    INJECTION = "injection"  # 注塑任务
    ASSEMBLY = "assembly"  # 组装任务


class MaterialFlow:
    """物料流管理：跟踪注塑零件到组装任务的物料供应"""

    def __init__(self):
        self.injection_to_assembly = defaultdict(list)  # 注塑->组装映射
        self.assembly_requirements = defaultdict(dict)  # 组装任务需求

    def add_dependency(self, injection_task_id, assembly_task_id,
                       required_quantity, initial_batch=0):
        """添加注塑-组装依赖关系"""
        self.injection_to_assembly[injection_task_id].append({
            'assembly_id': assembly_task_id,
            'required_quantity': required_quantity,
            'initial_batch': initial_batch,  # 开始组装所需的最小批量
            'supplied_quantity': 0  # 已供应的数量
        })

        # 记录组装任务的需求
        if assembly_task_id not in self.assembly_requirements:
            self.assembly_requirements[assembly_task_id] = {}
        self.assembly_requirements[assembly_task_id][injection_task_id] = {
            'required': required_quantity,
            'initial_batch': initial_batch,
            'supplied': 0
        }

    def can_start_assembly(self, assembly_task_id, completed_injections):
        """检查组装任务是否可以开始"""
        if assembly_task_id not in self.assembly_requirements:
            return True  # 没有依赖

        requirements = self.assembly_requirements[assembly_task_id]

        for injection_id, req_info in requirements.items():
            # 检查是否满足初始批量要求
            completed_qty = completed_injections.get(injection_id, {}).get('completed_quantity', 0)
            if completed_qty < req_info['initial_batch']:
                return False
        return True

    def update_supply(self, injection_task_id, produced_quantity, current_time):
        """更新物料供应"""
        if injection_task_id in self.injection_to_assembly:
            for dep in self.injection_to_assembly[injection_task_id]:
                assembly_id = dep['assembly_id']
                # 更新供应量
                dep['supplied_quantity'] = min(produced_quantity, dep['required_quantity'])
                self.assembly_requirements[assembly_id][injection_task_id]['supplied'] = dep['supplied_quantity']


class Mold:
    """模具资源"""

    def __init__(self, mold_id, compatible_machines, setup_time=30,
                 max_lifetime=1000000, current_usage=0):
        self.mold_id = mold_id
        self.compatible_machines = compatible_machines  # 可用的注塑机列表
        self.setup_time = setup_time  # 换模时间（分钟）
        self.max_lifetime = max_lifetime  # 模具寿命（生产次数）
        self.current_usage = current_usage
        self.scheduled_tasks = []  # 已排产的任务
        self.availability_slots = []  # 可用时间段

    def is_available(self, start_time, duration):
        """检查模具在指定时段是否可用"""
        # 检查是否超出寿命
        if self.current_usage >= self.max_lifetime:
            return False

        # 检查时间冲突
        end_time = start_time + duration
        for scheduled_start, scheduled_end in self.scheduled_tasks:
            if not (end_time <= scheduled_start or start_time >= scheduled_end):
                return False

        # 检查可用时间段
        if self.availability_slots:
            for avail_start, avail_end in self.availability_slots:
                if start_time >= avail_start and end_time <= avail_end:
                    return True
            return False

        return True

    def add_maintenance(self, start_time, duration):
        """添加维护时段"""
        self.availability_slots = self._subtract_slot(
            self.availability_slots, (start_time, start_time + duration)
        )

    def _subtract_slot(self, slots, remove_slot):
        """从可用时间段中移除指定时段"""
        result = []
        r_start, r_end = remove_slot

        for s_start, s_end in slots:
            if s_end <= r_start or s_start >= r_end:
                # 没有重叠
                result.append((s_start, s_end))
            else:
                # 有重叠，分割时间段
                if s_start < r_start:
                    result.append((s_start, r_start))
                if s_end > r_end:
                    result.append((r_end, s_end))

        return result


class InjectionMachine:
    """注塑机资源"""

    def __init__(self, machine_id, capacity, efficiency=1.0,
                 energy_consumption=1.0, shift_schedule=None):
        self.machine_id = machine_id
        self.capacity = capacity  # 产能（单位/小时）
        self.efficiency = efficiency
        self.energy_consumption = energy_consumption
        self.shift_schedule = shift_schedule or self._default_shift()
        self.scheduled_tasks = []  # (start_time, end_time, task_id, mold_id)
        self.maintenance_slots = []

    def _default_shift(self):
        """默认班次安排"""
        return {
            'day': {'start': 8 * 60, 'end': 20 * 60},  # 白班
            'night': {'start': 20 * 60, 'end': 8 * 60}  # 夜班（跨天）
        }

    def can_use_mold(self, mold_id, molds_dict):
        """检查是否可以安装指定模具"""
        mold = molds_dict.get(mold_id)
        if mold and self.machine_id in mold.compatible_machines:
            return True
        return False

    def is_available(self, start_time, duration, mold_id=None, molds_dict=None):
        """检查注塑机在指定时段是否可用"""
        # 检查维护时段
        end_time = start_time + duration
        for maint_start, maint_end in self.maintenance_slots:
            if not (end_time <= maint_start or start_time >= maint_end):
                return False

        # 检查模具兼容性
        if mold_id and molds_dict:
            if not self.can_use_mold(mold_id, molds_dict):
                return False

        # 检查时间冲突
        for scheduled in self.scheduled_tasks:
            s_start, s_end, _, _ = scheduled
            if not (end_time <= s_start or start_time >= s_end):
                return False

        # 检查班次时间
        if not self._check_shift_time(start_time, end_time):
            return False

        return True

    def _check_shift_time(self, start_time, end_time):
        """检查是否在班次时间内"""
        day_in_minutes = 24 * 60

        # 将时间映射到当天
        start_offset = start_time % day_in_minutes
        end_offset = end_time % day_in_minutes

        day_shift = self.shift_schedule['day']
        night_shift = self.shift_schedule['night']

        # 检查白班
        if day_shift['start'] <= day_shift['end']:
            if start_offset >= day_shift['start'] and end_offset <= day_shift['end']:
                return True
        else:  # 跨天白班
            if start_offset >= day_shift['start'] or end_offset <= day_shift['end']:
                return True

        # 检查夜班
        if night_shift['start'] <= night_shift['end']:
            if start_offset >= night_shift['start'] and end_offset <= night_shift['end']:
                return True
        else:  # 跨天夜班
            if start_offset >= night_shift['start'] or end_offset <= night_shift['end']:
                return True

        return False

    def schedule_task(self, start_time, duration, task_id, mold_id):
        """安排任务到注塑机"""
        self.scheduled_tasks.append((start_time, start_time + duration, task_id, mold_id))
        self.scheduled_tasks.sort()  # 按开始时间排序


class AssemblyLine:
    """组装线资源"""

    def __init__(self, line_id, capacity, workers=1, efficiency=1.0):
        self.line_id = line_id
        self.capacity = capacity  # 组装能力（单位/小时）
        self.workers = workers
        self.efficiency = efficiency
        self.scheduled_tasks = []  # (start_time, end_time, task_id)
        self.inventory = defaultdict(int)  # 零件库存

    def add_inventory(self, part_type, quantity):
        """添加零件到库存"""
        self.inventory[part_type] += quantity

    def consume_inventory(self, part_type, quantity):
        """从库存消耗零件"""
        if self.inventory[part_type] >= quantity:
            self.inventory[part_type] -= quantity
            return True
        return False

    def is_available(self, start_time, duration):
        """检查组装线在指定时段是否可用"""
        end_time = start_time + duration

        for s_start, s_end, _ in self.scheduled_tasks:
            if not (end_time <= s_start or start_time >= s_end):
                return False

        return True

    def schedule_task(self, start_time, duration, task_id):
        """安排任务到组装线"""
        self.scheduled_tasks.append((start_time, start_time + duration, task_id))
        self.scheduled_tasks.sort()


class ProductionTask:
    """生产任务基类"""

    def __init__(self, task_id, task_type, product_id, quantity,
                 priority=1, due_date=None, release_date=None):
        self.task_id = task_id
        self.task_type = task_type
        self.product_id = product_id
        self.quantity = quantity
        self.priority = priority
        self.due_date = due_date
        self.release_date = release_date
        self.predecessors = []  # 前驱任务
        self.successors = []  # 后继任务
        self.scheduled_start = None
        self.scheduled_end = None
        self.completed_quantity = 0

    def add_dependency(self, predecessor_task):
        """添加任务依赖"""
        self.predecessors.append(predecessor_task)
        predecessor_task.successors.append(self)


class InjectionTask(ProductionTask):
    """注塑任务"""

    def __init__(self, task_id, product_id, quantity, mold_id,
                 cycle_time, machines_required=1, **kwargs):
        super().__init__(task_id, TaskType.INJECTION, product_id, quantity, **kwargs)
        self.mold_id = mold_id
        self.cycle_time = cycle_time  # 单次循环时间（分钟）
        self.machines_required = machines_required  # 并行生产的机器数量
        self.unit_per_cycle = 1  # 每次循环生产的产品数量
        self.setup_time = 30  # 换模/准备时间（分钟）

    def calculate_duration(self):
        """计算任务所需总时间"""
        cycles_needed = self.quantity / self.unit_per_cycle
        production_time = cycles_needed * self.cycle_time
        return production_time + self.setup_time

    def get_required_machines(self, available_machines):
        """获取可用的注塑机列表"""
        compatible_machines = []
        for machine in available_machines:
            if machine.can_use_mold(self.mold_id, {}):  # 需要传入molds_dict
                compatible_machines.append(machine.machine_id)
        return compatible_machines


class AssemblyTask(ProductionTask):
    """组装任务"""

    def __init__(self, task_id, product_id, quantity, assembly_line_id,
                 assembly_time_per_unit, parts_required, **kwargs):
        super().__init__(task_id, TaskType.ASSEMBLY, product_id, quantity, **kwargs)
        self.assembly_line_id = assembly_line_id
        self.assembly_time_per_unit = assembly_time_per_unit  # 单位组装时间（分钟）
        self.parts_required = parts_required  # {part_type: quantity}
        self.initial_batch_requirements = {}  # 开始组装所需的最小批量

    def calculate_duration(self):
        """计算组装任务所需时间"""
        return self.quantity * self.assembly_time_per_unit

    def set_initial_batch(self, part_type, min_quantity):
        """设置开始组装所需的最小批量"""
        self.initial_batch_requirements[part_type] = min_quantity


class DependencyAwareEncoder:
    """考虑依赖关系的编码器"""

    @staticmethod
    def encode(tasks, material_flow):
        """编码排产方案

        采用三层编码：
        1. 任务优先级序列（考虑依赖关系的拓扑排序）
        2. 资源分配（注塑机/组装线）
        3. 开始时间偏移（相对于依赖约束的最早开始时间）
        """
        # 分离注塑任务和组装任务
        injection_tasks = [t for t in tasks if t.task_type == TaskType.INJECTION]
        assembly_tasks = [t for t in tasks if t.task_type == TaskType.ASSEMBLY]

        # 第一部分：任务序列（拓扑排序保证依赖关系）
        task_sequence = DependencyAwareEncoder._topological_sort(tasks, material_flow)

        # 第二部分：资源分配
        resource_assignment = []
        for task in task_sequence:
            if task.task_type == TaskType.INJECTION:
                # 为注塑任务随机分配注塑机（从兼容机器中）
                # 这里简化处理，实际需要根据模具兼容性
                resource_assignment.append(random.choice([0, 1, 2]))  # 机器ID
            else:
                # 组装任务分配到组装线
                resource_assignment.append(random.choice([0, 1]))  # 组装线ID

        # 第三部分：时间偏移（考虑到依赖关系）
        time_offsets = []
        for task in task_sequence:
            # 根据任务类型设置不同的时间偏移范围
            if task.task_type == TaskType.INJECTION:
                # 注塑任务：0-480分钟偏移
                time_offsets.append(random.randint(0, 480))
            else:
                # 组装任务：0-240分钟偏移（更小的灵活性）
                time_offsets.append(random.randint(0, 240))

        # 组合染色体
        chromosome = {
            'task_sequence': [t.task_id for t in task_sequence],
            'resource_assignment': resource_assignment,
            'time_offsets': time_offsets,
            'batch_overlap': random.random()  # 批次重叠度参数
        }

        return chromosome

    @staticmethod
    def _topological_sort(tasks, material_flow):
        """拓扑排序，考虑物料依赖关系"""
        # 构建任务依赖图
        task_map = {t.task_id: t for t in tasks}
        in_degree = {t.task_id: len(t.predecessors) for t in tasks}

        # 添加物料依赖
        for injection_id, dependencies in material_flow.injection_to_assembly.items():
            for dep in dependencies:
                assembly_id = dep['assembly_id']
                if injection_id in task_map and assembly_id in task_map:
                    # 确保注塑任务在组装任务之前
                    if task_map[injection_id] not in task_map[assembly_id].predecessors:
                        task_map[assembly_id].predecessors.append(task_map[injection_id])
                        in_degree[assembly_id] += 1

        # 拓扑排序
        result = []
        zero_degree = [task_id for task_id, deg in in_degree.items() if deg == 0]
        heapq.heapify(zero_degree)

        while zero_degree:
            task_id = heapq.heappop(zero_degree)
            task = task_map[task_id]
            result.append(task)

            for successor in task.successors:
                in_degree[successor.task_id] -= 1
                if in_degree[successor.task_id] == 0:
                    heapq.heappush(zero_degree, successor.task_id)

        # 检查是否有环
        if len(result) != len(tasks):
            # 存在环，随机排序
            result = random.sample(tasks, len(tasks))

        return result


class ResourceAwareDecoder:
    """资源感知的解码器"""

    def __init__(self, injection_machines, assembly_lines, molds, material_flow):
        self.injection_machines = {m.machine_id: m for m in injection_machines}
        self.assembly_lines = {l.line_id: l for l in assembly_lines}
        self.molds = {m.mold_id: m for m in molds}
        self.material_flow = material_flow
        self.task_map = {}

    def decode(self, chromosome, tasks):
        """解码染色体为排产计划"""
        # 创建任务映射
        self.task_map = {t.task_id: t for t in tasks}

        # 提取染色体信息
        task_sequence_ids = chromosome['task_sequence']
        resource_assignments = chromosome['resource_assignment']
        time_offsets = chromosome['time_offsets']
        batch_overlap = chromosome['batch_overlap']

        # 按顺序安排任务
        schedule = {
            'tasks': {},
            'machine_utilization': defaultdict(list),
            'line_utilization': defaultdict(list),
            'completion_status': {}
        }

        # 跟踪每个任务的完成数量
        completed_injections = {}

        for idx, task_id in enumerate(task_sequence_ids):
            task = self.task_map[task_id]
            resource_id = resource_assignments[idx]
            time_offset = time_offsets[idx]

            # 计算最早开始时间
            earliest_start = self._calculate_earliest_start(task, schedule)

            # 考虑批次重叠
            if task.task_type == TaskType.INJECTION:
                # 注塑任务可以提前开始
                actual_start = earliest_start + time_offset
                # 安排到注塑机
                scheduled_info = self._schedule_injection(
                    task, resource_id, actual_start, batch_overlap
                )
            else:
                # 组装任务：检查物料依赖
                if self.material_flow.can_start_assembly(task_id, completed_injections):
                    actual_start = earliest_start + min(time_offset, 240)  # 限制最大偏移
                    scheduled_info = self._schedule_assembly(
                        task, resource_id, actual_start
                    )
                else:
                    # 延迟到物料满足
                    actual_start = self._find_next_available_time_for_assembly(
                        task, resource_id, completed_injections
                    )
                    scheduled_info = self._schedule_assembly(task, resource_id, actual_start)

            # 更新计划
            schedule['tasks'][task_id] = scheduled_info
            if task.task_type == TaskType.INJECTION:
                # 更新完成数量
                completed_injections[task_id] = {
                    'completed_quantity': task.quantity,
                    'completion_time': scheduled_info['end_time']
                }
                # 更新物料流
                self.material_flow.update_supply(
                    task_id, task.quantity, scheduled_info['end_time']
                )

        return schedule

    def _calculate_earliest_start(self, task, schedule):
        """计算任务的最早开始时间（考虑依赖）"""
        earliest_start = task.release_date or 0

        for predecessor in task.predecessors:
            if predecessor.task_id in schedule['tasks']:
                pred_end = schedule['tasks'][predecessor.task_id]['end_time']
                earliest_start = max(earliest_start, pred_end)

        # 对于组装任务，还需要考虑物料依赖
        if task.task_type == TaskType.ASSEMBLY:
            requirements = self.material_flow.assembly_requirements.get(task.task_id, {})
            for injection_id, req_info in requirements.items():
                if injection_id in schedule['tasks']:
                    # 计算生产初始批量所需的时间
                    injection_task = self.task_map[injection_id]
                    initial_batch_time = self._calculate_batch_time(
                        injection_task, req_info['initial_batch']
                    )
                    earliest_start = max(
                        earliest_start,
                        schedule['tasks'][injection_id]['start_time'] + initial_batch_time
                    )

        return earliest_start

    def _calculate_batch_time(self, injection_task, batch_size):
        """计算生产指定批量所需的时间"""
        cycles_needed = batch_size / injection_task.unit_per_cycle
        return cycles_needed * injection_task.cycle_time + injection_task.setup_time

    def _schedule_injection(self, task, machine_id, proposed_start, batch_overlap):
        """安排注塑任务"""
        machine = self.injection_machines.get(machine_id)
        if not machine:
            # 使用第一个可用的机器
            machine = next(iter(self.injection_machines.values()))

        mold = self.molds.get(task.mold_id)

        # 计算任务持续时间
        duration = task.calculate_duration()

        # 考虑批次重叠，可以提前开始
        adjusted_start = max(0, proposed_start - int(duration * batch_overlap * 0.3))

        # 找到实际可用时间
        actual_start = self._find_available_slot(
            machine, mold, adjusted_start, duration
        )

        # 安排任务
        if machine.is_available(actual_start, duration, task.mold_id, self.molds):
            machine.schedule_task(actual_start, duration, task.task_id, task.mold_id)
            if mold:
                mold.scheduled_tasks.append((actual_start, actual_start + duration))

            return {
                'task_id': task.task_id,
                'task_type': 'injection',
                'machine_id': machine.machine_id,
                'mold_id': task.mold_id,
                'start_time': actual_start,
                'end_time': actual_start + duration,
                'quantity': task.quantity
            }

        # 如果不可用，尝试推迟
        return self._reschedule_injection(task, machine, mold, proposed_start, duration)

    def _find_available_slot(self, machine, mold, start_time, duration):
        """找到可用的时间段"""
        current = start_time
        max_search = current + 7 * 24 * 60  # 最多搜索7天

        while current < max_search:
            if (machine.is_available(current, duration, None, self.molds) and
                    (mold is None or mold.is_available(current, duration))):
                return current

            # 向前推进15分钟
            current += 15

        return start_time  # 返回原始时间（简化处理）

    def _reschedule_injection(self, task, machine, mold, start_time, duration):
        """重新安排注塑任务"""
        # 尝试不同的机器
        for alt_machine in self.injection_machines.values():
            if alt_machine.machine_id != machine.machine_id:
                if alt_machine.can_use_mold(task.mold_id, self.molds):
                    actual_start = self._find_available_slot(
                        alt_machine, mold, start_time, duration
                    )

                    if alt_machine.is_available(actual_start, duration, task.mold_id, self.molds):
                        alt_machine.schedule_task(actual_start, duration, task.task_id, task.mold_id)
                        if mold:
                            mold.scheduled_tasks.append((actual_start, actual_start + duration))

                        return {
                            'task_id': task.task_id,
                            'task_type': 'injection',
                            'machine_id': alt_machine.machine_id,
                            'mold_id': task.mold_id,
                            'start_time': actual_start,
                            'end_time': actual_start + duration,
                            'quantity': task.quantity
                        }

        # 所有机器都不可用，延迟到最早可用时间
        actual_start = start_time + 60  # 延迟1小时
        return self._schedule_injection(task, machine.machine_id, actual_start, 0)

    def _schedule_assembly(self, task, line_id, proposed_start):
        """安排组装任务"""
        assembly_line = self.assembly_lines.get(line_id)
        if not assembly_line:
            assembly_line = next(iter(self.assembly_lines.values()))

        duration = task.calculate_duration()

        # 找到实际可用时间
        actual_start = proposed_start
        while not assembly_line.is_available(actual_start, duration):
            actual_start += 15  # 每15分钟检查一次

        # 安排任务
        assembly_line.schedule_task(actual_start, duration, task.task_id)

        # 消耗库存（这里简化处理）
        for part_type, quantity in task.parts_required.items():
            assembly_line.consume_inventory(part_type, quantity)

        return {
            'task_id': task.task_id,
            'task_type': 'assembly',
            'line_id': assembly_line.line_id,
            'start_time': actual_start,
            'end_time': actual_start + duration,
            'quantity': task.quantity
        }

    def _find_next_available_time_for_assembly(self, task, line_id, completed_injections):
        """为组装任务找到下一个可用时间（考虑物料）"""
        assembly_line = self.assembly_lines.get(line_id)
        if not assembly_line:
            assembly_line = next(iter(self.assembly_lines.values()))

        # 计算物料满足的时间
        material_ready_time = 0
        requirements = self.material_flow.assembly_requirements.get(task.task_id, {})

        for injection_id, req_info in requirements.items():
            if injection_id in completed_injections:
                # 已经完成，可以立即开始
                continue

            # 找到相关注塑任务
            injection_task = self.task_map.get(injection_id)
            if injection_task and injection_id in self.task_map:
                # 计算生产初始批量所需的时间
                batch_time = self._calculate_batch_time(injection_task, req_info['initial_batch'])

                # 估计注塑任务的完成时间（这里简化）
                if injection_task.task_id in self.task_map:
                    material_ready_time = max(material_ready_time, batch_time)

        duration = task.calculate_duration()
        start_time = max(material_ready_time, task.release_date or 0)

        # 找到组装线可用的时间
        while not assembly_line.is_available(start_time, duration):
            start_time += 15

        return start_time


class MultiObjectiveFitness:
    """多目标适应度评估"""

    def __init__(self, tasks, injection_machines, assembly_lines,
                 material_flow, due_dates=None):
        self.tasks = tasks
        self.injection_machines = injection_machines
        self.assembly_lines = assembly_lines
        self.material_flow = material_flow
        self.due_dates = due_dates or {}
        self.task_map = {t.task_id: t for t in tasks}

    def evaluate(self, schedule):
        """评估排产方案的多目标适应度"""
        objectives = []

        # 1. 总完工时间（最小化）
        makespan = self._calculate_makespan(schedule)
        objectives.append(makespan)

        # 2. 总延迟惩罚（最小化）
        tardiness_penalty = self._calculate_tardiness(schedule)
        objectives.append(tardiness_penalty)

        # 3. 资源利用率（最大化，用负号表示）
        resource_utilization = self._calculate_resource_utilization(schedule)
        objectives.append(-resource_utilization)

        # 4. 依赖关系满足度（最大化，用负号表示）
        dependency_satisfaction = self._calculate_dependency_satisfaction(schedule)
        objectives.append(-dependency_satisfaction)

        # 5. 库存成本（最小化）
        inventory_cost = self._calculate_inventory_cost(schedule)
        objectives.append(inventory_cost)

        return tuple(objectives)

    def _calculate_makespan(self, schedule):
        """计算总完工时间"""
        end_times = []
        for task_info in schedule['tasks'].values():
            end_times.append(task_info['end_time'])

        return max(end_times) if end_times else 0

    def _calculate_tardiness(self, schedule):
        """计算总延迟惩罚"""
        total_penalty = 0

        for task_info in schedule['tasks'].values():
            task_id = task_info['task_id']
            end_time = task_info['end_time']

            task = self.task_map.get(task_id)
            if task and task.due_date:
                due_time = task.due_date
                if isinstance(due_time, datetime):
                    # 转换为分钟
                    due_minutes = due_time.hour * 60 + due_time.minute
                else:
                    due_minutes = due_time

                if end_time > due_minutes:
                    tardiness = end_time - due_minutes
                    # 考虑任务优先级
                    penalty = tardiness * task.priority
                    total_penalty += penalty

        return total_penalty

    def _calculate_resource_utilization(self, schedule):
        """计算资源利用率"""
        # 注塑机利用率
        injection_utilization = 0
        for machine in self.injection_machines:
            busy_time = 0
            for task_info in schedule['tasks'].values():
                if (task_info['task_type'] == 'injection' and
                        task_info.get('machine_id') == machine.machine_id):
                    duration = task_info['end_time'] - task_info['start_time']
                    busy_time += duration

            # 计算利用率（忙时/总时间）
            if schedule['tasks']:
                total_time = max([t['end_time'] for t in schedule['tasks'].values()])
                if total_time > 0:
                    injection_utilization += busy_time / total_time

        # 组装线利用率
        assembly_utilization = 0
        for line in self.assembly_lines:
            busy_time = 0
            for task_info in schedule['tasks'].values():
                if (task_info['task_type'] == 'assembly' and
                        task_info.get('line_id') == line.line_id):
                    duration = task_info['end_time'] - task_info['start_time']
                    busy_time += duration

            if schedule['tasks']:
                total_time = max([t['end_time'] for t in schedule['tasks'].values()])
                if total_time > 0:
                    assembly_utilization += busy_time / total_time

        # 综合利用率
        total_resources = len(self.injection_machines) + len(self.assembly_lines)
        total_utilization = (injection_utilization + assembly_utilization) / total_resources

        return total_utilization

    def _calculate_dependency_satisfaction(self, schedule):
        """计算依赖关系满足度"""
        satisfaction_score = 0
        max_score = len(self.tasks)  # 每个任务最多得1分

        for task in self.tasks:
            task_info = schedule['tasks'].get(task.task_id)
            if not task_info:
                continue

            # 检查任务依赖
            dependency_satisfied = True
            for pred in task.predecessors:
                pred_info = schedule['tasks'].get(pred.task_id)
                if not pred_info:
                    dependency_satisfied = False
                    break

                if pred_info['end_time'] > task_info['start_time']:
                    dependency_satisfied = False
                    break

            if dependency_satisfied:
                satisfaction_score += 1

            # 检查物料依赖（针对组装任务）
            if task.task_type == TaskType.ASSEMBLY:
                requirements = self.material_flow.assembly_requirements.get(task.task_id, {})
                material_satisfied = True

                for injection_id, req_info in requirements.items():
                    injection_info = schedule['tasks'].get(injection_id)
                    if not injection_info:
                        material_satisfied = False
                        break

                    # 检查是否满足初始批量
                    initial_batch_time = self._estimate_batch_completion(
                        injection_info, req_info['initial_batch']
                    )

                    if initial_batch_time > task_info['start_time']:
                        material_satisfied = False
                        break

                if material_satisfied:
                    satisfaction_score += 0.5  # 额外加分

        return satisfaction_score / max_score

    def _estimate_batch_completion(self, injection_info, batch_size):
        """估计完成指定批量所需的时间"""
        task = self.task_map.get(injection_info['task_id'])
        if not task or not isinstance(task, InjectionTask):
            return injection_info['end_time']

        # 计算生产batch_size所需的时间比例
        batch_ratio = batch_size / task.quantity
        batch_duration = (injection_info['end_time'] - injection_info['start_time']) * batch_ratio

        return injection_info['start_time'] + batch_duration

    def _calculate_inventory_cost(self, schedule):
        """计算库存成本（在制品库存）"""
        inventory_cost = 0

        # 跟踪每个时间点的在制品数量
        time_points = set()
        inventory_events = []

        for task_info in schedule['tasks'].values():
            if task_info['task_type'] == 'injection':
                # 注塑任务：生产时增加库存，被组装消耗时减少库存
                # 这里简化：假设生产后立即成为库存
                time_points.add(task_info['start_time'])
                time_points.add(task_info['end_time'])

                inventory_events.append((task_info['start_time'], 'start', task_info))
                inventory_events.append((task_info['end_time'], 'end', task_info))

        # 按时间排序
        time_points = sorted(time_points)
        inventory_events.sort(key=lambda x: x[0])

        # 计算每个时间段内的平均库存
        current_inventory = 0
        last_time = 0

        for time in time_points:
            if time > last_time:
                # 计算这段时间的库存成本
                duration = time - last_time
                inventory_cost += current_inventory * duration * 0.01  # 单位库存成本
                last_time = time

            # 更新当前库存
            for event_time, event_type, task_info in inventory_events:
                if event_time == time:
                    if event_type == 'start':
                        # 开始生产，库存逐渐增加
                        current_inventory += task_info['quantity'] * 0.5  # 简化：按一半计算
                    else:
                        # 生产完成，全部成为库存
                        current_inventory += task_info['quantity'] * 0.5

        return inventory_cost


class DependencyPreservingOperators:
    """保持依赖关系的遗传算子"""

    @staticmethod
    def crossover(parent1, parent2):
        """交叉算子：保持依赖关系"""
        # 确保两个染色体有相同的结构
        if (len(parent1['task_sequence']) != len(parent2['task_sequence']) or
                len(parent1['resource_assignment']) != len(parent2['resource_assignment'])):
            return parent1, parent2

        child1 = {
            'task_sequence': parent1['task_sequence'].copy(),
            'resource_assignment': parent1['resource_assignment'].copy(),
            'time_offsets': parent1['time_offsets'].copy(),
            'batch_overlap': parent1['batch_overlap']
        }

        child2 = {
            'task_sequence': parent2['task_sequence'].copy(),
            'resource_assignment': parent2['resource_assignment'].copy(),
            'time_offsets': parent2['time_offsets'].copy(),
            'batch_overlap': parent2['batch_overlap']
        }

        # 任务序列交叉（保持依赖的顺序）
        if random.random() < 0.7:
            child1['task_sequence'], child2['task_sequence'] = (
                DependencyPreservingOperators._sequence_crossover(
                    parent1['task_sequence'], parent2['task_sequence']
                )
            )

        # 资源分配交叉
        if random.random() < 0.5:
            child1['resource_assignment'], child2['resource_assignment'] = (
                DependencyPreservingOperators._resource_crossover(
                    parent1['resource_assignment'], parent2['resource_assignment']
                )
            )

        # 时间偏移交叉（混合交叉）
        if random.random() < 0.5:
            child1['time_offsets'], child2['time_offsets'] = (
                DependencyPreservingOperators._blend_crossover(
                    parent1['time_offsets'], parent2['time_offsets']
                )
            )

        # 批次重叠参数交叉
        child1['batch_overlap'] = (parent1['batch_overlap'] + parent2['batch_overlap']) / 2
        child2['batch_overlap'] = child1['batch_overlap']

        return child1, child2

    @staticmethod
    def _sequence_crossover(seq1, seq2):
        """顺序交叉，保持相对顺序"""
        size = len(seq1)

        # 选择两个交叉点
        cxpoint1 = random.randint(0, size - 2)
        cxpoint2 = random.randint(cxpoint1 + 1, size - 1)

        # 初始化子代
        child1 = [None] * size
        child2 = [None] * size

        # 复制中间段
        child1[cxpoint1:cxpoint2] = seq2[cxpoint1:cxpoint2]
        child2[cxpoint1:cxpoint2] = seq1[cxpoint1:cxpoint2]

        # 填充剩余位置
        index1 = index2 = 0

        for i in range(size):
            if i < cxpoint1 or i >= cxpoint2:
                # 找到不在中间段的基因
                while index1 < size and seq1[index1] in child1[cxpoint1:cxpoint2]:
                    index1 += 1
                if index1 < size:
                    child1[i] = seq1[index1]
                    index1 += 1

                while index2 < size and seq2[index2] in child2[cxpoint1:cxpoint2]:
                    index2 += 1
                if index2 < size:
                    child2[i] = seq2[index2]
                    index2 += 1

        return child1, child2

    @staticmethod
    def _resource_crossover(res1, res2):
        """资源分配交叉"""
        size = len(res1)
        child1 = res1.copy()
        child2 = res2.copy()

        # 均匀交叉
        for i in range(size):
            if random.random() < 0.5:
                child1[i], child2[i] = child2[i], child1[i]

        return child1, child2

    @staticmethod
    def _blend_crossover(offsets1, offsets2):
        """混合交叉（用于连续值）"""
        child1 = []
        child2 = []

        for off1, off2 in zip(offsets1, offsets2):
            alpha = random.random() * 0.5
            lower = min(off1, off2) - alpha * abs(off1 - off2)
            upper = max(off1, off2) + alpha * abs(off1 - off2)

            child1.append(random.uniform(lower, upper))
            child2.append(random.uniform(lower, upper))

        return child1, child2

    @staticmethod
    def mutation(individual, indpb, tasks, material_flow):
        """变异算子"""
        task_map = {t.task_id: t for t in tasks}

        # 任务序列变异（交换变异，但保持依赖）
        for i in range(len(individual['task_sequence'])):
            if random.random() < indpb:
                # 找到可以交换的位置
                swap_candidates = []
                for j in range(len(individual['task_sequence'])):
                    if i != j:
                        # 检查交换是否破坏依赖关系
                        if DependencyPreservingOperators._can_swap(
                                individual['task_sequence'], i, j, task_map, material_flow
                        ):
                            swap_candidates.append(j)

                if swap_candidates:
                    j = random.choice(swap_candidates)
                    # 交换位置
                    individual['task_sequence'][i], individual['task_sequence'][j] = (
                        individual['task_sequence'][j], individual['task_sequence'][i]
                    )
                    # 同时交换资源分配和时间偏移
                    individual['resource_assignment'][i], individual['resource_assignment'][j] = (
                        individual['resource_assignment'][j], individual['resource_assignment'][i]
                    )
                    individual['time_offsets'][i], individual['time_offsets'][j] = (
                        individual['time_offsets'][j], individual['time_offsets'][i]
                    )

        # 资源分配变异
        for i in range(len(individual['resource_assignment'])):
            if random.random() < indpb:
                task_id = individual['task_sequence'][i]
                task = task_map.get(task_id)

                if task:
                    if task.task_type == TaskType.INJECTION:
                        # 注塑任务：在可用机器范围内变异
                        individual['resource_assignment'][i] = random.randint(0, 2)
                    else:
                        # 组装任务：在可用组装线范围内变异
                        individual['resource_assignment'][i] = random.randint(0, 1)

        # 时间偏移变异
        for i in range(len(individual['time_offsets'])):
            if random.random() < indpb:
                # 高斯变异
                task_id = individual['task_sequence'][i]
                task = task_map.get(task_id)

                if task:
                    if task.task_type == TaskType.INJECTION:
                        # 注塑任务：较大的变异范围
                        individual['time_offsets'][i] += random.gauss(0, 60)
                        individual['time_offsets'][i] = max(0, individual['time_offsets'][i])
                    else:
                        # 组装任务：较小的变异范围
                        individual['time_offsets'][i] += random.gauss(0, 30)
                        individual['time_offsets'][i] = max(0, individual['time_offsets'][i])

        # 批次重叠参数变异
        if random.random() < indpb:
            individual['batch_overlap'] += random.gauss(0, 0.1)
            individual['batch_overlap'] = max(0, min(1, individual['batch_overlap']))

        return individual

    @staticmethod
    def _can_swap(sequence, i, j, task_map, material_flow):
        """检查交换两个任务是否破坏依赖关系"""
        task_i = task_map.get(sequence[i])
        task_j = task_map.get(sequence[j])

        if not task_i or not task_j:
            return True

        # 检查直接依赖
        if task_j in task_i.predecessors:
            return False
        if task_i in task_j.predecessors:
            return False

        # 检查间接依赖（通过物料流）
        if (task_i.task_type == TaskType.INJECTION and
                task_j.task_type == TaskType.ASSEMBLY):
            # 检查task_i是否是task_j的供应商
            if sequence[i] in material_flow.injection_to_assembly:
                for dep in material_flow.injection_to_assembly[sequence[i]]:
                    if dep['assembly_id'] == sequence[j]:
                        return False

        if (task_j.task_type == TaskType.INJECTION and
                task_i.task_type == TaskType.ASSEMBLY):
            # 检查task_j是否是task_i的供应商
            if sequence[j] in material_flow.injection_to_assembly:
                for dep in material_flow.injection_to_assembly[sequence[j]]:
                    if dep['assembly_id'] == sequence[i]:
                        return False

        return True


class InjectionAssemblyScheduler:
    """注塑-组装排产引擎"""

    def __init__(self):
        self.tasks = []
        self.injection_machines = []
        self.assembly_lines = []
        self.molds = []
        self.material_flow = MaterialFlow()

        # DEAP配置
        self._setup_deap()

    def _setup_deap(self):
        """设置DEAP框架"""
        # 定义多目标适应度（最小化所有目标）
        creator.create("FitnessMulti", base.Fitness,
                       weights=(-1.0, -1.0, 1.0, 1.0, -1.0))
        creator.create("Individual", dict, fitness=creator.FitnessMulti)

        self.toolbox = base.Toolbox()

        # 注册个体创建函数
        self.toolbox.register("individual", self._create_individual)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)

        # 注册遗传算子
        self.toolbox.register("mate", DependencyPreservingOperators.crossover)
        self.toolbox.register("mutate", DependencyPreservingOperators.mutation,
                              indpb=0.1, tasks=self.tasks, material_flow=self.material_flow)
        self.toolbox.register("select", tools.selNSGA2)

    def _create_individual(self):
        """创建个体"""
        encoder = DependencyAwareEncoder()
        chromosome = encoder.encode(self.tasks, self.material_flow)
        individual = creator.Individual(chromosome)
        return individual

    def add_injection_machine(self, machine_id, capacity, **kwargs):
        """添加注塑机"""
        machine = InjectionMachine(machine_id, capacity, **kwargs)
        self.injection_machines.append(machine)
        return machine

    def add_assembly_line(self, line_id, capacity, **kwargs):
        """添加组装线"""
        line = AssemblyLine(line_id, capacity, **kwargs)
        self.assembly_lines.append(line)
        return line

    def add_mold(self, mold_id, compatible_machines, **kwargs):
        """添加模具"""
        mold = Mold(mold_id, compatible_machines, **kwargs)
        self.molds.append(mold)
        return mold

    def add_injection_task(self, task_id, product_id, quantity, mold_id, **kwargs):
        """添加注塑任务"""
        task = InjectionTask(task_id, product_id, quantity, mold_id, **kwargs)
        self.tasks.append(task)
        return task

    def add_assembly_task(self, task_id, product_id, quantity, line_id,assembly_time_per_unit, parts_required, **kwargs):
        """添加组装任务"""
        task = AssemblyTask(task_id, product_id, quantity, line_id, assembly_time_per_unit,parts_required, **kwargs)
        self.tasks.append(task)
        return task

    def add_dependency(self, injection_task_id, assembly_task_id,
                       required_quantity, initial_batch=0):
        """添加注塑-组装依赖关系"""
        self.material_flow.add_dependency(
            injection_task_id, assembly_task_id, required_quantity, initial_batch
        )

        # 同时更新任务依赖
        injection_task = None
        assembly_task = None

        for task in self.tasks:
            if task.task_id == injection_task_id:
                injection_task = task
            elif task.task_id == assembly_task_id:
                assembly_task = task

        if injection_task and assembly_task:
            assembly_task.add_dependency(injection_task)

    def optimize(self, population_size=100, generations=200,
                 cxpb=0.7, mutpb=0.3, verbose=True):
        """执行优化"""
        # 创建初始种群
        pop = self.toolbox.population(n=population_size)

        # 创建解码器和评估器
        decoder = ResourceAwareDecoder(
            self.injection_machines, self.assembly_lines,
            self.molds, self.material_flow
        )
        evaluator = MultiObjectiveFitness(
            self.tasks, self.injection_machines, self.assembly_lines,
            self.material_flow
        )

        # 评估函数
        def evaluate(individual):
            # 解码染色体
            schedule = decoder.decode(individual, self.tasks)
            # 评估适应度
            return evaluator.evaluate(schedule)

        self.toolbox.register("evaluate", evaluate)

        # 评估初始种群
        invalid_ind = [ind for ind in pop if not ind.fitness.valid]
        fitnesses = self.toolbox.map(self.toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # 设置统计
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", np.mean, axis=0)
        stats.register("min", np.min, axis=0)
        stats.register("max", np.max, axis=0)

        # 进化循环
        logbook = tools.Logbook()
        logbook.header = ["gen", "nevals"] + stats.fields

        for gen in range(generations):
            # 选择下一代
            offspring = self.toolbox.select(pop, len(pop))

            # 克隆选中个体
            offspring = list(map(self.toolbox.clone, offspring))

            # 应用交叉和变异
            for child1, child2 in zip(offspring[::2], offspring[1::2]):
                if random.random() < cxpb:
                    self.toolbox.mate(child1, child2)
                    del child1.fitness.values
                    del child2.fitness.values

            for mutant in offspring:
                if random.random() < mutpb:
                    self.toolbox.mutate(mutant)
                    del mutant.fitness.values

            # 评估新个体
            invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
            fitnesses = self.toolbox.map(self.toolbox.evaluate, invalid_ind)
            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit

            # 替换种群
            pop[:] = offspring

            # 记录统计
            record = stats.compile(pop)
            logbook.record(gen=gen, nevals=len(invalid_ind), **record)

            if verbose and gen % 10 == 0:
                print(f"Generation {gen}:")
                print(f"  Makespan: {record['avg'][0]:.1f} min")
                print(f"  Tardiness: {record['avg'][1]:.1f}")
                print(f"  Utilization: {-record['avg'][2] * 100:.1f}%")
                print(f"  Dependency: {-record['avg'][3] * 100:.1f}%")
                print(f"  Inventory: {record['avg'][4]:.1f}")

        return pop, logbook

    def get_best_schedule(self, population):
        """获取最优排产方案"""
        # 使用非支配排序
        fronts = tools.sortNondominated(population, len(population))
        pareto_front = fronts[0]

        # 解码器
        decoder = ResourceAwareDecoder(
            self.injection_machines, self.assembly_lines,
            self.molds, self.material_flow
        )

        # 评估每个解
        schedules = []
        for ind in pareto_front:
            schedule = decoder.decode(ind, self.tasks)
            makespan = max([t['end_time'] for t in schedule['tasks'].values()])
            schedules.append((makespan, schedule, ind))

        # 选择完工时间最短的方案
        best_schedule = min(schedules, key=lambda x: x[0])

        return best_schedule[1], best_schedule[2].fitness.values

    def print_schedule(self, schedule):
        """打印排产计划"""
        print("\n" + "=" * 100)
        print("排产计划")
        print("=" * 100)
        print(f"{'任务ID':<12} {'类型':<10} {'资源':<10} {'开始时间':<20} {'结束时间':<20} {'数量':<10} {'状态':<10}")
        print("-" * 100)

        # 按开始时间排序
        sorted_tasks = sorted(
            schedule['tasks'].values(),
            key=lambda x: x['start_time']
        )

        for task_info in sorted_tasks:
            task_id = task_info['task_id']
            task_type = task_info['task_type']

            if task_type == 'injection':
                resource = f"机器{task_info['machine_id']}"
            else:
                resource = f"组装线{task_info['line_id']}"

            # 转换时间格式
            start_time = self._minutes_to_time(task_info['start_time'])
            end_time = self._minutes_to_time(task_info['end_time'])

            print(f"{task_id:<12} {task_type:<10} {resource:<10} "
                  f"{start_time:<20} {end_time:<20} {task_info['quantity']:<10} {'已排产':<10}")

    def _minutes_to_time(self, minutes):
        """将分钟数转换为时间字符串"""
        days = minutes // (24 * 60)
        hours = (minutes % (24 * 60)) // 60
        mins = minutes % 60

        return f"D{days} {hours:02d}:{mins:02d}"

    def analyze_dependencies(self, schedule):
        """分析依赖关系满足情况"""
        print("\n" + "=" * 100)
        print("依赖关系分析")
        print("=" * 100)

        for task in self.tasks:
            if task.task_type == TaskType.ASSEMBLY:
                task_info = schedule['tasks'].get(task.task_id)
                if not task_info:
                    continue

                print(f"\n组装任务 {task.task_id}:")
                print(f"  计划开始时间: {self._minutes_to_time(task_info['start_time'])}")

                # 检查物料依赖
                requirements = self.material_flow.assembly_requirements.get(task.task_id, {})
                for injection_id, req_info in requirements.items():
                    injection_info = schedule['tasks'].get(injection_id)
                    if injection_info:
                        # 计算初始批量完成时间
                        injection_task = next(t for t in self.tasks if t.task_id == injection_id)
                        if isinstance(injection_task, InjectionTask):
                            batch_time = injection_task.setup_time + (
                                    req_info['initial_batch'] / injection_task.unit_per_cycle
                            ) * injection_task.cycle_time

                            batch_complete = injection_info['start_time'] + batch_time

                            status = "满足" if batch_complete <= task_info['start_time'] else "不满足"
                            print(f"  依赖注塑任务 {injection_id}:")
                            print(f"    所需数量: {req_info['required']}")
                            print(f"    初始批量: {req_info['initial_batch']}")
                            print(f"    批量完成时间: {self._minutes_to_time(batch_complete)}")
                            print(f"    状态: {status}")


def create_complex_scenario():
    """创建复杂注塑-组装场景"""

    scheduler = InjectionAssemblyScheduler()

    # 1. 添加资源
    print("添加资源...")

    # 添加注塑机
    scheduler.add_injection_machine("IM-01", capacity=100, efficiency=0.95)
    scheduler.add_injection_machine("IM-02", capacity=120, efficiency=0.92)
    scheduler.add_injection_machine("IM-03", capacity=90, efficiency=0.88)

    # 添加组装线
    scheduler.add_assembly_line("AL-01", capacity=200, workers=3)
    scheduler.add_assembly_line("AL-02", capacity=180, workers=2)

    # 添加模具
    scheduler.add_mold("MOLD-A", compatible_machines=["IM-01", "IM-02"], setup_time=30)
    scheduler.add_mold("MOLD-B", compatible_machines=["IM-01", "IM-03"], setup_time=45)
    scheduler.add_mold("MOLD-C", compatible_machines=["IM-02", "IM-03"], setup_time=25)

    # 2. 创建成品A：需要3种注塑零件
    print("\n创建成品A的生产任务...")

    # 成品A的注塑零件
    injection_tasks_A = []
    for i in range(3):
        task_id = f"INJ-A-{i + 1}"
        mold_id = f"MOLD-{chr(65 + i)}"  # A, B, C
        quantity = 1000

        task = scheduler.add_injection_task(
            task_id=task_id,
            product_id=f"PART-A-{i + 1}",
            quantity=quantity,
            mold_id=mold_id,
            cycle_time=2.5,  # 2.5分钟/循环
            priority=2,
            due_date=3 * 24 * 60  # 3天内完成
        )
        injection_tasks_A.append(task)

    # 成品A的组装任务
    assembly_task_A = scheduler.add_assembly_task(
        task_id="ASSY-A",
        product_id="PRODUCT-A",
        quantity=500,  # 组装500个成品
        line_id="AL-01",
        parts_required={f"PART-A-{i + 1}": 2 for i in range(3)},  # 每个成品需要2个每种零件
        assembly_time_per_unit=5,  # 5分钟/个
        priority=1,
        due_date=4 * 24 * 60  # 4天内完成
    )

    # 设置依赖关系
    for inj_task in injection_tasks_A:
        scheduler.add_dependency(
            injection_task_id=inj_task.task_id,
            assembly_task_id=assembly_task_A.task_id,
            required_quantity=inj_task.quantity,
            initial_batch=200  # 生产200个后组装就可以开始
        )

    # 3. 创建成品B：需要2种注塑零件
    print("\n创建成品B的生产任务...")

    injection_tasks_B = []
    for i in range(2):
        task_id = f"INJ-B-{i + 1}"
        mold_id = f"MOLD-{chr(65 + i)}"  # A, B
        quantity = 800

        task = scheduler.add_injection_task(
            task_id=task_id,
            product_id=f"PART-B-{i + 1}",
            quantity=quantity,
            mold_id=mold_id,
            cycle_time=3.0,
            priority=3,
            due_date=2 * 24 * 60 + 12 * 60  # 2.5天内完成
        )
        injection_tasks_B.append(task)

    # 成品B的组装任务
    assembly_task_B = scheduler.add_assembly_task(
        task_id="ASSY-B",
        product_id="PRODUCT-B",
        quantity=400,
        line_id="AL-02",
        parts_required={"PART-B-1": 1, "PART-B-2": 2},
        assembly_time_per_unit=4,
        priority=2,
        due_date=3 * 24 * 60
    )

    # 设置依赖关系
    for inj_task in injection_tasks_B:
        scheduler.add_dependency(
            injection_task_id=inj_task.task_id,
            assembly_task_id=assembly_task_B.task_id,
            required_quantity=inj_task.quantity,
            initial_batch=150
        )

    # 4. 创建成品C：与A共享部分零件
    print("\n创建成品C的生产任务...")

    # 成品C需要已有的PART-A-1和新的PART-C-1
    injection_task_C = scheduler.add_injection_task(
        task_id="INJ-C-1",
        product_id="PART-C-1",
        quantity=600,
        mold_id="MOLD-B",
        cycle_time=2.8,
        priority=2,
        due_date=3 * 24 * 60
    )

    assembly_task_C = scheduler.add_assembly_task(
        task_id="ASSY-C",
        product_id="PRODUCT-C",
        quantity=300,
        line_id="AL-01",  # 与A共享组装线
        parts_required={"PART-A-1": 1, "PART-C-1": 1},
        assembly_time_per_unit=6,
        priority=3,
        due_date=4 * 24 * 60
    )

    # 设置依赖关系
    scheduler.add_dependency(
        injection_task_id="INJ-A-1",  # 共享零件
        assembly_task_id=assembly_task_C.task_id,
        required_quantity=300,  # 只需要300个
        initial_batch=100
    )

    scheduler.add_dependency(
        injection_task_id=injection_task_C.task_id,
        assembly_task_id=assembly_task_C.task_id,
        required_quantity=injection_task_C.quantity,
        initial_batch=120
    )

    return scheduler


def main():
    """主函数"""
    print("=" * 80)
    print("注塑-组装多级依赖排产系统")
    print("=" * 80)

    # 创建排产场景
    scheduler = create_complex_scenario()

    print(f"\n任务统计:")
    print(f"  注塑任务: {len([t for t in scheduler.tasks if t.task_type == TaskType.INJECTION])}")
    print(f"  组装任务: {len([t for t in scheduler.tasks if t.task_type == TaskType.ASSEMBLY])}")
    print(f"  资源: {len(scheduler.injection_machines)}台注塑机, "
          f"{len(scheduler.assembly_lines)}条组装线, "
          f"{len(scheduler.molds)}套模具")

    # 执行优化
    print("\n开始优化排产...")
    population, logbook = scheduler.optimize(
        population_size=80,
        generations=150,
        cxpb=0.8,
        mutpb=0.2,
        verbose=True
    )

    # 获取最优方案
    best_schedule, fitness_values = scheduler.get_best_schedule(population)

    print("\n" + "=" * 80)
    print("优化结果")
    print("=" * 80)
    print(f"总完工时间: {fitness_values[0]:.1f} 分钟 ({fitness_values[0] / 60:.1f} 小时)")
    print(f"总延迟惩罚: {fitness_values[1]:.1f}")
    print(f"资源利用率: {-fitness_values[2] * 100:.1f}%")
    print(f"依赖关系满足度: {-fitness_values[3] * 100:.1f}%")
    print(f"库存成本: {fitness_values[4]:.1f}")

    # 打印排产计划
    scheduler.print_schedule(best_schedule)

    # 分析依赖关系
    scheduler.analyze_dependencies(best_schedule)

    # 分析资源利用率
    print("\n" + "=" * 80)
    print("资源利用率分析")
    print("=" * 80)

    # 注塑机利用率
    makespan = max([t['end_time'] for t in best_schedule['tasks'].values()])

    for machine in scheduler.injection_machines:
        busy_time = 0
        for task_info in best_schedule['tasks'].values():
            if (task_info['task_type'] == 'injection' and
                    task_info.get('machine_id') == machine.machine_id):
                busy_time += task_info['end_time'] - task_info['start_time']

        utilization = busy_time / makespan if makespan > 0 else 0
        print(f"注塑机 {machine.machine_id}: {utilization * 100:.1f}%")

    for line in scheduler.assembly_lines:
        busy_time = 0
        for task_info in best_schedule['tasks'].values():
            if (task_info['task_type'] == 'assembly' and
                    task_info.get('line_id') == line.line_id):
                busy_time += task_info['end_time'] - task_info['start_time']

        utilization = busy_time / makespan if makespan > 0 else 0
        print(f"组装线 {line.line_id}: {utilization * 100:.1f}%")

    return scheduler, best_schedule


if __name__ == "__main__":
    scheduler, schedule = main()