import os
import time
import mysql.connector
from configparser import ConfigParser

# Use absolute paths for config, logs, and position file
CONFIG_PATH = "/home/user/automatic-file-change-notification/config/settings.conf"
LOG_FILE = "/home/user/automatic-file-change-notification/logs/error.log"
LAST_POS_FILE = "/home/user/automatic-file-change-notification/logs/last_pos.txt"
def load_config():
    parser = ConfigParser()
    parser.read(CONFIG_PATH)
    
    if parser.defaults():
        config = dict(parser.defaults())
        print(f"Loaded config: {config}")  # Debug print
        return config
    else:
        print("No DEFAULT section found in config file")
        return {}


def connect_db(config):
    try:
        conn = mysql.connector.connect(
            host=config["database_url"],
            user=config["database_user"],
            password=config["database_password"],
            database=config["database_name"]
        )
        print("✅ DB Connection successful")
        return conn
    except mysql.connector.Error as err:
        print("❌ DB Connection failed:", err)
        raise



'''def connect_db(config):
    return mysql.connector.connect(
        host=config["database_url"],
        user=config["database_user"],
        password=config["database_password"],
        database=config["database_name"]
    )'''


def parse_new_errors():
    if not os.path.exists(LAST_POS_FILE):
        last_pos = 0
    else:
        with open(LAST_POS_FILE, 'r') as f:
            last_pos = int(f.read())

    with open(LOG_FILE, 'r') as f:
        f.seek(last_pos)
        new_lines = f.readlines()
        last_pos = f.tell()

    with open(LAST_POS_FILE, 'w') as f:
        f.write(str(last_pos))

    return [line.strip() for line in new_lines if "[ERROR]" in line]

def insert_errors_to_db(errors, db_conn):
    cursor = db_conn.cursor()
    for error in errors:
        cursor.execute("INSERT INTO error_logs (error_message) VALUES (%s)", (error,))
    db_conn.commit()
    cursor.close()

if __name__ == "__main__":
    print("Starting Notifier...")
    config = load_config()
    db_conn = connect_db(config)
    errors = parse_new_errors()
    if errors:
        print(f"Found {len(errors)} new error(s). Inserting to DB...")
        insert_errors_to_db(errors, db_conn)
    else:
        print("No new errors found.")
    db_conn.close()
