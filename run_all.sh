#!/bin/bash

# -----------------------------------------
# Enhanced Automation Script for Jenkins
# -----------------------------------------

# Set up paths
WORKSPACE=${WORKSPACE:-/home/user/automatic-file-change-notification}
LOG_FILE="$WORKSPACE/logs/automation.log"
VENV_DIR="$WORKSPACE/myenv"
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

# Logging function
log() {
    echo "[$TIMESTAMP] $1" | tee -a "$LOG_FILE"
}

# Error handler
error_exit() {
    log "❌ ERROR: $1"
    exit 1
}

log "🚀 Starting Automation Script..."

# Step 1: Ensure log directory exists
mkdir -p "$WORKSPACE/logs"

# Step 2: Create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    log "🟠 Virtual environment not found. Creating one..."
    python3 -m venv "$VENV_DIR" || error_exit "Failed to create virtual environment"
fi

# Step 3: Activate virtual environment
log "🟢 Activating virtual environment..."
source "$VENV_DIR/bin/activate" || error_exit "Failed to activate virtual environment"

# Step 4: Upgrade pip
log "⬆️  Upgrading pip..."
pip install --upgrade pip || error_exit "Failed to upgrade pip"

# Step 5: Install dependencies
REQ_FILE="$WORKSPACE/requirements.txt"
if [ -f "$REQ_FILE" ]; then
    log "📦 Installing dependencies from requirements.txt..."
    pip install -r "$REQ_FILE" || error_exit "Failed to install dependencies"
else
    log "⚠️ No requirements.txt found. Skipping dependency installation."
fi

# Step 6: Verify MySQL connector is installed
log "🔎 Verifying mysql-connector-python installation..."
pip show mysql-connector-python >/dev/null || error_exit "mysql-connector-python is NOT installed!"

# Step 7: Run log generator script
LOG_GEN_SCRIPT="$WORKSPACE/src/log_generator.py"  # Updated to src
if [ -f "$LOG_GEN_SCRIPT" ]; then
    log "📝 Running log_generator.py..."
    python3 "$LOG_GEN_SCRIPT" || error_exit "log_generator.py failed"
else
    error_exit "log_generator.py not found at $LOG_GEN_SCRIPT"
fi

# Step 8: Run notifier script
NOTIFIER_SCRIPT="$WORKSPACE/src/notifier.py"  # Updated to src
if [ -f "$NOTIFIER_SCRIPT" ]; then
    log "📢 Running notifier.py..."
    python3 "$NOTIFIER_SCRIPT" || error_exit "notifier.py failed"
else
    error_exit "notifier.py not found at $NOTIFIER_SCRIPT"
fi

# Step 9: Deactivate virtual environment
log "🛑 Deactivating virtual environment..."
deactivate || log "⚠️ Failed to deactivate virtual environment (optional)."

log "✅ Automation complete!"
