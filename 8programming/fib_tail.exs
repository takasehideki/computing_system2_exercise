defmodule Fib do
  def fib(n), do: do_fib(n, 0, 1)

  defp do_fib(0, a, _b), do: a
  defp do_fib(n, a, b), do: do_fib(n - 1, b, a + b)
end

n = 40
IO.puts "Fibonacci(#{n}) = #{Fib.fib(n)}"