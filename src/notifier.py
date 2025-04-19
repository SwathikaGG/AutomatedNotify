import os
import time
import mysql.connector
from configparser import ConfigParser
from jinja2 import Environment, FileSystemLoader
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# Use absolute paths for config, logs, and position file
CONFIG_PATH = "/home/user/automatic-file-change-notification/config/settings.conf"
LOG_FILE = "/home/user/automatic-file-change-notification/logs/error.log"
LAST_POS_FILE = "/home/user/automatic-file-change-notification/logs/last_pos.txt"
TEMPLATE_DIR = "/home/user/automatic-file-change-notification/templates"
TEMPLATE_FILE = "report_template.html"

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

def render_html_report(build_number, commit_id, commit_message, commit_date, error_logs):
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template(TEMPLATE_FILE)
    return template.render(
        build_number=build_number,
        commit_id=commit_id,
        commit_message=commit_message,
        commit_date=commit_date,
        error_logs=error_logs
    )



def send_email_report(to_email, html_content):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Build Error Report"
    msg["From"] = "swathikagg0410@gmail.com"
    msg["To"] = to_email

    part = MIMEText(html_content, "html")
    msg.attach(part)

    try:
        # Connect to Gmail SMTP server using TLS (port 587)
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()  # Start TLS encryption

        # Login to the server with your Gmail credentials (use App Password here)
        server.login("swathikagg0410@gmail.com", "qtrr elov pmcs rvhw")

        # Send the email
        server.sendmail("swathikagg0410@gmail.com", to_email, msg.as_string())
        server.quit()
        print("✅ Email sent successfully!")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")



if __name__ == "__main__":
    print("Starting Notifier...")
    config = load_config()
    db_conn = connect_db(config)
    errors = parse_new_errors()
    if errors:
        print(f"Found {len(errors)} new error(s). Inserting to DB...")
        insert_errors_to_db(errors, db_conn)
        

# Get environment variables (can be set by Jenkins or manually)
        build_number = os.getenv("BUILD_NUMBER", "N/A")
        commit_id = os.getenv("GIT_COMMIT", "N/A")
        commit_message = os.getenv("GIT_COMMIT_MSG", "N/A")
        commit_date = os.getenv("GIT_COMMIT_DATE", "N/A")

# Render HTML report using Jinja2
        html_report = render_html_report(build_number, commit_id, commit_message, commit_date, errors)

# Send the report via email
        send_email_report(config.get("email_to", "admin@example.com"), html_report)

    else:
        print("No new errors found.")
    db_conn.close()
