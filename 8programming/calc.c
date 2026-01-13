/* This is a simple calculator program */
#include <stdio.h>  // Include standard input-output header

int main() {
  int a, b, c, x;  // Declare integer variables a, b, c, and x
  a = 10;          // Assign value 10 to variable a
  b = 20;          // Assign value 20 to variable b
  c = 3;           // Assign value 3 to variable c
  printf("Calculating: %d + %d * %d\n", a, b, c);  // Print the calculation being performed

  x = a + b * c;   // Perform arithmetic operation and assign the result to x

  printf("Result: %d\n", x);  // Print the result

  return x;
}