# OS-Core-Simulator Makefile
# 用於編譯 C 語言實現的作業系統模擬程序

CC = gcc
CFLAGS = -Wall -pthread -g
PREFIX = .

.PHONY: all clean process ipc

all: process ipc

# 進程管理模塊
process:
	$(CC) $(CFLAGS) process/producer_consumer.c -o $(PREFIX)/process/producer_consumer

# 進程間通訊模塊
ipc:
	$(CC) $(CFLAGS) ipc/rps_game.c -o $(PREFIX)/ipc/rps_game

clean:
	rm -f $(PREFIX)/process/producer_consumer $(PREFIX)/ipc/rps_game
	rm -f $(PREFIX)/**/*.o
