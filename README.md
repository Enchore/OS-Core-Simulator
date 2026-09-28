# OS-Core-Simulator — 作業系統核心機制模擬

[![CI](https://github.com/Enchore/OS-Core-Simulator/actions/workflows/ci.yml/badge.svg)](https://github.com/Enchore/OS-Core-Simulator/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> 作業系統核心機制模擬 | Operating System Core Mechanism Simulator

## 項目簡介

操作系統核心機制的教學向模擬實現，共 12 個模塊，覆蓋進程管理、記憶體分配、進程間通訊與檔案系統四大主題。Python 用於邏輯模擬，C 用於貼近真實系統調用的部分（pthread 同步、IPC 通訊）。

## 模塊清單

### 進程管理 `process/`

| 文件 | 內容 |
|------|------|
| `scheduler.py` | 進程調度算法：FCFS、SJF、Round Robin，含週轉時間／等待時間統計。**可直接運行** |
| `process_sim.py` | 進程狀態機（PCB）：創建、就緒、運行、阻塞、終止 |
| `deadlock.py` | 死鎖檢測：資源分配圖與環路檢測 |
| `producer_consumer.c` | pthread 生產者-消費者問題，含互斥鎖與條件變量。**需 gcc 編譯** |

### 記憶體管理 `memory/`

| 文件 | 內容 |
|------|------|
| `memory_allocator.py` | 640KB 記憶體分配模擬。**first_fit / best_fit / worst_fit 三種算法在同一文件內實現**，通過構造參數 `algorithm` 切換；含空閒塊合併與碎片整理 |

### 進程間通訊 `ipc/`

| 文件 | 內容 |
|------|------|
| `pipe_demo.py` | Linux 管道（pipe）通訊示例。**可直接運行** |
| `semaphore.py` | 信號量機制模擬：P/V 操作 |
| `rps_game.c` | 基於 IPC 的石頭剪刀布對戰遊戲。**需 gcc 編譯** |

### 檔案系統 `filesystem/`

| 文件 | 內容 |
|------|------|
| `fs_simulator.py` | 模擬 Linux 目錄樹結構 |
| `commands.py` | Shell 指令模擬：ls、cd、mkdir、touch、cat 等 |
| `permission.py` | 權限位模擬：chmod、chown |
| `user_manager.py` | Linux 使用者與群組管理 |

## 技術棧

| 類別 | 技術 |
|------|------|
| 系統編程 | C, pthread |
| 邏輯模擬 | Python 3 |
| IPC | Linux pipe |
| 構建工具 | Make, gcc |

## 快速開始

### 一鍵運行全部 Python 模塊

```bash
python main.py              # 依次演示全部模塊
python main.py --list       # 列出可用模塊
python main.py scheduler    # 只運行指定模塊
```

### 單獨運行可直接執行的模塊

```bash
python process/scheduler.py
python ipc/pipe_demo.py
```

### 編譯並運行 C 程序

```bash
make            # 編譯 process/producer_consumer 與 ipc/rps_game
./process/producer_consumer
./ipc/rps_game
make clean      # 清理編譯產物
```

## 使用示例

```python
from memory.memory_allocator import MemoryAllocator

# 切換分配算法：first_fit / best_fit / worst_fit
allocator = MemoryAllocator(algorithm="best_fit")
allocator.allocate("P1", 100)
allocator.allocate("P2", 240)
allocator.free("P1")
allocator.print_status()
```

```python
from process.scheduler import Process, fcfs, sjf, round_robin

procs = [Process("P1", arrival=0, burst=5), Process("P2", arrival=1, burst=3)]
print(fcfs(procs))
print(sjf(procs))
print(round_robin(procs, quantum=2))
```

## 項目結構

```
OS-Core-Simulator/
├── main.py                    # 統一演示入口
├── process/
│   ├── scheduler.py           # 調度算法（可執行）
│   ├── process_sim.py         # 進程狀態機
│   ├── deadlock.py            # 死鎖檢測
│   └── producer_consumer.c    # pthread 同步（需編譯）
├── memory/
│   └── memory_allocator.py    # 三種分配算法（同文件，參數切換）
├── ipc/
│   ├── pipe_demo.py           # 管道通訊（可執行）
│   ├── semaphore.py           # 信號量
│   └── rps_game.c             # IPC 對戰遊戲（需編譯）
├── filesystem/
│   ├── fs_simulator.py        # 目錄樹模擬
│   ├── commands.py            # Shell 指令
│   ├── permission.py          # 權限位
│   └── user_manager.py        # 用戶管理
└── Makefile
```

## 當前邊界

- 模塊總數為 **12 個**，非「30+」——本項目聚焦四大主題的核心機制，未覆蓋頁表置換、設備驅動、網絡協議棧等內容
- `ipc/` 目前僅實現**管道與信號量**，消息隊列與共享記憶體尚未實現
- 三種記憶體分配算法合併在 `memory_allocator.py` 單一文件內，非獨立文件
- `process_sim.py`、`deadlock.py`、`memory_allocator.py`、`semaphore.py`、`filesystem/*` 為庫形態，需 import 調用或通過 `main.py` 演示，本身無 `__main__` 入口
- 無單元測試與 CI

## 許可證

本項目基於 [MIT License](LICENSE) 開源。
