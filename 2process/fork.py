import os, sys

print(f"my PID: {os.getpid()}")

ret = os.fork()

if ret == 0:
    # Child process
    print("Child Process:")
    print(f"  my PID: {os.getpid()}")
    print(f"  Parent PID: {os.getppid()}")
    sys.exit(0)
else:
    # Parent process
    print("Parent Process:")
    print(f"  my PID: {os.getpid()}")
    print(f"  Child PID: {ret}")
    os.wait()  # Wait for the child process to finish

sys.exit(1)