import mmap
import os
import time
import subprocess

# ダミーファイルとして一時的に作成されるファイル名
FILE_NAME = "tmp_fcb_write_demo.txt"
# ダミーファイルのサイズ (1MB)
FILE_SIZE = 1 * 1024 * 1024
# 書き込みアクセスのサイズ (50KB)
ACCESS_SIZE = 50 * 1024

# 各種情報を表示する関数
def show_status(step_name, pid):
    print("=" * 60)
    print(f"--- Status at Step: {step_name} ---")

    # A. ファイルのFCBの内容
    print("\n[A. File FCB Information: stat FILE_NAME]")
    show_command = ['stat', FILE_NAME]
    try:
        result = subprocess.run(show_command, capture_output=True, text=True, check=True)
        print(result.stdout.strip())
    except Exception as e:
        print(f"ERROR: Failed to execute {show_command} command. {e}")

    # B. プロセスが開いているファイルの情報
    print("\n[B. Open Files: lsof -p PID]")
    show_command = ['lsof', '-p', str(pid)]
    try:
        result = subprocess.run(show_command, capture_output=True, text=True, check=True)
        # デモファイル名を含む行のみを表示
        relevant_lines = [line for line in result.stdout.splitlines() if FILE_NAME in line]
        if relevant_lines:
            print(result.stdout.splitlines()[0] + '\n' + '\n'.join(relevant_lines))
        else:
            print("(Demo file is not shown)")
    except Exception as e:
        print(f"ERROR: Failed to execute {show_command} command. {e}")

    # C. 実記憶と仮想記憶の使用量
    print("\n[C. Memory Status: ps -o pid,rss,vsz PID]")
    show_command = ['ps', '-o', 'pid,rss,vsz', '-p', str(pid)]
    try:
        result = subprocess.run(show_command, capture_output=True, text=True, check=True)
        print(result.stdout.strip())
    except Exception as e:
        print(f"ERROR: Failed to execute {show_command} command. {e}")

    print("=" * 60)

# 仮想記憶を介してファイル操作を行うデモのメイン関数
def main_fcb_virtual_memory_demo():
    pid = os.getpid()

    print("--- Demo for file operation via virtual memory ---")
    print(f"  File name: {FILE_NAME}")
    print(f"  File size: {FILE_SIZE / (1024 * 1024)} MB ({FILE_SIZE} bytes)")
    print(f"  Access size to the file: {ACCESS_SIZE / (1024)} KB ({ACCESS_SIZE} bytes)")
    print(f"  Process PID: {pid}")
    print("--------------------------------------------------")

    # 準備：ダミーファイルを作成してFCB（inode）を設定する
    print(f"Generating dummy file...")
    f = os.open(FILE_NAME, os.O_CREAT | os.O_WRONLY)
    os.write(f, b'X' * FILE_SIZE)
    os.close(f)

    # 1. 準備完了後の状態を表示
    show_status("1. Initial State", pid)

    try:
        # mmapシステムコールによるファイルのマッピング
        print("[Operation: Map the file to virtual memory]")
        # 読み書きモードでファイルを開いてカーネルがFCBを参照する
        f = os.open(FILE_NAME, os.O_RDWR)
        # mmapを発行して仮想記憶を確保する
        mapped_data = mmap.mmap(f, FILE_SIZE, access=mmap.ACCESS_WRITE)
        time.sleep(2)
        print("mmap complete. File has been mapped to virtual memory.")

        # 2. 仮想記憶に割り当てた後の状態を表示
        show_status("2. After mmap (Virtual Memory Reservation)", pid)

        # 仮想記憶を介してファイルに書き込み
        print(f"[Operation: Access {ACCESS_SIZE / (1024)} KB to mapped area to allocate physical memory]")
        start_time = time.time()
        # 仮想記憶に確保された領域の一部にアクセスして実記憶に割り当てる
        for i in range(0, ACCESS_SIZE):
            mapped_data[i] = b'Z'[0]
        end_time = time.time()
        print(f"Access time to virtual memory: {end_time - start_time:.6f} seconds")
        # 書き込んだデータをファイルに反映
        mapped_data.flush()
        time.sleep(5)

        # 3. 実記憶を介したアクセス後の状態を表示
        show_status("3. After access (Physical Memory Allocation)", pid)

    except Exception as e:
        print(f"Fatal error: {e}")

    # ファイルの削除と仮想記憶の解放でクリーンアップ
    finally:
        if 'mapped_data' in locals():
            mapped_data.close()
        if 'f' in locals():
            os.close(f)
        if os.path.exists(FILE_NAME):
            os.remove(FILE_NAME)
        print("Demo finished and cleanup complete.")

if __name__ == "__main__":
    main_fcb_virtual_memory_demo()