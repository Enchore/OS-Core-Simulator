"""
640KB 記憶體分配系統
模擬 640KB 傳統記憶體分配，支持首次適配、最佳適配、最壞適配等算法。
"""
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class MemoryBlock:
    """記憶體塊。"""
    start: int
    size: int
    pid: Optional[str] = None  # None 表示空閒塊

    @property
    def is_free(self) -> bool:
        """是否為空閒塊。"""
        return self.pid is None

    @property
    def end(self) -> int:
        """結束地址。"""
        return self.start + self.size


class MemoryAllocator:
    """
    640KB 記憶體分配器。
    支持多種分配算法。
    """

    TOTAL_MEMORY = 640  # 640 KB

    def __init__(self, algorithm: str = "first_fit"):
        """
        初始化記憶體分配器。

        Args:
            algorithm: 分配算法 (first_fit / best_fit / worst_fit)
        """
        self._algorithm = algorithm
        self._blocks: List[MemoryBlock] = [
            MemoryBlock(start=0, size=self.TOTAL_MEMORY, pid=None)
        ]

    def allocate(self, pid: str, size: int) -> Optional[int]:
        """
        分配記憶體。

        Args:
            pid: 進程 ID
            size: 需要的大小 (KB)

        Returns:
            分配的起始地址，分配失敗返回 None
        """
        if size <= 0:
            return None

        free_blocks = [b for b in self._blocks if b.is_free and b.size >= size]

        if not free_blocks:
            print(f"[記憶體] 無法為進程 {pid} 分配 {size}KB：空間不足")
            return None

        # 根據算法選擇空閒塊
        if self._algorithm == "first_fit":
            block = free_blocks[0]
        elif self._algorithm == "best_fit":
            block = min(free_blocks, key=lambda b: b.size)
        elif self._algorithm == "worst_fit":
            block = max(free_blocks, key=lambda b: b.size)
        else:
            block = free_blocks[0]

        # 執行分配
        idx = self._blocks.index(block)
        if block.size > size:
            # 分割塊
            self._blocks.insert(idx + 1, MemoryBlock(
                start=block.start + size,
                size=block.size - size,
                pid=None
            ))
        block.size = size
        block.pid = pid

        print(f"[記憶體] 為進程 {pid} 分配 {size}KB @ {block.start}KB ({self._algorithm})")
        return block.start

    def free(self, pid: str) -> bool:
        """
        釋放進程佔用的記憶體。

        Args:
            pid: 進程 ID

        Returns:
            是否成功釋放
        """
        freed = False
        for block in self._blocks:
            if block.pid == pid:
                block.pid = None
                freed = True
                print(f"[記憶體] 釋放進程 {pid} 的 {block.size}KB")

        if freed:
            self._merge_free_blocks()
        return freed

    def _merge_free_blocks(self):
        """合併相鄰的空閒塊。"""
        i = 0
        while i < len(self._blocks) - 1:
            if self._blocks[i].is_free and self._blocks[i + 1].is_free:
                self._blocks[i].size += self._blocks[i + 1].size
                self._blocks.pop(i + 1)
            else:
                i += 1

    def get_status(self) -> dict:
        """獲取記憶體使用狀態。"""
        used = sum(b.size for b in self._blocks if not b.is_free)
        free = self.TOTAL_MEMORY - used
        fragments = sum(1 for b in self._blocks if b.is_free)

        return {
            "total": self.TOTAL_MEMORY,
            "used": used,
            "free": free,
            "usage_percent": round(used / self.TOTAL_MEMORY * 100, 2),
            "fragments": fragments,
            "algorithm": self._algorithm,
            "blocks": [
                {"start": b.start, "size": b.size, "pid": b.pid}
                for b in self._blocks
            ]
        }

    def print_status(self):
        """打印記憶體狀態。"""
        status = self.get_status()
        print(f"\n=== 記憶體狀態 ({status['algorithm']}) ===")
        print(f"總計: {status['total']}KB | "
              f"已用: {status['used']}KB | "
              f"空閒: {status['free']}KB | "
              f"使用率: {status['usage_percent']}%")
        print(f"碎片數: {status['fragments']}")
        print("-" * 40)
        for b in self._blocks:
            state = "空閒" if b.is_free else f"[{b.pid}]"
            print(f"  {b.start:3d}KB - {b.end:3d}KB ({b.size:3d}KB) {state}")
