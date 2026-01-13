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

# Docker CLIに必要なパッケージのインストールとリポジトリの設定
RUN apt-get update && apt-get install -y \
  ca-certificates \
  curl \
  gnupg \
  && install -m 0755 -d /etc/apt/keyrings \
  && curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg \
  && chmod a+r /etc/apt/keyrings/docker.gpg \
  && echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  tee /etc/apt/sources.list.d/docker.list > /dev/null

# Docker CLIのインストール
RUN apt-get update && apt-get install -y \
  docker-ce-cli \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# 9programming で必要なパッケージをインストール
RUN apt-get update && apt-get install -y \
  python3-pip elixir \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# PythonのJIT実行に関するパッケージをインストール
RUN pip3 install --break-system-packages --no-cache-dir numba

# デフォルトのコマンドを指定
CMD ["bash"]
