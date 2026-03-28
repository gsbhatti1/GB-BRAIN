#!/usr/bin/env bash
# GB-BRAIN — Safe VPS Update Script
# ===================================
# Pulls latest code from origin/main, reinstalls dependencies,
# and restarts supervisor services.  Only acts if there are real changes.
#
# Cron usage:
#   0 6 * * * /opt/gb-brain/vps/update.sh >> /var/log/gb-brain/updates.log 2>&1
#
# Manual usage:
#   /opt/gb-brain/vps/update.sh

set -e

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

PROJECT_DIR="/opt/gb-brain"
VENV_PIP="${PROJECT_DIR}/venv/bin/pip"
BRANCH="main"

# ---------------------------------------------------------------------------
# Timestamp header
# ---------------------------------------------------------------------------

echo ""
echo "============================================="
echo "  GB-BRAIN Update Check"
echo "  Time   : $(date '+%Y-%m-%d %H:%M:%S %Z')"
echo "  Dir    : ${PROJECT_DIR}"
echo "  Branch : ${BRANCH}"
echo "============================================="

# ---------------------------------------------------------------------------
# Ensure we are in the right directory
# ---------------------------------------------------------------------------

if [[ ! -d "${PROJECT_DIR}/.git" ]]; then
    echo "ERROR: ${PROJECT_DIR} is not a git repository."
    exit 1
fi

cd "${PROJECT_DIR}"

# ---------------------------------------------------------------------------
# Fetch latest refs without changing working tree
# ---------------------------------------------------------------------------

echo ""
echo "[1/5] Fetching from origin …"
git fetch origin "${BRANCH}" --quiet

# ---------------------------------------------------------------------------
# Check for differences
# ---------------------------------------------------------------------------

echo "[2/5] Checking for changes …"
CHANGED_FILES="$(git diff HEAD "origin/${BRANCH}" --name-only)"

if [[ -z "${CHANGED_FILES}" ]]; then
    echo ""
    echo "  Already up to date — no changes on origin/${BRANCH}."
    echo "============================================="
    echo "  No update needed."
    echo "  Time : $(date '+%Y-%m-%d %H:%M:%S %Z')"
    echo "============================================="
    echo ""
    exit 0
fi

echo ""
echo "  Changes detected:"
echo "${CHANGED_FILES}" | sed 's/^/    + /'

# ---------------------------------------------------------------------------
# Stop services
# ---------------------------------------------------------------------------

echo ""
echo "[3/5] Stopping supervisor services …"
sudo supervisorctl stop all

# ---------------------------------------------------------------------------
# Pull latest code
# ---------------------------------------------------------------------------

echo "[4/5] Pulling latest code from origin/${BRANCH} …"
git pull origin "${BRANCH}"

# ---------------------------------------------------------------------------
# Reinstall dependencies (quiet — only shows new installs)
# ---------------------------------------------------------------------------

echo "[5/5] Installing/updating Python dependencies …"
"${VENV_PIP}" install -r "${PROJECT_DIR}/requirements.txt" --quiet

# ---------------------------------------------------------------------------
# Start services
# ---------------------------------------------------------------------------

echo ""
echo "  Starting supervisor services …"
sudo supervisorctl start all
sleep 2
sudo supervisorctl status

# ---------------------------------------------------------------------------
# Done
# ---------------------------------------------------------------------------

echo ""
echo "============================================="
echo "  UPDATE COMPLETE"
echo "  Time    : $(date '+%Y-%m-%d %H:%M:%S %Z')"
echo "  Changes :"
echo "${CHANGED_FILES}" | sed 's/^/    · /'
echo "============================================="
echo ""
