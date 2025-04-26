#!/bin/bash

# -----------------------------------------
# Enhanced Automation Script for Jenkins
# -----------------------------------------

# Step 0: Determine workspace path
WORKSPACE=${WORKSPACE:-$(pwd)}
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
    log "🟠 Virtual environment not found. Creating one at $VENV_DIR..."
    python3 -m venv "$VENV_DIR" || error_exit "Failed to create virtual environment"
fi

# Step 3: Activate virtual environment
if [ -f "$VENV_DIR/bin/activate" ]; then
    log "🟢 Activating virtual environment..."
    source "$VENV_DIR/bin/activate" || error_exit "Failed to activate virtual environment"
else
    error_exit "Virtual environment activate script not found at $VENV_DIR/bin/activate"
fi

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
LOG_GEN_SCRIPT="$WORKSPACE/src/log_generator.py"
if [ -f "$LOG_GEN_SCRIPT" ]; then
    log "📝 Running log_generator.py..."
    python3 "$LOG_GEN_SCRIPT" || error_exit "log_generator.py failed"
else
    error_exit "log_generator.py not found at $LOG_GEN_SCRIPT"
fi

# Step 8: Run notifier script
NOTIFIER_SCRIPT="$WORKSPACE/src/notifier.py"
if [ -f "$NOTIFIER_SCRIPT" ]; then
    log "📢 Running notifier.py..."
    python3 "$NOTIFIER_SCRIPT" || error_exit "notifier.py failed"
else
    error_exit "notifier.py not found at $NOTIFIER_SCRIPT"
fi
# Step 9: Run Trivy filesystem scan (offline)


TRIVY_PATH_TO_SCAN="/home/user/automatic-file-change-notification"
TRIVY_OUTPUT="/home/user/automatic-file-change-notification/logs/trivy_scan_report.json"

log "🔍 Running Trivy filesystem scan on $TRIVY_PATH_TO_SCAN..."
trivy fs --offline --severity CRITICAL,HIGH,MEDIUM --format json "$TRIVY_PATH_TO_SCAN" > "$TRIVY_OUTPUT" 2>>"$LOG_FILE"

if [ $? -eq 0 ]; then
    log "🧪 Trivy scan completed. Report saved to $TRIVY_OUTPUT"
else
    log "⚠️ Trivy scan failed. Check log for details."
fi

'''# Set default WORKSPACE if not set
if [ -z "$WORKSPACE" ]; then
  WORKSPACE="/home/user/automatic-file-change-notification"
fi

TRIVY_PATH_TO_SCAN="$WORKSPACE"
TRIVY_OUTPUT="$WORKSPACE/logs/trivy_scan_report.json"

log "🔍 Running Trivy filesystem scan on $TRIVY_PATH_TO_SCAN..."
trivy fs --offline --severity CRITICAL,HIGH,MEDIUM --format json "$TRIVY_PATH_TO_SCAN" > "$TRIVY_OUTPUT" 2>>"$LOG_FILE"


if [ $? -eq 0 ]; then
    log "🧪 Trivy scan completed. Report saved to $TRIVY_OUTPUT"
else
    log "⚠️ Trivy scan failed. Check log for details."
fi'''

# Step 10: Parse Trivy vulnerabilities
TRIVY_PARSER_SCRIPT="$WORKSPACE/src/trivy_parser.py"
if [ -f "$TRIVY_PARSER_SCRIPT" ]; then
    log "📋 Parsing Trivy vulnerabilities and inserting into MySQL..."
    python3 "$TRIVY_PARSER_SCRIPT" || error_exit "trivy_parser.py failed"
else
    error_exit "trivy_parser.py not found at $TRIVY_PARSER_SCRIPT"
fi

# Step 11: Deactivate virtual environment if available
log "🛑 Deactivating virtual environment..."
type deactivate &>/dev/null && deactivate || log "⚠️ Virtual environment wasn't active or deactivate failed."

log "✅ Automation complete!"
