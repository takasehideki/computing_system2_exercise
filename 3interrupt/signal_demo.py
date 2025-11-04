import time
import sys
import signal
import os

keep_running = True
# SIGALRMの発生間隔
ALARM_INTERVAL = 5

# 登録されたシグナルが発生したときに実行されるハンドラ
def signal_demo_handler(signum, frame):
    # 受け取ったシグナルを表示する
    sys.stderr.write(f"\n[Signal Interruption Handling]:")
    sys.stderr.write(f" received {signal.Signals(signum).name} ({signum})\n")

    # SIGALRMの場合は再度タイマを設定する
    if signum == signal.SIGALRM:
        signal.alarm(ALARM_INTERVAL)
    # SIGTERMの場合は終了フラグを降ろしてメインループを終了させる
    elif signum == signal.SIGTERM:
        global keep_running
        keep_running = False

def main_signal_demo():
    print("--- Demo for signal handling ---")
    print("Available signals to handle: SIGINT, SIGUSR1, SIGALRM, SIGTERM")

    try:
        # 4種類のシグナルに対するハンドラを設定
        for sig in [signal.SIGINT, signal.SIGUSR1, signal.SIGALRM, signal.SIGTERM]:
            signal.signal(sig, signal_demo_handler)
        # SIGALRMのためのタイマ設定
        signal.alarm(ALARM_INTERVAL)
    except OSError as e:
        sys.stderr.write(f"Failed to set signal handler: {e}\n")
        sys.exit(1)

    print("\nMain loop starts.")
    print("To exit this program, please kill the process with another terminal using the PID.")

    counter = 0
    # メインループ
    while keep_running:
        time.sleep(1.0)
        counter += 1
        print(f"Loop {counter} running. PID: {os.getpid()}", end="\r", flush=True)

    # SIGTERMによってループから抜けた後の処理
    print("\n[Main loop resumed]: break from main loop")
    print("Exiting program")

    # 実行中のアラームをキャンセルしてクリーンアップする
    signal.alarm(0)
    sys.exit(0)

if __name__ == "__main__":
    main_signal_demo()