from ortools.sat.python import cp_model
import datetime

# ===================== 1. 基础配置与模拟数据 =====================
# 班次定义：白班=偶数班次ID，夜班=奇数班次ID
SHIFT_WHITE = 0
SHIFT_NIGHT = 1
MAX_SHIFT = 30  # 最大排产班次（20天）

# 基准日期，今天
BASE_DATE = datetime.date.today()

orders = {
    "O1": {
        "due_date": datetime.date(2025, 12, 30),  # 第9天 → 班次ID=19（夜班）
        "final_product": "P1",
        "qty": 300
    },
    "O2": {
        "due_date": datetime.date(2025, 12, 25),  # 第11天 → 班次ID=23（夜班）
        "final_product": "P2",
        "qty": 500
    },
    "O3": {
        "due_date": datetime.date(2025, 1, 10),  # 第14天 → 班次ID=29（夜班）
        "final_product": "P1",
        "qty": 600
    }
}

# 转换交货期为班次ID
for order_id, order in orders.items():
    days_diff = (order["due_date"] - BASE_DATE).days
    order["due_shift"] = days_diff * 2 + 1  # 交货期设为当天夜班结束

# BOM结构：父物料 → {子物料: (配比)}
bom_structure = {
    "P1": {"S1": 1},  # 1个P1需2个S1，
    "P2": {"S2": 1},  # 1个P2需1个S2，
    "S1": {"I1": 1},  # 1个S1需1个I1，
    "S2": {"I2": 1},  # 1个S2需1个I2，
}

# 注塑资源：机台+模具组合的班产能
injection_resources = {
    "M1_M101": {"machine": "M1", "mold": "M101", "cap": 100},
    "M1_M102": {"machine": "M1", "mold": "M102", "cap": 100},
    "M2_M101": {"machine": "M2", "mold": "M101", "cap": 100},
    "M2_M102": {"machine": "M2", "mold": "M102", "cap": 100},
}
# 注塑半成品对应可用资源
injection_semi_mapping = {
    "I1": ["M1_M101", "M2_M101"],  # I1仅用M101模具
    "I2": ["M1_M102", "M2_M102"],  # I2仅用M102模具
}
# 机加/组装班产能
machining_cap = {"S1": 200, 'S2': 300}
assembly_cap = {"P1": 300, 'P2': 300}
