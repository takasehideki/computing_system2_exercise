from numba import jit

@jit
def fib(n):
    if n < 2:
        return n
    return fib(n-1) + fib(n-2)

n = 40
print(f"Fibonacci({n}) = {fib(n)}")