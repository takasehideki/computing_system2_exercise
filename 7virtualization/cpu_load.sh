#!/bin/sh

# 論理コア数を取得
CORES=$(nproc)
echo "The number of cores detected: $CORES"
echo "Starting CPU load generation on all cores..."

# コアの数だけループを回してバックグラウンドで実行
for i in $(seq 1 $CORES); do
    # 無限ループをバックグラウンドで実行
    while true; do :; done &
done

echo "Load processes have been started."
echo "To stop the load, please terminate the container (e.g., Ctrl+C)."

# バックグラウンドプロセスが終了するのを待機（コンテナを維持するため）
wait