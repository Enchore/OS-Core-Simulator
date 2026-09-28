#!/usr/bin/env python3
"""
OS-Core-Simulator 統一演示入口

用法：
    python main.py              依次演示全部模塊
    python main.py --list       列出所有可用模塊
    python main.py scheduler    只運行指定模塊（可多個）

說明：
    部分模塊（process_sim / deadlock / memory_allocator / semaphore /
    filesystem/*）本身為庫形態、無 __main__ 入口，需通過本文件演示。
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def _title(text):
    """打印模塊標題分隔線。"""
    print("\n" + "=" * 62)
    print(f"  {text}")
    print("=" * 62)


def demo_scheduler():
    """進程調度算法：FCFS / SJF / Round Robin。"""
    from process.scheduler import Process, fcfs, sjf, round_robin

    _title("進程調度算法（FCFS / SJF / RR）")

    procs = [
        Process(name="P1", arrival_time=0, burst_time=5),
        Process(name="P2", arrival_time=1, burst_time=3),
        Process(name="P3", arrival_time=2, burst_time=8),
        Process(name="P4", arrival_time=3, burst_time=6),
    ]

    for algo_name, algo in (("FCFS 先來先服務", fcfs),
                            ("SJF 最短作業優先", sjf)):
        result = algo([Process(p.name, p.arrival_time, p.burst_time)
                       for p in procs])
        print(f"\n--- {algo_name} ---")
        _print_schedule(result)

    result = round_robin([Process(p.name, p.arrival_time, p.burst_time)
                          for p in procs], quantum=3)
    print("\n--- Round Robin 時間片輪轉（quantum=3）---")
    _print_schedule(result)


def _print_schedule(result):
    """打印調度結果，兼容 dict 與含進程列表的返回值。"""
    if not isinstance(result, dict):
        print(result)
        return
    for key in ("average_waiting_time", "avg_waiting_time",
                "average_turnaround_time", "avg_turnaround_time"):
        if key in result:
            print(f"  {key}: {result[key]}")
    procs = result.get("processes") or result.get("results") or []
    for p in procs:
        name = getattr(p, "name", p.get("name", "?"))
        wt = getattr(p, "waiting_time", p.get("waiting_time"))
        tt = getattr(p, "turnaround_time", p.get("turnaround_time"))
        print(f"    {name}: 等待={wt} 週轉={tt}")
    if not procs:
        for key, value in result.items():
            if key not in ("average_waiting_time", "avg_waiting_time",
                           "average_turnaround_time", "avg_turnaround_time"):
                print(f"  {key}: {value}")


def demo_process():
    """進程生命週期與狀態機。"""
    from process.process_sim import ProcessSimulator

    _title("進程狀態機（PCB 生命週期）")

    sim = ProcessSimulator()
    p1 = sim.create_process("init", burst_time=5, priority=1)
    p2 = sim.create_process("bash", burst_time=3)
    p3 = sim.create_process("worker", burst_time=7, priority=2)

    print(f"已創建 3 個進程，PID: {p1.pid}, {p2.pid}, {p3.pid}")
    print("\n當前進程列表：")
    for pcb in sim.list_processes():
        print(f"  PID {pcb.pid:>3} | {pcb.name:<8} | 狀態: {pcb.state}")

    sim.terminate_process(p2.pid)
    print(f"\n終止 PID {p2.pid} 後剩餘進程：")
    for pcb in sim.list_processes():
        print(f"  PID {pcb.pid:>3} | {pcb.name:<8} | 狀態: {pcb.state}")


def demo_deadlock():
    """銀行家算法死鎖檢測。"""
    from process.deadlock import DeadlockDetector

    _title("死鎖檢測（銀行家算法）")

    detector = DeadlockDetector(total_resources={"A": 10, "B": 5, "C": 7})
    detector.add_process("P0", max_need={"A": 7, "B": 5, "C": 3})
    detector.add_process("P1", max_need={"A": 3, "B": 2, "C": 2})
    detector.add_process("P2", max_need={"A": 9, "B": 0, "C": 2})

    print("系統總資源: A=10, B=5, C=7")
    print("進程最大需求: P0=(7,5,3)  P1=(3,2,2)  P2=(9,0,2)\n")

    for req, proc in (({"A": 2, "B": 1, "C": 1}, "P0"),
                      ({"A": 2, "B": 0, "C": 0}, "P1"),
                      ({"A": 3, "B": 0, "C": 2}, "P2")):
        ok = detector.allocate(proc, req)
        verdict = "分配成功（系統安全）" if ok else "分配被拒絕（會導致不安全狀態）"
        print(f"  {proc} 請求 {req} → {verdict}")


def demo_memory():
    """三種記憶體分配算法對比。"""
    from memory.memory_allocator import MemoryAllocator

    _title("記憶體分配（first_fit / best_fit / worst_fit）")

    print(f"總記憶體: {MemoryAllocator.TOTAL_MEMORY} KB\n")

    for algo in ("first_fit", "best_fit", "worst_fit"):
        print(f"\n----- 算法: {algo} -----")
        allocator = MemoryAllocator(algorithm=algo)
        for pid, size in (("P1", 120), ("P2", 60), ("P3", 200)):
            addr = allocator.allocate(pid, size)
            if addr is None:
                print(f"  為 {pid} 分配 {size}KB → 失敗（空間不足）")
            else:
                print(f"  為 {pid} 分配 {size}KB → 起始地址 {addr}KB")
        allocator.free("P2")
        print(f"  釋放 P2")
        addr = allocator.allocate("P4", 40)
        print(f"  為 P4 分配 40KB → {'地址 ' + str(addr) + 'KB' if addr is not None else '失敗'}")
        allocator.print_status()


def demo_semaphore():
    """信號量 P/V 操作。"""
    from ipc.semaphore import SimpleSemaphore

    _title("信號量機制（P/V 操作）")

    sem = SimpleSemaphore(initial_value=2)
    print(f"初始值: {sem.value}\n")

    print("執行 P 操作 x2：")
    sem.wait()
    sem.wait()
    print(f"\n當前值: {sem.value}")

    print("\n執行 V 操作：")
    sem.signal()
    print(f"當前值: {sem.value}")

    print("\n再執行 P 操作：")
    sem.wait()
    print(f"當前值: {sem.value}")

    print("\n說明：wait() 在值 <= 0 時會真實阻塞線程，"
          "本演示中 P/V 操作配對執行，不會發生死鎖。")


def demo_filesystem():
    """檔案系統模擬與 Shell 指令。"""
    from filesystem.fs_simulator import FileSystemSimulator
    from filesystem.commands import ShellCommands

    _title("檔案系統模擬與 Shell 指令")

    fs = FileSystemSimulator()
    if not fs.login("root", "root"):
        print("登入失敗，使用未登入狀態繼續演示")
    else:
        print("已登入為 root")

    shell = ShellCommands(fs)
    commands = [
        "pwd",
        "ls",
        "mkdir demo",
        "cd demo",
        "touch hello.txt",
        "echo hello os",
        "ls",
        "cd /",
        "ls",
        "whoami",
        "help",
    ]

    for cmd in commands:
        print(f"\n$ {cmd}")
        try:
            output = shell.execute(cmd)
            if output:
                print(output)
        except Exception as exc:
            print(f"  （執行異常: {exc}）")


def demo_permission():
    """權限位模擬。"""
    from filesystem.permission import Permission

    _title("檔案權限位（chmod / 權限檢查）")

    for perm_str in ("rwxr-xr-x", "rw-r--r--", "rwxrwxrwx", "---------"):
        perm = Permission(perm_str)
        print(f"  {perm_str}  →  權限數字 {perm.to_octal():<4} "
              f"回讀: {perm.to_string()}")

    print("\nchmod 修改演示：")
    perm = Permission("rw-r--r--")
    print(f"  原始: {perm.to_string()} → {perm.to_octal()}")
    perm.chmod("755")
    print(f"  chmod 755 後: {perm.to_string()} → {perm.to_octal()}")
    perm.chmod("600")
    print(f"  chmod 600 後: {perm.to_string()} → {perm.to_octal()}")


def demo_user():
    """Linux 使用者管理。"""
    from filesystem.user_manager import UserManager

    _title("Linux 使用者管理")

    um = UserManager()
    um.add_user("alice", "alice123", uid=1001)
    um.add_user("bob", "bob456", uid=1002)

    print("使用者列表：")
    for user in um.list_users():
        groups = ",".join(getattr(user, "groups", [])) or "-"
        print(f"  uid={getattr(user, 'uid', '?'):<5} "
              f"{getattr(user, 'username', '?'):<10} "
              f"home={getattr(user, 'home', '-'):<15} groups={groups}")

    print("\n加入群組：")
    um.add_to_group("alice", "sudo")
    alice = um.get_user("alice")
    if alice:
        print(f"  alice 群組: {','.join(getattr(alice, 'groups', []))}")

    print("\n修改密碼：")
    ok = um.change_password("bob", "newpass789")
    print(f"  bob 改密: {'成功' if ok else '失敗'}")

    print("\n刪除使用者：")
    ok = um.delete_user("bob")
    print(f"  刪除 bob: {'成功' if ok else '失敗'}")
    print(f"  剩餘使用者: {[u.username for u in um.list_users()]}")


DEMOS = {
    "scheduler": demo_scheduler,
    "process": demo_process,
    "deadlock": demo_deadlock,
    "memory": demo_memory,
    "semaphore": demo_semaphore,
    "filesystem": demo_filesystem,
    "permission": demo_permission,
    "user": demo_user,
}


def main():
    """命令行入口。"""
    args = sys.argv[1:]

    if args and args[0] in ("--list", "-l"):
        print("可用模塊：")
        for name in DEMOS:
            print(f"  {name:<12} {DEMOS[name].__doc__}")
        print("\n用法: python main.py [模塊名 ...]")
        return 0

    targets = [a for a in args if a in DEMOS]
    if not targets:
        targets = list(DEMOS)

    print(f"OS-Core-Simulator — 即將演示 {len(targets)} 個模塊: "
          f"{', '.join(targets)}")

    failed = []
    for name in targets:
        try:
            DEMOS[name]()
        except Exception as exc:
            failed.append(name)
            print(f"\n[模塊 {name} 執行失敗] {type(exc).__name__}: {exc}")

    print("\n" + "=" * 62)
    if failed:
        print(f"演示結束，{len(failed)} 個模塊異常: {', '.join(failed)}")
        return 1
    print(f"演示結束，{len(targets)} 個模塊全部執行完成。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
