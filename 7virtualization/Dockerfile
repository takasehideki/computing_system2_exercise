# ベースイメージとしてAlpine Linuxを使用
FROM alpine:latest

# スクリプトをコンテナ内のパスへコピー
COPY cpu_load.sh /usr/local/bin/cpu_load.sh

# 実行権限を付与
RUN chmod +x /usr/local/bin/cpu_load.sh

# コンテナ起動時にスクリプトを実行
CMD ["/bin/sh", "/usr/local/bin/cpu_load.sh"]
