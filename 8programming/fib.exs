defmodule Fib do
  def fib(n) when n < 2, do: n
  def fib(n), do: fib(n-1) + fib(n-2)
end

n = 40
IO.puts "Fibonacci(#{n}) = #{Fib.fib(n)}"