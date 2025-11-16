import multiprocessing
import time
import os
import sys

# プロセス数とプロセスごとのインクリメント回数
NUM_PROCESSES = 5
INCREMENTS_PER_PROCESS = 20_000

# 共有資源（共有メモリ）としてカウンタを用意して初期化
# i: 整数型, 0: 初期値
# これによりプロセス間で同じメモリ領域を参照する
SHARED_COUNTER = multiprocessing.Value('i', 0)

# 排他制御のためのセマフォ
# セマフォ変数（内部カウンタ）が1なのでバイナリセマフォ（ミューテックス）として機能
semaphore = multiprocessing.Semaphore(1)

# プロセス間で共有されるカウンタをインクリメントするワーカー関数
def increment_worker(counter, process_id):
    for _ in range(INCREMENTS_PER_PROCESS):
        # セマフォのP操作（資源の獲得）
        # 本来は try-finally で解放を保証すべきだが簡略化のため省略
        semaphore.acquire()

        # 競合状態が発生しうるクリティカルセクションの処理
        # counter.value += 1 でもいいが敢えて分解して記述している
        current_value = counter.value
        current_value += 1
        counter.value = current_value

        # デバッグ出力：コメントインすると動作を細かく観測できる
        # print(f"Process {process_id} (PID[{os.getpid()}]) increments to {counter.value}", flush=True)

        # セマフォのV操作（資源の解放）
        semaphore.release()

def main_sync_demo():
    global SHARED_COUNTER

    processes = []
    target_value = NUM_PROCESSES * INCREMENTS_PER_PROCESS

    print("--- Demo for process synchronization ---")
    print(f"  Parent Process PID: {os.getpid()}")
    print(f"  Number of Processes: {NUM_PROCESSES}")
    print(f"  Target final value: {target_value}")
    print("----------------------------------------")

    # 処理時間の計測開始
    start_time = time.time()

    # 各プロセスに共有カウンタオブジェクトを渡しながら生成と実行
    for i in range(NUM_PROCESSES):
        process = multiprocessing.Process(target=increment_worker, args=(SHARED_COUNTER, i))
        processes.append(process)
        process.start()
        print(f"Starting Process {i} with PID[{process.pid}]", flush=True)

    # 全プロセスの終了を待機
    for process in processes:
        process.join()
        print(f"Process with PID[{process.pid}] has finished.", flush=True)

    # 処理時間の計測終了
    end_time = time.time()

    final_value = SHARED_COUNTER.value

    print("----------------------------------------")
    print(f"Incremented final value: {final_value}")

    # 結果の検証
    if final_value == target_value:
        print(f"Success! Data consistency confirmed. All increments accounted for.")
    else:
        print(f"Failed! Data inconsistency detected. {target_value - final_value} increments were lost.")

    print(f"Execution time: {end_time - start_time:.4f} seconds")

if __name__ == "__main__":
    main_sync_demo()