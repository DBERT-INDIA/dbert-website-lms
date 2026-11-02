#!/bin/bash
# ==============================================================================
# DBERT Ecosystem — Deployment Entry Point
# (Redirects legacy deploy_ec2.sh to unified deploy_ec2_unified.sh)
# ==============================================================================
set -Eeuo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "[*] Invoking unified deployment script: $SCRIPT_DIR/deploy_ec2_unified.sh..."
exec bash "$SCRIPT_DIR/deploy_ec2_unified.sh" "$@"
