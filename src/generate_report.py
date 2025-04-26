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
# Fetch real error logs from database
# Fetch error logs from database
cursor.execute("SELECT error_message, timestamp FROM error_logs ORDER BY timestamp DESC LIMIT 15")
error_logs_records = cursor.fetchall()

# Prepare list with timestamp + error message
error_logs = [f"{record['timestamp']} - {record['error_message']}" for record in error_logs_records]

cursor.close()
conn.close()

# Fetch from environment variables (not dummy values)
build_number = os.getenv("BUILD_NUMBER", "N/A")
commit_id = os.getenv("GIT_COMMIT", "N/A")




# Render the template
html_output = template.render(
    build_number=build_number,
    commit_id=commit_id,
    error_logs=error_logs,
    vulnerabilities=vulnerabilities
)

# Save to file
output_file = os.path.join(os.path.dirname(__file__), 'report.html')
with open(output_file, 'w') as f:
    f.write(html_output)

print("✅ Report generated successfully from database and real Jenkins environment!")
