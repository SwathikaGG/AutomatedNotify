#!/bin/bash

# -----------------------------------------
# Enhanced Automation Script
# -----------------------------------------

LOG_FILE="logs/automation.log"
VENV_DIR="$WORKSPACE/myenv"
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

log() {
    echo "[$TIMESTAMP] $1" | tee -a "$LOG_FILE"
}

error_exit() {
    log "❌ ERROR: $1"
    exit 1
}

log "🚀 Starting Automation Script..."

# Step 1: Check and create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    log "🟠 Virtual environment not found. Creating a new one..."
    python3 -m venv "$VENV_DIR" || error_exit "Failed to create virtual environment"
fi

# Step 2: Activate virtual environment
log "🟢 Activating Python virtual environment..."
source "$VENV_DIR/bin/activate" || error_exit "Failed to activate virtual environment"

# Step 3: Install dependencies if requirements.txt exists
if [ -f "$WORKSPACE/requirements.txt" ]; then
    log "📦 Installing dependencies from requirements.txt..."
    pip install -r "$WORKSPACE/requirements.txt" || error_exit "Failed to install dependencies"
else
    log "⚠️ No requirements.txt found. Skipping dependencies installation."
fi

# Step 4: Run log generator
log "📝 Running log_generator.py..."
python3 "$WORKSPACE/scripts/log_generator.py" || error_exit "log_generator.py failed"

# Step 5: Run notifier
log "📢 Running notifier.py..."
python3 "$WORKSPACE/src/notifier.py" || error_exit "notifier.py failed"

log "✅ Automation complete!"

# Deactivate the virtual environment
deactivate || log "⚠️ Failed to deactivate virtual environment (optional)."
