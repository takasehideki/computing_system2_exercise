# ベースイメージとしてUbuntuを使用
FROM ubuntu:24.04

# 非対面モードに設定（インストール中の入力を求められないようにする）
ENV DEBIAN_FRONTEND=noninteractive

# 必要なパッケージをインストール
RUN apt-get update && apt-get install -y \
  build-essential \
  sysstat \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# デフォルトのコマンドを指定
CMD ["bash"]
