"""
進程調度算法模擬
實現 FCFS、SJF、時間片輪轉 (RR) 等調度算法的可視化模擬。
"""
from dataclasses import dataclass
from typing import List
from collections import deque


@dataclass
class Process:
    """進程數據類。"""
    name: str
    arrival_time: int
    burst_time: int
    remaining_time: int = 0
    completion_time: int = 0
    waiting_time: int = 0
    turnaround_time: int = 0

    def __post_init__(self):
        if self.remaining_time == 0:
            self.remaining_time = self.burst_time


def fcfs(processes: List[Process]) -> dict:
    """
    先來先服務 (First Come First Served) 調度算法。

    Args:
        processes: 進程列表

    Returns:
        調度結果統計
    """
    sorted_procs = sorted(processes, key=lambda p: p.arrival_time)
    current_time = 0

    for p in sorted_procs:
        if current_time < p.arrival_time:
            current_time = p.arrival_time
        p.completion_time = current_time + p.burst_time
        p.turnaround_time = p.completion_time - p.arrival_time
        p.waiting_time = p.turnaround_time - p.burst_time
        current_time = p.completion_time

    return _calc_stats(sorted_procs)


def sjf(processes: List[Process]) -> dict:
    """
    短作業優先 (Shortest Job First) 調度算法。

    Args:
        processes: 進程列表

    Returns:
        調度結果統計
    """
    sorted_procs = sorted(processes, key=lambda p: p.arrival_time)
    completed = []
    current_time = 0
    remaining = list(sorted_procs)

    while remaining:
        # 找到已到達且執行時間最短的進程
        available = [p for p in remaining if p.arrival_time <= current_time]
        if not available:
            current_time = remaining[0].arrival_time
            continue

        shortest = min(available, key=lambda p: p.burst_time)
        remaining.remove(shortest)

        shortest.completion_time = current_time + shortest.burst_time
        shortest.turnaround_time = shortest.completion_time - shortest.arrival_time
        shortest.waiting_time = shortest.turnaround_time - shortest.burst_time
        current_time = shortest.completion_time
        completed.append(shortest)

    return _calc_stats(completed)


def round_robin(processes: List[Process], quantum: int = 2) -> dict:
    """
    時間片輪轉 (Round Robin) 調度算法。

    Args:
        processes: 進程列表
        quantum: 時間片大小

    Returns:
        調度結果統計
    """
    queue = deque(sorted(processes, key=lambda p: p.arrival_time))
    current_time = 0
    completed = []

    while queue:
        p = queue.popleft()

        if current_time < p.arrival_time:
            current_time = p.arrival_time

        exec_time = min(quantum, p.remaining_time)
        p.remaining_time -= exec_time
        current_time += exec_time

        if p.remaining_time > 0:
            queue.append(p)
        else:
            p.completion_time = current_time
            p.turnaround_time = current_time - p.arrival_time
            p.waiting_time = p.turnaround_time - p.burst_time
            completed.append(p)

    return _calc_stats(completed)


def _calc_stats(processes: List[Process]) -> dict:
    """計算調度結果統計。"""
    if not processes:
        return {"avg_waiting": 0, "avg_turnaround": 0, "schedule": []}

    avg_wt = sum(p.waiting_time for p in processes) / len(processes)
    avg_tt = sum(p.turnaround_time for p in processes) / len(processes)

    return {
        "avg_waiting": round(avg_wt, 2),
        "avg_turnaround": round(avg_tt, 2),
        "schedule": [
            {
                "name": p.name,
                "at": p.arrival_time,
                "bt": p.burst_time,
                "ct": p.completion_time,
                "wt": p.waiting_time,
                "tat": p.turnaround_time
            }
            for p in processes
        ]
    }


if __name__ == "__main__":
    # 示例進程
    procs = [
        Process("P1", 0, 6),
        Process("P2", 1, 4),
        Process("P3", 2, 8),
        Process("P4", 3, 2),
    ]

    print("=== FCFS ===")
    result = fcfs([Process(p.name, p.arrival_time, p.burst_time) for p in procs])
    print(f"平均等待時間: {result['avg_waiting']}")
    print(f"平均周轉時間: {result['avg_turnaround']}")

    print("\n=== SJF ===")
    result = sjf([Process(p.name, p.arrival_time, p.burst_time) for p in procs])
    print(f"平均等待時間: {result['avg_waiting']}")
    print(f"平均周轉時間: {result['avg_turnaround']}")

    print("\n=== Round Robin (q=2) ===")
    result = round_robin([Process(p.name, p.arrival_time, p.burst_time) for p in procs])
    print(f"平均等待時間: {result['avg_waiting']}")
    print(f"平均周轉時間: {result['avg_turnaround']}")
