# Jenkins-Driven Automated Vulnerability Detection, Error Monitoring, and Notification Pipeline with MySQL and Trivy Integration

# Project Overview
This project is an automated pipeline that integrates Jenkins, MySQL, and Trivy for vulnerability detection, error monitoring, and notifications. It is designed to detect vulnerabilities in source code, track errors, and notify developers promptly. The system leverages the power of Jenkins for automation, MySQL for storing logs and vulnerability data, and Trivy for scanning repositories or file systems for vulnerabilities.

# Key Features:

Automated Vulnerability Scanning using Trivy for fast and efficient detection.

Error Log Monitoring through custom Python scripts that simulate errors and store them in MySQL.

Email Notifications alerting developers about vulnerabilities and errors.

Jenkins Integration for seamless, continuous execution of the entire pipeline.

HTML Report Generation summarizing the vulnerabilities and errors found.

MySQL Database for storing error logs and vulnerability data for reporting and analysis.

# Technologies Used

Jenkins: Continuous integration and automation tool.

MySQL: Database for storing error logs and vulnerabilities.

Trivy: Fast and simple vulnerability scanner for repositories and file systems.

Python: Scripting language for automation and error handling.

Bash: Shell scripting for task automation (run_all.sh, trivy_scanner.sh).

HTML: Used for generating reports for the developer.

SMTP: For sending email notifications.
