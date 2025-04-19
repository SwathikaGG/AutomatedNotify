#!/bin/bash
source /home/user/myenv/bin/activate
python /home/user/automatic-file-change-notification/scripts/log_generator.py
python /home/user/automatic-file-change-notification/src/notifier.py
deactivate
