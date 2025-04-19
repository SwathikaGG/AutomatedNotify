<<<<<<< HEAD
#!/bin/bash
source /home/user/myenv/bin/activate
python /home/user/automatic-file-change-notification/scripts/log_generator.py
python /home/user/automatic-file-change-notification/src/notifier.py
deactivate
=======
#!/bin/bash

# -----------------------------------------
# Enhanced Automation Script
# -----------------------------------------

LOG_FILE="logs/automation.log"
VENV_DIR="myenv"
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

log() {
    echo "[$TIMESTAMP] $1" | tee -a "$LOG_FILE"
}

error_exit() {
    log "❌ ERROR: $1"
    exit 1
}

log "🚀 Starting Automation Script..."

# Step 1: Activate virtual environment
if [ -d "$VENV_DIR" ]; then
    log "🟢 Activating Python virtual environment..."
    source "$VENV_DIR/bin/activate" || error_exit "Failed to activate virtual environment"
else
    error_exit "Virtual environment not found in $VENV_DIR"
fi

# Step 2: Run log generator
log "📝 Running log_generator.py..."
python3 src/log_generator.py || error_exit "log_generator.py failed"

# Step 3: Run notifier
log "📢 Running notifier.py..."
python3 src/notifier.py || error_exit "notifier.py failed"

log "✅ Automation complete!"
>>>>>>> 8a1c0b0 (Enhance run_all.sh with error handling, logging, and robustness)
