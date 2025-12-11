import time
import os
import random
import string
import sys
from io import FileIO, BufferedWriter

# 書き込み先として一時的に作成されるファイル名
FILE_NAME_NO_BUFF = "tmp_no_buff_write.txt"
FILE_NAME_BUFF = "tmp_buff_write.txt"
# 書き込みを行うダミーデータのサイズ (1MB)
FILE_SIZE = 1 * 1024 * 1024
# 非バッファリング時のチャンクサイズ (4バイト)
CHUNK_SIZE_NO_BUFFER = 4
# バッファリング時のチャンクサイズ (1KB)
CHUNK_SIZE_BUFFER = 1 * 1024

# バッファリングなしの小さなチャンク単位での書き込み時間を計測する関数
# Python標準のバッファリングを最小限に抑えて操作を模擬
def measure_no_buffering_write(data):
    start_time = time.time()

    try:
        # os.open でファイルディスクリプタを直接操作する（Python標準のI/Oストリームを避ける）ことで
        # バッファリングを最小限に抑える（ただしOSレベルのバッファリングは残る）
        fd = os.open(FILE_NAME_NO_BUFF, os.O_CREAT | os.O_WRONLY)

        total_written = 0
        while total_written < len(data):
            # 小さなチャンクごとにデータを切り出す
            chunk = data[total_written:total_written + CHUNK_SIZE_NO_BUFFER]

            # OSに直接書き込みを要求する
            total_written += os.write(fd, chunk)

        # 最終的な書き込み完了を待つ（必須ではないがディスクへの反映を保証するために実行）
        os.fsync(fd)

    except Exception as e:
        print(f"\nAn error occurred: {e}")
        return None

    # ファイルディスクリプタを閉じてクリーンアップ
    finally:
        if 'fd' in locals() and fd >= 0:
            os.close(fd)

    end_time = time.time()
    return end_time - start_time

# バッファリングありの大きなチャンク単位での書き込み時間を計測する関数
def measure_buffering_write(data):
    start_time = time.time()

    # RAWのファイルディスクリプタを取得してBufferedWriterで大きなバッファを追加
    try:
        raw_io = FileIO(FILE_NAME_BUFF, 'w')
        buffered_io = BufferedWriter(raw_io, buffer_size=CHUNK_SIZE_BUFFER)

        # データを一括で書き込む
        buffered_io.write(data)

        # バッファに残っているデータを強制的にディスクに書き出す
        buffered_io.flush()

    except Exception as e:
        print(f"\nAn error occurred: {e}")
        return None

    # 確保したリソースを閉じてクリーンアップ
    finally:
        if 'buffered_io' in locals():
            buffered_io.close()

    end_time = time.time()
    return end_time - start_time

# バッファリングの有無で書き込み効率を比較するデモのメイン関数
def main_buffering_write_demo():
    print("--- Demo for efficiency of file buffering ---")
    print(f"  File name (no buffering): {FILE_NAME_NO_BUFF}")
    print(f"  File name (with buffering): {FILE_NAME_BUFF}")
    print(f"  File size: {FILE_SIZE / (1024 * 1024)} MB ({FILE_SIZE} bytes)")
    print(f"  Chunk size without buffering: {CHUNK_SIZE_NO_BUFFER} bytes")
    print(f"  Chunk size with buffering: {CHUNK_SIZE_BUFFER} bytes")
    print("---------------------------------------------")

    # ダミーデータを用意（'X' の繰り返しで模擬）
    print("Preparing dummy data in memory...")
    try:
        data_to_write = b'X' * FILE_SIZE
        print("Data preparation complete.")
    except MemoryError:
        print("\n!!! Memory Allocation Error: Please reduce the file size.!!!")
        return

    # 非バッファリング書き込みを実行・計測
    print(f"\n--- 1. Inefficient write w/o buffering by {CHUNK_SIZE_NO_BUFFER} bytes chunk ---")
    no_buffer_time = measure_no_buffering_write(data_to_write)

    # バッファリング書き込みを実行・計測
    print(f"\n--- 2. Efficient write with buffering by {CHUNK_SIZE_BUFFER} bytes chunk ---")
    buffer_time = measure_buffering_write(data_to_write)

    # 結果の表示
    if no_buffer_time is not None and buffer_time is not None:
        print(f"\nResults Summary:")
        print(f"1. Inefficient write time: {no_buffer_time:.4f} seconds")
        print(f"2. Efficient write time: {buffer_time:.4f} seconds")

        if no_buffer_time > 0:
            speedup = no_buffer_time / buffer_time
            print(f"Speedup: Approx. {speedup:.2f} times faster")
        else:
            print("Inefficient write time is too short to calculate the ratio.")
    else:
        print("An error occurred during the write operations; results are incomplete.")
        sys.exit(1)

    # 生成されたファイルの比較
    if not os.path.exists(FILE_NAME_NO_BUFF) or not os.path.exists(FILE_NAME_BUFF):
        print("Error: One or both files do not exist.")
    else:
        fd1 = os.open(FILE_NAME_NO_BUFF, os.O_RDONLY)
        fd2 = os.open(FILE_NAME_BUFF, os.O_RDONLY)
        try:
            while True:
                chunk1 = os.read(fd1, CHUNK_SIZE_BUFFER)
                chunk2 = os.read(fd2, CHUNK_SIZE_BUFFER)
                if not chunk1 and not chunk2:
                    print("File comparison: The files are identically the same.")
                    break
                if chunk1 != chunk2:
                    print("File comparison: The files differ.")
                    break
                if not chunk1 or not chunk2:
                    print("File comparison: The files differ in size.")
                    break
        except Exception as e:
            print(f"An error occurred during file comparison: {e}")
        finally:
            os.close(fd1)
            os.close(fd2)

    # ファイルを削除してクリーンアップ
    try:
        os.remove(FILE_NAME_NO_BUFF)
        os.remove(FILE_NAME_BUFF)
        print(f"\nThe demo files were successfully cleaned up.")
    except OSError:
        print(f"\nFailed to clean up the demo files.")

if __name__ == "__main__":
    main_buffering_write_demo()