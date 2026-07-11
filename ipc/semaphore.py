"""
信號量實現模組
Python 實現的信號量機制，用於進程同步。
"""
from threading import Semaphore, Lock
from typing import Optional


class SimpleSemaphore:
    """
    簡易信號量實現。
    模擬 Linux sem_t 信號量的基本功能。
    """

    def __init__(self, initial_value: int = 1):
        """
        初始化信號量。

        Args:
            initial_value: 信號量初始值
        """
        self._value = initial_value
        self._lock = Lock()
        self._sem = Semaphore(initial_value)

    def wait(self):
        """P 操作（等待/申請資源）。"""
        with self._lock:
            if self._value <= 0:
                print(f"[信號量] 進程阻塞（當前值: {self._value}）")
            self._value -= 1
        self._sem.acquire()
        print(f"[信號量] P 操作完成（剩餘: {self._value}）")

    def signal(self):
        """V 操作（釋放資源）。"""
        self._sem.release()
        with self._lock:
            self._value += 1
        print(f"[信號量] V 操作完成（剩餘: {self._value}）")

    @property
    def value(self) -> int:
        """獲取當前信號量值。"""
        return self._value
