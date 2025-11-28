import subprocess
import time
import os
import sys
import mmap  # 仮想記憶の確保のために追加

# 仮想記憶に確保する巨大配列のサイズ（バイト単位）：ここでは約100GB (100 * 1024^3)
MEMORY_SIZE_BYTES = 100 * 1024 * 1024 * 1024
# アクセスして実記憶に確保される巨大配列のサイズ（バイト単位）：ここでは約1MB (1 * 1024^2)
ACCESS_MEMORY_SIZE_BYTES = 1 * 1024 * 1024

# 巨大配列はグローバルで保持して，delで参照が解除されるまで
# メモリを占有させる（関数終了後にGCで解放されないようにする）
huge_memory_list = None

# メモリ使用量を表示する関数
def show_memory_status(step_name):
    print("=" * 60)
    print(f"--- Memory Status at Step: {step_name} ---")

    # ps コマンドを実行して実記憶と仮想記憶の使用量を表示
    show_command = ['ps', '-o', 'pid,cmd,rss,vsz', '-p', str(os.getpid())]
    try:
        result = subprocess.run(show_command, capture_output=True, text=True, check=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Failed to execute {show_command} command. {e}")

    print("=" * 60)

# 仮想記憶を確保するデモのメイン関数
def main_virtual_memory_allocation_demo():
    global huge_memory_list

    print(f"Process PID: {os.getpid()}")
    print(f"Memory amount to allocate: Approx. {MEMORY_SIZE_BYTES / (1024**3):.2f} GB")
    print("-" * 60)

    # 確保前のメモリ使用状況を表示
    show_memory_status("Before Allocation")

    # 仮想記憶を確保する処理：
    # 巨大配列のためのメモリ領域を確保してOSに仮想記憶の使用を要求する
    # この時点ではページにはアクセスしないためRSS（実記憶）は大きく増えないはず
    print(f"\n[IN PROGRESS] Generating a huge list and allocating approx. {MEMORY_SIZE_BYTES / (1024**3):.2f} GB of memory...")
    try:
        huge_memory_list = mmap.mmap(-1, MEMORY_SIZE_BYTES)
    except MemoryError:
        print("\n!!! MemoryError occurred. Not enough memory available on the system. !!!")
        sys.exit(1)
    # 確保されたメモリがGCされないように短い時間待機
    time.sleep(2)
    print("[DONE] Memory allocation completed.")

    # 確保後のメモリ使用状況を表示
    show_memory_status("After Allocation")

    # 実記憶を確保する処理：
    # 仮想記憶に確保されたメモリの一部にアクセスして実記憶に割り当てる
    # 全メモリにアクセスするとシステムが不安定になる可能性があるため，一部のみアクセスする
    print(f"\n[IN PROGRESS] Accessing a part of list to allocate approx. {ACCESS_MEMORY_SIZE_BYTES / (1024**2):.2f} MB of memory...")
    for i in range(0, ACCESS_MEMORY_SIZE_BYTES):
        huge_memory_list[i] = 0
    print("[DONE] Memory access completed.")

    # 少し待機してから再度状況を表示
    time.sleep(2)
    show_memory_status("After Accessing Memory")

    # 巨大配列のメモリマップを閉じる
    huge_memory_list.close()
    # 巨大配列への参照を解除して確保されているメモリを片付ける
    # グローバル変数の参照を削除してPythonのGCにメモリを解放させる
    del huge_memory_list
    print("\n[CLEANUP] Releasing the list reference and waiting for Python GC to free memory...")
    # GCが動作するのを待機（すぐに解放されない場合もあるため）
    time.sleep(5)

    # 5. 片付け後のメモリ使用状況を表示
    show_memory_status("After Cleanup")

    print("\nDemo finished.")

if __name__ == "__main__":
    main_virtual_memory_allocation_demo()