#!/bin/bash

# -----------------------------------------
# Trivy Scanner Script
# -----------------------------------------

WORKSPACE=${WORKSPACE:-$(pwd)}
LOG_DIR="$WORKSPACE/logs"
SCAN_OUTPUT="$LOG_DIR/trivy_scan_report.json"  # Change output file extension to .json
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

# Logging function
log() {
    echo "[$TIMESTAMP] $1" | tee -a "$LOG_DIR/trivy_scanner.log"
}

# Error handler
error_exit() {
    log "❌ ERROR: $1"
    exit 1
}

log "🚀 Starting Trivy vulnerability scan..."

# Step 1: Confirm Trivy is available
if ! command -v trivy &> /dev/null; then
    error_exit "Trivy is not installed or not in PATH."
fi

# Step 2: Run scan on current project directory, outputting in JSON format
log "🔍 Scanning project directory with Trivy..."
trivy fs --quiet -f json "$WORKSPACE" > "$SCAN_OUTPUT" || error_exit "Trivy scan failed"

# Step 3: Log scan summary
if [ -s "$SCAN_OUTPUT" ]; then
    log "✅ Trivy scan completed. Results saved to $SCAN_OUTPUT"
else
    log "⚠️ Trivy scan finished but report is empty."
fi

log "🏁 Trivy scanner script completed."
