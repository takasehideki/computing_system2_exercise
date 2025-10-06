# ベースイメージとしてUbuntuを使用
FROM ubuntu:24.04

# 必要なパッケージをインストール
RUN apt-get update && \
  apt-get install -y \
  build-essential \
  sysstat && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/*

# デフォルトのコマンドを指定
CMD ["bash"]
