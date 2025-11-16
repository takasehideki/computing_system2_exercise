import multiprocessing
import time
import random
import os
import sys

# 設定
NUM_PRODUCERS = 2  # 生産者プロセスの数
NUM_CONSUMERS = 3  # 消費者プロセスの数
ITEMS_PER_PRODUCER = 10   # 1つの生産者が作成するアイテム数
BUFFER_SIZE = 5    # キューの最大サイズ
MAX_PRODUCER_SLEEP_TIME = 0.3  # 生産者のアイテム作成の最大待機時間（秒）
MAX_CONSUMER_SLEEP_TIME = 1.0  # 消費者のアイテム処理の最大待機時間（秒）

# 終了を通知するための特殊な値（センチネル値）
SENTINEL = None

# 生産者：アイテムを作成してキューに入れる
def producer(queue, producer_id):
    # プロセスIDを取得（デバッグ用）
    pid = os.getpid()
    print(f"[{pid}] Producer {producer_id} starting. Will generate {ITEMS_PER_PRODUCER} items.", flush=True)

    for i in range(ITEMS_PER_PRODUCER):
        # アイテムのデータを作成
        item = f"Data-{producer_id}-{i:02}"

        # キューにアイテムを追加する
        # キューが満杯の場合は休眠して空きができるのを待つ
        queue.put(item)

        print(f"[{pid}] Producer {producer_id} produced: {item}", flush=True)

        # 次の作成までランダムな時間で待機
        time.sleep(random.uniform(0.1, MAX_PRODUCER_SLEEP_TIME))

    print(f"[{pid}] Producer {producer_id} finished generating {ITEMS_PER_PRODUCER} items.", flush=True)

# 消費者：キューからアイテムを取り出して処理する
def consumer(queue, consumer_id):
    # プロセスIDを取得（デバッグ用）
    pid = os.getpid()
    print(f"[{pid}] Consumer {consumer_id} starting.", flush=True)

    processed_count = 0
    # 終了シグナルを受け取るまでループ
    while True:
        # キューからアイテムを取り出す
        # キューが空の場合は休眠してアイテムが来るのを待つ
        item = queue.get()

        # センチネル値を受け取ったら処理を終了する
        if item is SENTINEL:
            print(f"[{pid}] Consumer {consumer_id} received SENTINEL. Stopping.", flush=True)
            break

        print(f"[{pid}] Consumer {consumer_id} consumed: {item}", flush=True)
        processed_count += 1

        # アイテムの処理をランダムな時間でシミュレート
        time.sleep(random.uniform(0.1, MAX_CONSUMER_SLEEP_TIME))

    print(f"[{pid}] Consumer {consumer_id} finished. Total items processed: {processed_count}", flush=True)

def main_comm_demo():
    # プロセス間で共有されるキュー（バッファ）を初期化
    queue = multiprocessing.Queue(maxsize=BUFFER_SIZE)

    producers = []
    consumers = []

    print("--- Demo for Producer-Consumer Problem ---")
    print(f"  The number of producers: {NUM_PRODUCERS}")
    print(f"  The number of consumers: {NUM_CONSUMERS}")
    print(f"  Items per producer: {ITEMS_PER_PRODUCER}")
    print(f"  Total items to be produced: {ITEMS_PER_PRODUCER * NUM_PRODUCERS}")
    print(f"  Buffer size: {BUFFER_SIZE}")
    print("------------------------------------------")

    # 生産者プロセスの生成と起動
    for i in range(1, NUM_PRODUCERS + 1):
        p = multiprocessing.Process(
            target=producer,
            args=(queue, i)
        )
        producers.append(p)
        p.start()
        print(f"Starting Producer {i} with PID[{p.pid}]", flush=True)

    # 消費者プロセスの生成と起動
    for i in range(1, NUM_CONSUMERS + 1):
        c = multiprocessing.Process(
            target=consumer,
            args=(queue, i)
        )
        consumers.append(c)
        c.start()
        print(f"Starting Consumer {i} with PID[{c.pid}]", flush=True)

    # すべての生産者の終了を待機
    for p in producers:
        p.join()

    print("\n--- All Producers have finished. Waiting for Consumers... ---")

    # 生産者の数だけセンチネル値をキューに追加して消費者に終了を通知する
    for _ in range(NUM_CONSUMERS):
        queue.put(SENTINEL)

    # すべての消費者の終了を待機
    for c in consumers:
        c.join()

    print("\n--- All Consumers have also finished successfully ---")

if __name__ == "__main__":
    main_comm_demo()