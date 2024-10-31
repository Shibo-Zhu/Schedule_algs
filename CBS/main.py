import heapq
from collections import deque
import time

class Task:
    def __init__(self, task_id, arrival_time, exec_time):
        self.task_id = task_id
        self.arrival_time = arrival_time
        self.exec_time = exec_time
        self.remaining_time = exec_time

class CBS:
    def __init__(self, Q_s, T_s):
        self.Q_s = Q_s  # 最大预算
        self.T_s = T_s  # 周期
        self.c = Q_s  # 当前预算
        self.d_k = T_s  # 当前截止期
        self.queue = deque()  # 任务队列
        self.current_task = None
        self.time = 0  # 模拟当前时间

    def add_task(self, task):
        print(f"Task {task.task_id} arrives at time {task.arrival_time}")
        self.queue.append(task)
        if self.current_task is None:
            self._assign_task()

    def _assign_task(self):
        """根据 CBS 规则分配任务的截止期和预算"""
        if not self.queue:
            self.current_task = None
            return
        
        task = self.queue.popleft()
        
        # 规则1：如果预算不够满足截止期
        if self.time + (self.c / self.Q_s) * self.T_s >= self.d_k:
            self.d_k = self.time + self.T_s
            self.c = self.Q_s
            print(f"Applying Rule 1: New deadline = {self.d_k}, Reset budget = {self.c}")
        else:
            # 规则2：预算不变，截止期延后
            self.d_k -= 1
            print(f"Applying Rule 2: Deadline adjusted to {self.d_k}")
        
        self.current_task = task

    def execute(self):
        """执行当前任务并模拟 CBS 的预算和截止期管理"""
        while self.current_task:
            # 执行当前任务
            self.current_task.remaining_time -= 1
            self.c -= 1
            print(f"Executing Task {self.current_task.task_id}, Remaining time: {self.current_task.remaining_time}, Budget left: {self.c}")

            # 检查任务是否完成
            if self.current_task.remaining_time <= 0:
                print(f"Task {self.current_task.task_id} completed")
                self.current_task = None
                self._assign_task()  # 选择下一个任务
            
            # 检查预算是否耗尽
            elif self.c == 0:
                print("Budget exhausted, applying Rule 3")
                self.d_k += self.T_s
                self.c = self.Q_s
                print(f"New deadline = {self.d_k}, Reset budget = {self.c}")
            
            # 模拟时间前进
            self.time += 1
            time.sleep(0.1)  # 模拟时间流逝，可以注释掉以便更快运行

# 模拟任务添加和 CBS 调度
cbs = CBS(Q_s=5, T_s=10)  # 定义带宽和周期

tasks = [
    Task(task_id=1, arrival_time=0, exec_time=3),
    Task(task_id=2, arrival_time=2, exec_time=5),
    Task(task_id=3, arrival_time=4, exec_time=2),
]

# 添加任务并执行调度
for task in tasks:
    cbs.add_task(task)

cbs.execute()
