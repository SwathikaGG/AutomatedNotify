
import time

LOG_FILE = "/home/user/automatic-file-change-notification/logs/error.log"
LAST_POS_FILE = "/home/user/automatic-file-change-notification/logs/last_pos.txt"

errors = [
    "[ERROR]  - File not found",
    "[ERROR]  - Unexpected null value",
    "[ERROR]  - Timeout while processing request",
    "[ERROR]  - Invalid input data",
    "[ERROR]  - Connection timeout"
]

def append_errors():
    with open(LOG_FILE, "a") as f:
        for error in errors:
            f.write(error + "\n")
            print(f"Appended: {error}")
            time.sleep(5)  # Wait 5 seconds before appending the next error
    
    # Optionally reset the last position file if you want to clear it after appending
    with open(LAST_POS_FILE, 'w') as f:
        f.write("0")  # Reset to the beginning if you want to process all errors again next time

if __name__ == "__main__":
    append_errors()
