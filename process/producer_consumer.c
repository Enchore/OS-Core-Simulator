/**
 * 生產者-消費者問題
 * 使用 pthread 和信號量實現經典的生產者-消費者進程同步問題。
 *
 * 編譯：gcc -Wall -pthread -o producer_consumer producer_consumer.c
 * 運行：./producer_consumer
 */
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <semaphore.h>
#include <unistd.h>

#define BUFFER_SIZE 5      /* 緩衝區大小 */
#define PRODUCER_COUNT 2   /* 生產者數量 */
#define CONSUMER_COUNT 2   /* 消費者數量 */
#define ITEM_COUNT 20      /* 生產總數量 */

/* 共享緩衝區 */
int buffer[BUFFER_SIZE];
int in_idx = 0;   /* 生產者放入位置 */
int out_idx = 0;  /* 消費者取出位置 */

/* 信號量 */
sem_t empty;       /* 空位數量 */
sem_t full;        /* 已有產品數量 */
pthread_mutex_t mutex; /* 互斥鎖 */

/**
 * 生產者線程函數
 * 生產產品並放入緩衝區
 */
void *producer(void *arg) {
    int id = *(int *)arg;
    for (int i = 0; i < ITEM_COUNT / PRODUCER_COUNT; i++) {
        int item = rand() % 100;

        /* 等待空位 */
        sem_wait(&empty);
        pthread_mutex_lock(&mutex);

        /* 放入緩衝區 */
        buffer[in_idx] = item;
        printf("生產者 %d: 生產了產品 %d [位置 %d]\n", id, item, in_idx);
        in_idx = (in_idx + 1) % BUFFER_SIZE;

        pthread_mutex_unlock(&mutex);
        sem_post(&full);

        usleep(rand() % 500000); /* 模擬生產耗時 */
    }
    return NULL;
}

/**
 * 消費者線程函數
 * 從緩衝區取出產品並消費
 */
void *consumer(void *arg) {
    int id = *(int *)arg;
    for (int i = 0; i < ITEM_COUNT / CONSUMER_COUNT; i++) {
        /* 等待產品 */
        sem_wait(&full);
        pthread_mutex_lock(&mutex);

        /* 從緩衝區取出 */
        int item = buffer[out_idx];
        printf("消費者 %d: 消費了產品 %d [位置 %d]\n", id, item, out_idx);
        out_idx = (out_idx + 1) % BUFFER_SIZE;

        pthread_mutex_unlock(&mutex);
        sem_post(&empty);

        usleep(rand() % 500000); /* 模擬消費耗時 */
    }
    return NULL;
}

int main(void) {
    pthread_t prod_threads[PRODUCER_COUNT];
    pthread_t cons_threads[CONSUMER_COUNT];
    int prod_ids[PRODUCER_COUNT];
    int cons_ids[CONSUMER_COUNT];

    /* 初始化信號量和互斥鎖 */
    sem_init(&empty, 0, BUFFER_SIZE);
    sem_init(&full, 0, 0);
    pthread_mutex_init(&mutex, NULL);

    printf("=== 生產者-消費者問題模擬 ===\n");
    printf("緩衝區大小: %d, 生產者: %d, 消費者: %d\n\n",
           BUFFER_SIZE, PRODUCER_COUNT, CONSUMER_COUNT);

    /* 創建生產者線程 */
    for (int i = 0; i < PRODUCER_COUNT; i++) {
        prod_ids[i] = i + 1;
        pthread_create(&prod_threads[i], NULL, producer, &prod_ids[i]);
    }

    /* 創建消費者線程 */
    for (int i = 0; i < CONSUMER_COUNT; i++) {
        cons_ids[i] = i + 1;
        pthread_create(&cons_threads[i], NULL, consumer, &cons_ids[i]);
    }

    /* 等待所有線程完成 */
    for (int i = 0; i < PRODUCER_COUNT; i++) {
        pthread_join(prod_threads[i], NULL);
    }
    for (int i = 0; i < CONSUMER_COUNT; i++) {
        pthread_join(cons_threads[i], NULL);
    }

    /* 清理資源 */
    sem_destroy(&empty);
    sem_destroy(&full);
    pthread_mutex_destroy(&mutex);

    printf("\n=== 所有生產和消費完成 ===\n");
    return 0;
}
