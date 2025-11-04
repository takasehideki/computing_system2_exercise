import signal
import time
import sys
import os

# 繰り返し間隔を定義 (秒・整数)
INTERVAL = 5

# タイマ割込み処理に対応するSIGALRMが発生したときに実行されるハンドラ
def timer_handler(signum, frame):
    # 外部割込みの発生を通知
    sys.stderr.write("\n[External Interruption Handling]:\n")
    sys.stderr.write(f"  Timer interrupt (SIGALRM: {signum}) occurred\n\n")
    # ハンドラ内で再度 alarm() を呼び出して次のタイマ割込みを設定する
    signal.alarm(INTERVAL)

def main_timer_wait():
    print(f"--- Demo for external interruption: timer wait ---")

    # SIGALRMに対する割込み処理を設定
    try:
        signal.signal(signal.SIGALRM, timer_handler)
    except OSError as e:
        sys.stderr.write(f"Failed to set signal handler: {e}\n")
        sys.exit(1)

    # 5秒後に SIGALRM シグナルをプロセスに送信するようにOSにタイマを設定
    # カーネルがタイマ満了という外部イベントを監視する
    signal.alarm(INTERVAL)

    print(f"PID of this process: {os.getpid()}")
    print(f"Timer interrupt will occur every {INTERVAL} seconds.\n")

    try:
        # 無限ループでメインの作業を実行
        counter = 0
        while True:
            time.sleep(1.0)
            counter += 1
            print(f"Main loop running... ({counter})", end="\r", flush=True)
    except KeyboardInterrupt:
        # Ctrl+C の入力（SIGINTの発生）で終了する
        print("\nProgram terminated by Ctrl+C.")
        # 実行中のアラームをキャンセルしてクリーンアップする
        signal.alarm(0)
        sys.exit(0)

if __name__ == "__main__":
    main_timer_wait()