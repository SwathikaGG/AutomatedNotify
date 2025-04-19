import os
from jinja2 import Environment, FileSystemLoader

# Set the path to your templates directory
template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')

# Create an environment and tell Jinja2 where to look for templates
env = Environment(loader=FileSystemLoader(template_dir))

# Load the template
template = env.get_template('report_template.html')

# Data to be passed into the template
data = {
    'error_logs': 'Example error log content...',
    'build_info': 'Build number 26...',
    'commit_details': 'Git commit: abc123...',
}

# Render the template with data
html_output = template.render(data)

# Save the generated HTML to a file
with open('report.html', 'w') as f:
    f.write(html_output)

print("Report generated successfully!")
