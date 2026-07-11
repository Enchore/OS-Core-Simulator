"""
管道通信示例
使用 Python 模擬 Linux 管道通信。
"""
import os
from typing import Optional


def pipe_demo():
    """
    演示管道通信。
    父進程向子進程通過管道發送數據。
    """
    read_fd, write_fd = os.pipe()

    pid = os.fork()
    if pid == 0:
        # 子進程：讀取數據
        os.close(write_fd)
        data = os.read(read_fd, 1024).decode()
        print(f"[子進程] 收到: {data}")
        os.close(read_fd)
    else:
        # 父進程：發送數據
        os.close(read_fd)
        message = "Hello from parent process via pipe!"
        os.write(write_fd, message.encode())
        os.close(write_fd)
        os.waitpid(pid, 0)
        print("[父進程] 數據已發送")


if __name__ == "__main__":
    pipe_demo()
