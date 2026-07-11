"""
進程管理模擬模塊
Python 實現的進程創建、調度與終止模擬。
"""
from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum
import time
from collections import deque


class ProcessState(Enum):
    """進程狀態枚舉。"""
    NEW = "new"
    READY = "ready"
    RUNNING = "running"
    WAITING = "waiting"
    TERMINATED = "terminated"


@dataclass
class PCB:
    """進程控制塊 (Process Control Block)。"""
    pid: int
    name: str
    priority: int = 0
    burst_time: int = 0
    arrival_time: int = 0
    state: ProcessState = ProcessState.NEW
    remaining_time: int = 0

    def __post_init__(self):
        if self.remaining_time == 0:
            self.remaining_time = self.burst_time


class ProcessSimulator:
    """進程模擬器。"""

    _next_pid = 1

    def __init__(self):
        """初始化進程模擬器。"""
        self._processes: List[PCB] = []
        self._ready_queue = deque()

    def create_process(self, name: str, burst_time: int,
                       priority: int = 0,
                       arrival_time: int = 0) -> PCB:
        """
        創建新進程。

        Args:
            name: 進程名稱
            burst_time: 執行時間
            priority: 優先級
            arrival_time: 到達時間

        Returns:
            進程控制塊
        """
        pcb = PCB(
            pid=ProcessSimulator._next_pid,
            name=name,
            priority=priority,
            burst_time=burst_time,
            arrival_time=arrival_time
        )
        ProcessSimulator._next_pid += 1
        pcb.state = ProcessState.READY
        self._processes.append(pcb)
        self._ready_queue.append(pcb)
        return pcb

    def terminate_process(self, pid: int) -> bool:
        """
        終止進程。

        Args:
            pid: 進程 ID

        Returns:
            是否成功終止
        """
        for p in self._processes:
            if p.pid == pid:
                p.state = ProcessState.TERMINATED
                return True
        return False

    def list_processes(self) -> List[PCB]:
        """列出所有進程。"""
        return [p for p in self._processes
                if p.state != ProcessState.TERMINATED]
