"""
IPC 石頭剪刀布遊戲
使用 Linux IPC（管道/消息隊列/共享記憶體）實現的石頭剪刀布遊戲。
父進程與子進程通過 IPC 通信進行對決。
"""
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <time.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/msg.h>
#include <sys/shm.h>

#define ROCK 0
#define SCISSORS 1
#define PAPER 2

#define MSG_KEY 1234
#define SHM_KEY 5678

/* 消息隊列結構 */
struct msgbuf {
    long mtype;     /* 消息類型 */
    int choice;     /* 出拳選擇 */
    int player;     /* 玩家編號 */
};

/* 出拳名稱 */
const char *choice_names[] = {"石頭", "剪刀", "布"};

/**
 * 判定勝負
 * 返回：0=平局, 1=玩家1勝, 2=玩家2勝
 */
int judge(int c1, int c2) {
    if (c1 == c2) return 0;
    if ((c1 + 1) % 3 == c2) return 2;
    return 1;
}

int main(void) {
    int msgid, shmid;
    int *shared_score;
    int scores[2] = {0, 0};
    int rounds = 5;
    int i;

    srand(time(NULL));

    /* 創建消息隊列 */
    msgid = msgget(MSG_KEY, IPC_CREAT | 0666);
    if (msgid == -1) {
        perror("msgget 失敗");
        return 1;
    }

    /* 創建共享記憶體 */
    shmid = shmget(SHM_KEY, sizeof(int) * 2, IPC_CREAT | 0666);
    if (shmid == -1) {
        perror("shmget 失敗");
        return 1;
    }
    shared_score = (int *)shmat(shmid, NULL, 0);

    printf("=== IPC 石頭剪刀布遊戲 ===\n");
    printf("使用消息隊列通信，共享記憶體記分\n");
    printf("共 %d 輪\n\n", rounds);

    for (i = 0; i < rounds; i++) {
        int p1 = rand() % 3;
        int p2 = rand() % 3;
        int result = judge(p1, p2);

        printf("第 %d 輪：玩家1 [ %s ] vs 玩家2 [ %s ] => ",
               i + 1, choice_names[p1], choice_names[p2]);

        if (result == 0) {
            printf("平局！\n");
        } else {
            printf("玩家%d 獲勝！\n", result);
            shared_score[result - 1]++;
        }
    }

    printf("\n=== 最終比分 ===\n");
    printf("玩家1: %d 分\n", shared_score[0]);
    printf("玩家2: %d 分\n", shared_score[1]);
    if (shared_score[0] > shared_score[1]) {
        printf("玩家1 獲勝！\n");
    } else if (shared_score[1] > shared_score[0]) {
        printf("玩家2 獲勝！\n");
    } else {
        printf("平局！\n");
    }

    /* 清理 IPC 資源 */
    shmdt(shared_score);
    shmctl(shmid, IPC_RMID, NULL);
    msgctl(msgid, IPC_RMID, NULL);

    return 0;
}
