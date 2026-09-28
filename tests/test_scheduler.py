"""进程调度算法测试。

期望值均按课本公式手算得出，不是照抄实现输出。
"""
import pytest

from conftest import load

scheduler = load("scheduler", "process/scheduler.py")

Process = scheduler.Process


@pytest.fixture
def textbook_processes():
    # 注意：调度函数会就地修改 Process 对象，每次用例都要新建
    return [Process("P1", 0, 6), Process("P2", 1, 4),
            Process("P3", 2, 8), Process("P4", 3, 2)]


def test_fcfs_follows_arrival_order_and_matches_hand_calculation(textbook_processes):
    result = scheduler.fcfs(textbook_processes)

    assert [item["name"] for item in result["schedule"]] == ["P1", "P2", "P3", "P4"]
    # 手算：等待时间 0,5,8,15；周转时间 6,9,16,17
    assert [item["wt"] for item in result["schedule"]] == [0, 5, 8, 15]
    assert [item["ct"] for item in result["schedule"]] == [6, 10, 18, 20]
    assert result["avg_waiting"] == pytest.approx(7.0)
    assert result["avg_turnaround"] == pytest.approx(12.0)


def test_sjf_runs_shortest_first_when_all_arrive_together():
    processes = [Process("P1", 0, 6), Process("P2", 0, 4),
                 Process("P3", 0, 8), Process("P4", 0, 2)]

    result = scheduler.sjf(processes)

    assert [item["name"] for item in result["schedule"]] == ["P4", "P2", "P1", "P3"]
    # 手算：等待时间 0,2,6,12；周转时间 2,6,12,20
    assert [item["wt"] for item in result["schedule"]] == [0, 2, 6, 12]
    assert result["avg_waiting"] == pytest.approx(5.0)
    assert result["avg_turnaround"] == pytest.approx(10.0)


def test_sjf_never_worse_than_fcfs_on_average_waiting():
    base = [("P1", 0, 6), ("P2", 1, 4), ("P3", 2, 8), ("P4", 3, 2)]

    fcfs = scheduler.fcfs([Process(*p) for p in base])
    sjf = scheduler.sjf([Process(*p) for p in base])

    assert sjf["avg_waiting"] <= fcfs["avg_waiting"]


def test_round_robin_rotates_by_quantum_and_completes_everyone():
    processes = [Process("P1", 0, 6), Process("P2", 0, 4),
                 Process("P3", 0, 8), Process("P4", 0, 2)]

    result = scheduler.round_robin(processes, quantum=2)

    assert len(result["schedule"]) == 4
    # quantum=2 时，短作业 P4 先跑完，长作业被反复挂回队尾
    assert [item["name"] for item in result["schedule"]] == ["P4", "P2", "P1", "P3"]
    # 时间轴：0-2 P1 / 2-4 P2 / 4-6 P3 / 6-8 P4(完成) / 8-10 P1 / 10-12 P2(完成)
    #        / 12-14 P3 / 14-16 P1(完成) / 16-18 P3 / 18-20 P3(完成)
    # 手算：完成时间 8,12,16,20；等待时间 6,8,10,12；周转时间 8,12,16,20
    assert [item["ct"] for item in result["schedule"]] == [8, 12, 16, 20]
    assert result["avg_waiting"] == pytest.approx(9.0)
    assert result["avg_turnaround"] == pytest.approx(14.0)


def test_empty_process_list_returns_zeroed_stats():
    for algorithm in (scheduler.fcfs, scheduler.sjf, scheduler.round_robin):
        result = algorithm([])

        assert result["avg_waiting"] == 0
        assert result["avg_turnaround"] == 0
        assert result["schedule"] == []
