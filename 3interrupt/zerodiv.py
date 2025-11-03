import sys

def main_zero_division():
    # コマンドライン引数のチェック
    if len(sys.argv) != 2:
        # 使用方法を標準エラー出力に表示して終了
        sys.stderr.write(f"Usage: python3 {sys.argv[0]} <denominator_number>\n")
        sys.exit(1)

    print("--- Demo for internal interruption: Zero Division Exception ---")

    # 分子を100に設定してコマンドライン引数から分母を取得
    numerator = 100
    try:
        denominator = int(sys.argv[1])
    except ValueError:
        # 分母が整数でない場合のエラー処理
        sys.stderr.write(f"Invalid denominator: {sys.argv[1]} must be an integer\n")
        sys.exit(1)

    print(f"Execute {numerator} / {denominator}")

    try:
        # 分母がゼロの場合はこの命令実行時にCPU内で例外（内部割り込み）が発生する
        result = numerator / denominator
        # 除算が正常に実行できた場合は結果を出力 (例外発生時には実行されない)
        print(f"Result (success): {result}")

    except ZeroDivisionError as e:
        # カーネルから制御が戻ってPythonの例外ハンドラがこれを捕捉する
        print(f"\n[Internal Interruption Handling]:")
        print(f"  ZeroDivisionError was detected by the kernel.")
        print(f"  Error message: {e}")

if __name__ == "__main__":
    main_zero_division()