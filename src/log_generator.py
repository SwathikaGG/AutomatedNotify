
import time

LOG_FILE = "/home/user/automatic-file-change-notification/logs/error.log"
LAST_POS_FILE = "/home/user/automatic-file-change-notification/logs/last_pos.txt"

errors = [
    "[ERROR] 2025-04-19 16:00:00 - File not found",
    "[ERROR] 2025-04-20 17:00:00 - Unexpected null value",
    "[ERROR] 2025-04-20 19:12:00 - Timeout while processing request",
    "[ERROR] 2025-04-21 09:30:00 - Invalid input data",
    "[ERROR] 2025-04-21 11:00:00 - Connection timeout"
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
