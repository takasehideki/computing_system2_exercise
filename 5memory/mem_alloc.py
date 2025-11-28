import subprocess
import time
import os
import sys

# 実記憶に確保する巨大配列のサイズ（バイト単位）：ここでは約1GB (1 * 1024^3)
MEMORY_SIZE_BYTES = 1 * 1024 * 1024 * 1024

# 巨大配列はグローバルで保持して，delで参照が解除されるまで
# メモリを占有させる（関数終了後にGCで解放されないようにする）
huge_memory_list = None

# メモリ使用量を表示する関数
def show_memory_status(step_name):
    print("=" * 60)
    print(f"--- Memory Status at Step: {step_name} ---")

    # free コマンドを実行して実記憶の使用量を表示
    show_command = ['free']
    try:
        result = subprocess.run(show_command, capture_output=True, text=True, check=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Failed to execute {show_command} command. {e}")

    print("=" * 60)

# 実記憶を確保するデモのメイン関数
def main_memory_allocation_demo():
    global huge_memory_list

    print(f"Process PID: {os.getpid()}")
    print(f"Memory amount to allocate: Approx. {MEMORY_SIZE_BYTES / (1024**3):.2f} GB")
    print("-" * 60)

    # 確保前のメモリ使用状況を表示
    show_memory_status("Before Allocation")

    # 実記憶を確保する処理：
    # 巨大配列を作成しながらデータを格納してアクセスすることでOSに実記憶の確保を要求する
    # ここではゼロ初期化（Pythonでは8バイトとして概算）して値を書き込むことで実現している
    print(f"\n[IN PROGRESS] Generating a huge list and allocating approx. {MEMORY_SIZE_BYTES / (1024**3):.2f} GB of memory...")
    try:
        huge_memory_list = [0] * (MEMORY_SIZE_BYTES // 8)
    except MemoryError:
        print("\n!!! MemoryError occurred. Not enough memory available on the system. !!!")
        sys.exit(1)
    # 確保されたメモリがGCされないように短い時間待機
    time.sleep(2)
    print("[DONE] Memory allocation completed.")

    # 確保後のメモリ使用状況を表示
    show_memory_status("After Allocation")

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
    main_memory_allocation_demo()