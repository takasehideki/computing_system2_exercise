import os, sys

print(f"my PID: {os.getpid()}")

ret = os.fork()

if ret == 0:
    # Child process
    print("Child Process:")
    print(f"  my PID: {os.getpid()}")
    print(f"  Parent PID: {os.getppid()}")
    os.execve("/bin/echo", ["echo", f"Hello from {os.getpid()} by execve!"], {})  # Replace child process with /bin/echo
    sys.exit(0)
else:
    # Parent process
    print("Parent Process:")
    print(f"  my PID: {os.getpid()}")
    print(f"  Child PID: {ret}")
    os.wait()  # Wait for the child process to finish

sys.exit(1)