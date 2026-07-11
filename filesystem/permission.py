"""
權限管理模組
模擬 Linux 檔案權限系統（rwx）。
"""
from typing import Optional


class Permission:
    """Linux 檔案權限。"""

    # 權限位掩碼
    READ = 4
    WRITE = 2
    EXECUTE = 1

    # 角色掩碼
    OWNER = 0
    GROUP = 1
    OTHERS = 2

    def __init__(self, perm_str: str = "rwxr-xr-x"):
        """
        初始化權限。

        Args:
            perm_str: 權限字符串，如 "rwxr-xr-x"
        """
        self._permissions = self._parse(perm_str)

    def _parse(self, perm_str: str) -> list:
        """
        解析權限字符串。

        Args:
            perm_str: 9 位權限字符串

        Returns:
            三元組列表 [(owner_perm, group_perm, others_perm)]
        """
        perms = []
        for role in range(3):
            segment = perm_str[role * 3: role * 3 + 3]
            perm = 0
            perm += self.READ if 'r' in segment else 0
            perm += self.WRITE if 'w' in segment else 0
            perm += self.EXECUTE if 'x' in segment else 0
            perms.append(perm)
        return perms

    def to_string(self) -> str:
        """轉換為權限字符串。"""
        result = ""
        for perm in self._permissions:
            result += "r" if perm & self.READ else "-"
            result += "w" if perm & self.WRITE else "-"
            result += "x" if perm & self.EXECUTE else "-"
        return result

    def to_octal(self) -> int:
        """轉換為八進制表示（如 755）。"""
        return (self._permissions[0] * 100 +
                self._permissions[1] * 10 +
                self._permissions[2])

    def check(self, role: int, permission: int) -> bool:
        """
        檢查指定角色是否擁有指定權限。

        Args:
            role: 角色 (OWNER/GROUP/OTHERS)
            permission: 權限 (READ/WRITE/EXECUTE)

        Returns:
            是否有權限
        """
        return bool(self._permissions[role] & permission)

    def set_permission(self, role: int, perm: int):
        """
        設置權限。

        Args:
            role: 角色
            perm: 權限值 (0-7)
        """
        self._permissions[role] = perm

    def chmod(self, mode: str):
        """
        修改權限。

        Args:
            mode: 權限模式，支持 "755" 或 "u+x" 格式
        """
        if mode.isdigit() and len(mode) == 3:
            # 八進制模式 (如 755)
            self._permissions[0] = int(mode[0])
            self._permissions[1] = int(mode[1])
            self._permissions[2] = int(mode[2])
