import multiprocessing
import time
import random
import sys
import os

# 哲学者の人数と食事を何度試みるか
NUM_PHILOSOPHERS = 5
EATING_CYCLES = 3

# 共有資源として哲学者の人数分のフォークを用意
forks = [multiprocessing.Semaphore(1) for _ in range(NUM_PHILOSOPHERS)]

# 哲学者の動作をシミュレートする関数
def philosopher_life(philosopher_id):
    # プロセスIDを取得（デバッグ用）
    pid = os.getpid()

    # フォークのインデックスを決定
    # right_forkはphilosopher_idのフォーク、left_forkは隣のphilosopherのフォーク
    right_fork = forks[philosopher_id]
    left_fork = forks[(philosopher_id - 1 + NUM_PHILOSOPHERS) % NUM_PHILOSOPHERS]

    for cycle in range(EATING_CYCLES):
        # 1. 思索する
        print(f"[PID:{pid}] P{philosopher_id} is thinking... (Cycle {cycle+1})", flush=True)
        time.sleep(random.uniform(0.1, 0.5))

        # 2. 食事を試みる
        while True:
            # 右側のフォークを確保 (P操作)
            print(f"[PID:{pid}] P{philosopher_id} tries to pick up RIGHT fork ({philosopher_id})...", flush=True)
            right_fork.acquire()
            print(f"[PID:{pid}] P{philosopher_id} successfully picked up RIGHT fork ({philosopher_id}).", flush=True)

            # 片方の共有資源を保持した状態になりやすくする（全員に右のフォークを持たせる）ための待機時間
            time.sleep(0.5)

            # 左側のフォークを確保しようとする (P操作)
            print(f"[PID:{pid}] P{philosopher_id} tries to pick up LEFT fork ({(philosopher_id - 1 + NUM_PHILOSOPHERS) % NUM_PHILOSOPHERS})...", flush=True)
            left_fork.acquire()
            print(f"[PID:{pid}] P{philosopher_id} successfully picked up LEFT fork ({(philosopher_id - 1 + NUM_PHILOSOPHERS) % NUM_PHILOSOPHERS}).", flush=True)

            # 両方のフォークを確保できたのでループを抜ける
            break

        # デッドロックが発生すると以降は実行されない
        # 両方のフォークを確保できたので食事をする
        print(f"[PID:{pid}] P{philosopher_id} is EATING!!", flush=True)
        time.sleep(1.0)

        # 3. 両方のフォークを解放 (V操作)
        left_fork.release()
        right_fork.release()
        print(f"[PID:{pid}] P{philosopher_id} finished eating and released forks. (Cycle {cycle+1})", flush=True)

def main_philosophers():
    print("--- Demo for Dining Philosophers ---")
    print(f"  Parent PID: {os.getpid()}")
    print(f"  Number of Philosophers/Forks: {NUM_PHILOSOPHERS}")
    print("------------------------------------")

    processes = []
    # 哲学者IDを引数として渡しながらプロセスの生成と実行
    for i in range(NUM_PHILOSOPHERS):
        process = multiprocessing.Process(target=philosopher_life, args=(i,))
        processes.append(process)
        process.start()
        print(f"Starting Process P{i} with PID[{process.pid}]", flush=True)

    # 全プロセスの終了を待機（デッドロックして停止した時にはCtrl+Cで手動停止が必要）
    for process in processes:
        process.join()

    print("\n--- All philosophers have finished eating successfully ---", flush=True)

if __name__ == "__main__":
    try:
        main_philosophers()
    except KeyboardInterrupt:
        sys.exit(0)