import time

LOG_FILE = "/home/user/automatic-file-change-notification/logs/error.log"

errors = [
    "[ERROR] 2025-04-19 16:45:00 - File not found",
    "[ERROR] 2025-04-19 17:46:00 - Unexpected null value",
    "[ERROR] 2025-04-19 19:47:00 - Timeout while processing request",
]

def append_errors():
    with open(LOG_FILE, "a") as f:
        for error in errors:
            f.write(error + "\n")
            print(f"Appended: {error}")
            time.sleep(5)  # Wait 5 seconds before appending the next error

if __name__ == "__main__":
    append_errors()
