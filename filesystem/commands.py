"""
檔案系統指令模組
模擬常用 Linux 檔案系統指令的 Python 實現。
"""
from typing import Optional


class ShellCommands:
    """檔案系統指令集合。"""

    def __init__(self, fs):
        """
        初始化指令集。

        Args:
            fs: FileSystemSimulator 實例
        """
        self._fs = fs

    def execute(self, command: str) -> str:
        """
        執行 Shell 指令。

        Args:
            command: 指令字符串

        Returns:
            執行結果
        """
        parts = command.strip().split()
        if not parts:
            return ""

        cmd = parts[0]
        args = parts[1:]

        # 指令映射
        commands = {
            "ls": self._ls,
            "cd": self._cd,
            "pwd": self._pwd,
            "mkdir": self._mkdir,
            "touch": self._touch,
            "cat": self._cat,
            "rm": self._rm,
            "echo": self._echo,
            "chmod": self._chmod,
            "whoami": self._whoami,
            "help": self._help,
        }

        handler = commands.get(cmd)
        if handler:
            return handler(args)
        return f"命令未找到: {cmd}"

    def _ls(self, args: list) -> str:
        path = args[0] if args else "."
        items = self._fs.ls(path)
        return "  ".join(items) if items else "(空目錄)"

    def _cd(self, args: list) -> str:
        if not args:
            return "cd: 缺少參數"
        path = args[0]
        if self._fs.cd(path):
            return ""
        return f"cd: {path}: 不是一個目錄"

    def _pwd(self, args: list) -> str:
        return self._fs.pwd()

    def _mkdir(self, args: list) -> str:
        if not args:
            return "mkdir: 缺少參數"
        if self._fs.mkdir(args[0]):
            return ""
        return f"mkdir: 無法創建目錄 '{args[0]}'"

    def _touch(self, args: list) -> str:
        if not args:
            return "touch: 缺少參數"
        if self._fs.touch(args[0]):
            return ""
        return f"touch: 無法創建文件 '{args[0]}'"

    def _cat(self, args: list) -> str:
        if not args:
            return "cat: 缺少參數"
        return self._fs.cat(args[0])

    def _rm(self, args: list) -> str:
        return f"rm: 功能未實現"  # TODO: 實現 rm

    def _echo(self, args: list) -> str:
        return " ".join(args)

    def _chmod(self, args: list) -> str:
        if len(args) < 2:
            return "chmod: 缺少參數"
        if self._fs.chmod(args[1], args[0]):
            return ""
        return f"chmod: 無法修改 '{args[1]}' 的權限"

    def _whoami(self, args: list) -> str:
        return "root"  # TODO: 從 fs 獲取當前用戶

    def _help(self, args: list) -> str:
        return (
            "可用命令: ls, cd, pwd, mkdir, touch, cat, "
            "rm, echo, chmod, whoami, help"
        )
