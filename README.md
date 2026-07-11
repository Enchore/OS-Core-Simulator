# OS-Core-Simulator — 作業系統核心機制模擬

> 作業系統核心機制模擬 | Operating System Core Mechanism Simulator

## 項目簡介

30+ 個作業系統核心概念的 Python/C 實現，涵蓋進程管理、記憶體分配、同步機制與檔案系統模擬。pthread 生產者-消費者問題進程同步、640KB 記憶體分配系統（多種演算法）、Linux IPC 進程間通訊（石頭剪刀布遊戲）、完整模擬 Linux 使用者管理、權限操作、目錄結構與檔案系統指令。

## 功能模塊

### 進程管理 (`process/`)
- 進程創建與終止模擬
- pthread 生產者-消費者問題
- 進程調度算法（FCFS、SJF、RR）
- 死鎖檢測與預防

### 記憶體管理 (`memory/`)
- 640KB 記憶體分配系統
- 首次適配算法（First Fit）
- 最佳適配算法（Best Fit）
- 最壞適配算法（Worst Fit）
- 記憶體碎片整理

### 進程間通訊 (`ipc/`)
- Linux IPC（管道、消息隊列、共享記憶體）
- 基於 IPC 的石頭剪刀布遊戲
- 信號量機制

### 檔案系統 (`filesystem/`)
- 模擬 Linux 目錄結構
- 使用者管理
- 權限操作（chmod、chown）
- 檔案系統指令（ls、cd、mkdir、touch、cat 等）

## 技術棧

| 類別 | 技術 |
|------|------|
| 系統編程 | C, pthread |
| 腳本模擬 | Python |
| IPC | Linux IPC (pipe, msg queue, shared memory) |
| 構建工具 | Make, Bash |

## 項目結構

```
OS-Core-Simulator/
├── process/                   # 進程管理
│   ├── process_sim.py         # 進程模擬 (Python)
│   ├── producer_consumer.c   # 生產者-消費者 (C/pthread)
│   ├── scheduler.py          # 進程調度算法
│   └── deadlock.py           # 死鎖檢測
├── memory/                    # 記憶體管理
│   ├── memory_allocator.py   # 記憶體分配系統
│   ├── first_fit.py          # 首次適配算法
│   ├── best_fit.py           # 最佳適配算法
│   └── worst_fit.py          # 最壞適配算法
├── ipc/                       # 進程間通訊
│   ├── rps_game.c            # 石頭剪刀布 IPC 遊戲 (C)
│   ├── pipe_demo.py          # 管道通信示例
│   └── semaphore.py          # 信號量實現
├── filesystem/                # 檔案系統模擬
│   ├── fs_simulator.py       # 檔案系統核心
│   ├── user_manager.py       # 使用者管理
│   ├── permission.py         # 權限管理
│   └── commands.py          # 檔案系統指令
├── Makefile                   # 構建腳本
├── README.md
├── .gitignore
└── LICENSE
```

## 快速開始

### Python 模擬

```bash
# 記憶體分配模擬
python memory/memory_allocator.py

# 進程調度模擬
python process/scheduler.py

# 檔案系統模擬
python filesystem/fs_simulator.py
```

### C 程序（需要 Linux 環境）

```bash
make all

# 生產者-消費者
./process/producer_consumer

# 石頭剪刀布 IPC 遊戲
./ipc/rps_game
```

## 貢獻

歡迎提交 Issue 和 Pull Request。

## 許可證

本項目基於 [MIT License](LICENSE) 開源。
