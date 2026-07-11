"""
死鎖檢測模塊
模擬死鎖產生條件與檢測算法（銀行家算法、資源分配圖）。
"""
from typing import List, Dict


class DeadlockDetector:
    """死鎖檢測器，使用銀行家算法進行安全序列檢測。"""

    def __init__(self, total_resources: Dict[str, int]):
        """
        初始化死鎖檢測器。

        Args:
            total_resources: 系統總資源（如 {"A": 10, "B": 5}）
        """
        self._total = total_resources
        self._available = dict(total_resources)
        self._allocation: Dict[str, Dict[str, int]] = {}
        self._need: Dict[str, Dict[str, int]] = {}

    def add_process(self, pid: str, max_need: Dict[str, int]):
        """
        添加進程及其最大資源需求。

        Args:
            pid: 進程 ID
            max_need: 最大資源需求
        """
        self._allocation[pid] = {r: 0 for r in self._total}
        self._need[pid] = dict(max_need)

    def allocate(self, pid: str, request: Dict[str, int]) -> bool:
        """
        嘗試為進程分配資源。

        Args:
            pid: 進程 ID
            request: 請求的資源量

        Returns:
            是否可以安全分配
        """
        # 檢查請求是否超過需要
        for r in request:
            if request[r] > self._need[pid].get(r, 0):
                return False
            if request[r] > self._available[r]:
                return False

        # 嘗試分配
        for r in request:
            self._available[r] -= request[r]
            self._allocation[pid][r] += request[r]
            self._need[pid][r] -= request[r]

        # 檢查安全性
        if self._is_safe():
            return True
        else:
            # 回滾
            for r in request:
                self._available[r] += request[r]
                self._allocation[pid][r] -= request[r]
                self._need[pid][r] += request[r]
            return False

    def _is_safe(self) -> bool:
        """
        使用銀行家算法檢查系統是否處於安全狀態。

        Returns:
            是否安全
        """
        work = dict(self._available)
        finish = {pid: False for pid in self._allocation}

        while True:
            found = False
            for pid in self._allocation:
                if not finish[pid]:
                    can_finish = all(
                        self._need[pid].get(r, 0) <= work[r]
                        for r in self._total
                    )
                    if can_finish:
                        for r in self._total:
                            work[r] += self._allocation[pid][r]
                        finish[pid] = True
                        found = True
                        break

            if not found:
                break

        return all(finish.values())
