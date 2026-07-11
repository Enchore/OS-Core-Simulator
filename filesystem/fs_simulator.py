"""
Linux 檔案系統模擬器
完整模擬 Linux 檔案系統，包括目錄結構、使用者管理、權限操作與檔案指令。
"""
import os
import time
from typing import Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class FSNode:
    """檔案系統節點（文件或目錄）。"""
    name: str
    is_dir: bool = False
    content: str = ""
    children: Dict[str, 'FSNode'] = field(default_factory=dict)
    owner: str = "root"
    group: str = "root"
    permissions: str = "rwxr-xr-x"  # 默認權限
    created_at: float = field(default_factory=time.time)
    modified_at: float = field(default_factory=time.time)
    size: int = 0

    def __post_init__(self):
        if self.is_dir:
            self.children["."] = self
            self.children[".."] = self  # 將在掛載後更新


@dataclass
class User:
    """系統用戶。"""
    username: str
    password: str
    uid: int
    gid: int = 0
    home: str = "/home"


class FileSystemSimulator:
    """檔案系統模擬器。"""

    def __init__(self):
        """初始化檔案系統。"""
        self._users: Dict[str, User] = {}
        self._current_user: Optional[User] = None
        self._current_dir: FSNode = FSNode(name="/", is_dir=True)
        self._root = self._current_dir

        # 創建默認用戶
        self._create_default_users()
        self._create_default_structure()

    def _create_default_users(self):
        """創建默認用戶。"""
        self.add_user("root", "root", uid=0)
        self.add_user("user", "user", uid=1000)

    def _create_default_structure(self):
        """創建默認目錄結構。"""
        home = self._mkdir("/home")
        self._mkdir("/home/user")
        self._mkdir("/tmp")
        self._mkdir("/etc")
        self._mkdir("/var")

    def add_user(self, username: str, password: str, uid: int) -> bool:
        """添加用戶。"""
        if username in self._users:
            return False
        self._users[username] = User(
            username=username, password=password, uid=uid,
            home=f"/home/{username}"
        )
        return True

    def login(self, username: str, password: str) -> bool:
        """用戶登錄。"""
        user = self._users.get(username)
        if user and user.password == password:
            self._current_user = user
            self._current_dir = self._navigate_to("/home/" + username)
            if not self._current_dir:
                self._current_dir = self._root
            return True
        return False

    def ls(self, path: str = ".") -> List[str]:
        """列出目錄內容。"""
        target = self._resolve_path(path)
        if not target or not target.is_dir:
            return []
        return list(target.children.keys())

    def cd(self, path: str) -> bool:
        """切換目錄。"""
        target = self._resolve_path(path)
        if target and target.is_dir:
            self._current_dir = target
            return True
        return False

    def mkdir(self, name: str) -> bool:
        """創建目錄。"""
        if name in self._current_dir.children:
            return False
        self._current_dir.children[name] = FSNode(
            name=name, is_dir=True,
            owner=self._current_user.username if self._current_user else "root"
        )
        return True

    def touch(self, name: str) -> bool:
        """創建文件。"""
        if name in self._current_dir.children:
            return False
        self._current_dir.children[name] = FSNode(
            name=name, is_dir=False,
            owner=self._current_user.username if self._current_user else "root"
        )
        return True

    def cat(self, name: str) -> str:
        """查看文件內容。"""
        node = self._current_dir.children.get(name)
        if node and not node.is_dir:
            return node.content
        return f"cat: {name}: 沒有那個文件或目錄"

    def pwd(self) -> str:
        """顯示當前路徑。"""
        # TODO: 從當前節點反向構建路徑
        return "/"

    def chmod(self, name: str, permissions: str) -> bool:
        """修改文件權限。"""
        node = self._current_dir.children.get(name)
        if node:
            node.permissions = permissions
            return True
        return False

    def _mkdir(self, path: str) -> Optional[FSNode]:
        """內部方法：根據絕對路徑創建目錄。"""
        parts = [p for p in path.split("/") if p]
        current = self._root
        for part in parts:
            if part not in current.children:
                current.children[part] = FSNode(name=part, is_dir=True)
            current = current.children[part]
        return current

    def _resolve_path(self, path: str) -> Optional[FSNode]:
        """解析路徑。"""
        if path == "/":
            return self._root
        if path == "." or path == "":
            return self._current_dir
        if path == "..":
            return self._root  # 簡化處理

        parts = [p for p in path.split("/") if p]
        current = self._root if path.startswith("/") else self._current_dir

        for part in parts:
            if part in current.children:
                current = current.children[part]
            else:
                return None
        return current
