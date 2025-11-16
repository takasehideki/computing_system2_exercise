import sys, time
import datetime # for use of busy loop

def main():
    # check command line arguments
    if len(sys.argv) != 2:
        sys.stderr.write(f"Usage: {sys.argv[0]} <message>\n")
        sys.exit(1)

    message = sys.argv[1]
    count = 0

    # set busy loop duration
    BUSY_DURATION_SECONDS = 1.0

    # main loop
    try:
        while count < 30:  # limit to 30 iterations
            print(f"{message}: {count}")
            count += 1

            # start busy loop
            start_time = time.time()
            while time.time() - start_time < BUSY_DURATION_SECONDS:
                pass

    # handle keyboard interrupt (e.g., Ctrl+C) to exit gracefully
    except KeyboardInterrupt:
        print("\nBusy loop interrupted by user.")
        sys.exit(0)

if __name__ == "__main__":
    main()