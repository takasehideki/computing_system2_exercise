#include <stdio.h>
#include <stdlib.h>

#define N 1024  // 行列のサイズ

void matmul(double *a, double *b, double *c) {
  for (int i = 0; i < N; i++) {
    for (int k = 0; k < N; k++) {
        double r = a[i * N + k];
        for (int j = 0; j < N; j++) {
            c[i * N + j] += r * b[k * N + j];
        }
    }
  }
}

int main() {
  double *a = (double *)malloc(sizeof(double) * N * N);
  double *b = (double *)malloc(sizeof(double) * N * N);
  double *c = (double *)malloc(sizeof(double) * N * N);

  // 行列の初期化
  for (int i = 0; i < N * N; i++) { a[i] = 1.0; b[i] = 2.0; }

  matmul(a, b, c);

  printf("Result: %f\n", c[0]); // 結果の一部を表示
  return 0;
}