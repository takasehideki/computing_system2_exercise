import sys
import os

def main_input_wait():
    print("--- Demo for external interruption: I/O wait ---")
    print(f"PID of this process: {os.getpid()}")

    count = 1
    while True:
        # input() が呼び出されるとカーネルに制御が戻され
        # プロセスはキーボードからのI/O割り込みを待つ状態に遷移する
        user_input = input(f"\n[{count}] Enter something and press Enter (q to quit): ")

        # 割り込み（入力）が完了した後の処理
        print(f"I/O Completion Notification: Processed input '{user_input}'.", flush=True)
        count += 1

        # 'q'のときはループを抜けて終了する
        if user_input.lower() == 'q':
            break

    print("\nExiting the program.")

if __name__ == "__main__":
    main_input_wait()