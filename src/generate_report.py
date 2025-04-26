import os
import mysql.connector
from jinja2 import Environment, FileSystemLoader

# Set up template directory
template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
env = Environment(loader=FileSystemLoader(template_dir))
template = env.get_template('report_template.html')

# Load DB config manually (improve later to use config file if needed)
config = {
    "host": "localhost",
    "user": "root",
    "password": "admin",
    "database": "logscanner"
}

# Connect to MySQL and fetch vulnerabilities
conn = mysql.connector.connect(**config)
cursor = conn.cursor(dictionary=True)

cursor.execute("SELECT target, pkg_name, installed_version, vulnerability_id, severity, title FROM trivy_vulnerabilities")
vulnerabilities = cursor.fetchall()
print(vulnerabilities)

cursor.close()
conn.close()

# Fetch from environment variables (not dummy values)
build_number = os.getenv("BUILD_NUMBER", "N/A")
commit_id = os.getenv("GIT_COMMIT", "N/A")
commit_message = os.getenv("GIT_COMMIT_MSG", "N/A")
commit_date = os.getenv("GIT_COMMIT_DATE", "N/A")

# Simulating error logs (you can connect to DB or file if needed)
error_logs = ["Sample error line 1", "Sample error line 2"]

# Render the template
html_output = template.render(
    build_number=build_number,
    commit_id=commit_id,
    commit_message=commit_message,
    commit_date=commit_date,
    error_logs=error_logs,
    vulnerabilities=vulnerabilities
)

# Save to file
output_file = os.path.join(os.path.dirname(__file__), 'report.html')
with open(output_file, 'w') as f:
    f.write(html_output)

print("✅ Report generated successfully from database and real Jenkins environment!")
