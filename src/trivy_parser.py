import json
import mysql.connector
import os

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'admin',  # Fill in if password is set
    'database': 'logscanner'
}

TRIVY_REPORT_FILE = os.path.join(os.getcwd(), 'logs', 'trivy_scan_report.json')

def insert_vulnerability(cursor, vuln):
    sql = """
    INSERT INTO trivy_vulnerabilities (target, pkg_name, installed_version, vulnerability_id, severity, title)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    values = (
        vuln.get('Target', ''),
        vuln.get('PkgName', ''),
        vuln.get('InstalledVersion', ''),
        vuln.get('VulnerabilityID', ''),
        vuln.get('Severity', ''),
        vuln.get('Title', '')
    )
    cursor.execute(sql, values)

def insert_no_vulnerability(cursor, target):
    # Insert a record indicating no vulnerabilities were found for the given target
    sql = """
    INSERT INTO trivy_vulnerabilities (target, pkg_name, installed_version, vulnerability_id, severity, title)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    values = (
        target,
        'N/A',  # No package name
        'N/A',  # No installed version
        'N/A',  # No vulnerability ID
        'N/A',  # No severity
        'No vulnerabilities found'  # Custom message for no vulnerabilities
    )
    cursor.execute(sql, values)

def main():
    if not os.path.exists(TRIVY_REPORT_FILE):
        print(f"❌ Trivy report not found at {TRIVY_REPORT_FILE}")
        return

    with open(TRIVY_REPORT_FILE, 'r') as f:
        data = json.load(f)

    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor()

    for result in data.get('Results', []):
        target = result.get('Target', '')
        vulnerabilities = result.get('Vulnerabilities', [])
        if vulnerabilities:  # If vulnerabilities are found, insert them
            for vuln in vulnerabilities:
                vuln['Target'] = target
                insert_vulnerability(cursor, vuln)
            connection.commit()
        else:
            print(f"✅ No vulnerabilities found for target: {target}")
            # Insert a record for "No vulnerabilities found"
            insert_no_vulnerability(cursor, target)
            connection.commit()

    cursor.close()
    connection.close()
    print("✅ Vulnerabilities (or 'No vulnerabilities found' records) inserted into MySQL successfully.")

if __name__ == "__main__":
    main()
