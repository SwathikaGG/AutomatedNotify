# Automatic User Notification on File Changes

This repository contains files that will be monitored for changes. 

- `config/`: Configuration files for the app.
- `logs/`: Log files generated during the application run.

The project uses Jenkins to monitor changes in these files and notify users when a change is detected.

## Files:

- `config/config.yaml`: App configuration settings.
- `config/settings.conf`: App-specific settings.
- `logs/app.log`: Application logs.
- `logs/error.log`: Error logs.

## How to Use

1. Make changes to any of the files in `config/` or `logs/`.
2. Jenkins will automatically detect the changes and send a notification (via email or Slack).

