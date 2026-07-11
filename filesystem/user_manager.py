"""
使用者管理模組
模擬 Linux 用戶的添加、刪除、查詢等功能。
"""
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class LinuxUser:
    """Linux 用戶數據。"""
    username: str
    password: str
    uid: int
    gid: int = 0
    home: str = ""
    shell: str = "/bin/bash"
    groups: List[str] = None

    def __post_init__(self):
        if self.home == "":
            self.home = f"/home/{self.username}"
        if self.groups is None:
            self.groups = []


class UserManager:
    """Linux 用戶管理器。"""

    def __init__(self):
        """初始化用戶管理器。"""
        self._users: Dict[str, LinuxUser] = {}
        self._groups: Dict[str, List[str]] = {}
        self._next_uid = 1000

        # 創建 root 用戶
        self.add_user("root", "", uid=0, gid=0)

    def add_user(self, username: str, password: str, uid: Optional[int] = None,
                 gid: int = 0, groups: Optional[List[str]] = None) -> LinuxUser:
        """
        添加新用戶。

        Args:
            username: 用戶名
            password: 密碼
            uid: 用戶 ID（可選，自動分配）
            gid: 主組 ID
            groups: 附加組列表

        Returns:
            創建的用戶對象
        """
        if username in self._users:
            raise ValueError(f"用戶 {username} 已存在")

        if uid is None:
            uid = self._next_uid
            self._next_uid += 1

        user = LinuxUser(
            username=username,
            password=password,
            uid=uid,
            gid=gid,
            groups=groups or []
        )
        self._users[username] = user

        # 添加到組
        group_name = str(gid)
        if group_name not in self._groups:
            self._groups[group_name] = []
        self._groups[group_name].append(username)

        for g in user.groups:
            if g not in self._groups:
                self._groups[g] = []
            self._groups[g].append(username)

        return user

    def delete_user(self, username: str) -> bool:
        """
        刪除用戶。

        Args:
            username: 用戶名

        Returns:
            是否成功刪除
        """
        if username not in self._users:
            return False

        if username == "root":
            raise ValueError("不能刪除 root 用戶")

        del self._users[username]
        return True

    def get_user(self, username: str) -> Optional[LinuxUser]:
        """獲取用戶信息。"""
        return self._users.get(username)

    def list_users(self) -> List[LinuxUser]:
        """列出所有用戶。"""
        return list(self._users.values())

    def change_password(self, username: str, new_password: str) -> bool:
        """修改用戶密碼。"""
        user = self._users.get(username)
        if user:
            user.password = new_password
            return True
        return False

    def add_to_group(self, username: str, group_name: str) -> bool:
        """將用戶添加到組。"""
        user = self._users.get(username)
        if user and group_name not in user.groups:
            user.groups.append(group_name)
            if group_name not in self._groups:
                self._groups[group_name] = []
            self._groups[group_name].append(username)
            return True
        return False
