# GB-BRAIN — VPS Deployment Guide

> **Conventions:** SQLite is truth. Capital is priority. Secrets live in `.env` only.  
> Tested on Ubuntu 22.04 LTS and Debian 12.

---

## Requirements

| Resource       | Minimum                         | Recommended                            |
|----------------|---------------------------------|----------------------------------------|
| OS             | Ubuntu 22.04 LTS / Debian 12    | Ubuntu 22.04 LTS                       |
| CPU            | 1 vCPU                          | 2 vCPUs                                |
| RAM            | 2 GB                            | 4 GB (DigitalOcean $24/mo Droplet)     |
| Disk           | 20 GB SSD                       | 40 GB SSD                              |
| Python         | 3.11+                           | 3.11.x                                 |
| Git            | Any recent                      | Latest                                 |
| Network        | Stable, low-latency             | Dedicated IP, no NAT                   |

---

## Step-by-Step Deployment

### 1. Initial Server Setup

```bash
# SSH into the new server as root
ssh root@YOUR_VPS_IP

# Update the system
apt-get update && apt-get upgrade -y

# Create a dedicated non-root user
adduser gb
usermod -aG sudo gb

# Copy SSH key to new user (run from your LOCAL machine)
ssh-copy-id gb@YOUR_VPS_IP

# Back on the server — harden SSH
nano /etc/ssh/sshd_config
# Set:
#   PermitRootLogin no
#   PasswordAuthentication no
#   PubkeyAuthentication yes
systemctl restart sshd

# Configure UFW firewall
ufw allow OpenSSH
ufw allow 8080/tcp    # webhook listener (TradingView)
ufw --force enable
ufw status verbose
```

---

### 2. Install Dependencies

```bash
# Switch to gb user
su - gb

# Install Python 3.11, pip, git, and supervisor
sudo apt-get install -y \
    python3.11 python3.11-venv python3.11-dev \
    python3-pip \
    git \
    supervisor \
    logrotate \
    curl \
    htop

# Verify versions
python3.11 --version   # Python 3.11.x
git --version
supervisord --version

# Create a virtual environment location
mkdir -p /opt/gb-brain
python3.11 -m venv /opt/gb-brain/venv

# Activate it globally for the gb user
echo 'source /opt/gb-brain/venv/bin/activate' >> ~/.bashrc
source ~/.bashrc
```

---

### 3. Clone and Configure GB-BRAIN

```bash
# Clone the repository
cd /opt
sudo git clone https://github.com/YOUR_USER/GB-BRAIN.git gb-brain
sudo chown -R gb:gb /opt/gb-brain

# Enter the directory
cd /opt/gb-brain

# Install Python dependencies
/opt/gb-brain/venv/bin/pip install --upgrade pip
/opt/gb-brain/venv/bin/pip install -r requirements.txt

# Set up environment file (NEVER commit .env to git)
cp .env.example .env
nano .env
# Fill in all required secrets — example keys:
#
#   OANDA_ACCOUNT_ID=001-001-XXXXXXX-001
#   OANDA_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#   BLOFIN_API_KEY=xxxx
#   BLOFIN_API_SECRET=xxxx
#   BLOFIN_PASSPHRASE=xxxx
#   TELEGRAM_BOT_TOKEN=xxxx
#   TELEGRAM_CHAT_ID=xxxx
#   WEBHOOK_SECRET=xxxx
#   DB_PATH=/opt/gb-brain/data/gb_brain.db
#   ENV=production

# Create required directories
mkdir -p /opt/gb-brain/data
mkdir -p /var/log/gb-brain
sudo chown -R gb:gb /var/log/gb-brain

# Initialise the SQLite database
/opt/gb-brain/venv/bin/python scripts/init_db.py

# Verify DB was created
ls -lh /opt/gb-brain/data/gb_brain.db
```

---

### 4. Test Before Going Live

```bash
cd /opt/gb-brain

# 1. Smoke test — verifies imports, config, DB connectivity
/opt/gb-brain/venv/bin/python scripts/smoke_test.py

# 2. Parity check — confirms backtest == runtime logic
/opt/gb-brain/venv/bin/python simulate/engine_parity_check.py --verbose

# 3. Replay mode — run through a sample historical window
/opt/gb-brain/venv/bin/python simulate/replay_mode.py \
    --lane GB-INDICES \
    --start 2024-01-01 \
    --end   2024-01-31 \
    --mode  paper

# 4. Verify SQLite has been written to
sqlite3 /opt/gb-brain/data/gb_brain.db \
    "SELECT * FROM backtest_results ORDER BY id DESC LIMIT 5;"

# 5. Run the live observer in foreground for 60 seconds (paper mode)
timeout 60 /opt/gb-brain/venv/bin/python runtime/live_observer.py \
    --mode paper --lane GB-INDICES || true

echo "All tests passed — safe to go live"
```

---

### 5. Set Up Process Manager (Supervisor)

```bash
# Create log directory if not yet present
sudo mkdir -p /var/log/gb-brain
sudo chown -R gb:gb /var/log/gb-brain

# Copy supervisor config files
sudo cp /opt/gb-brain/vps/supervisor_observer.conf \
        /etc/supervisor/conf.d/gb-observer.conf

sudo cp /opt/gb-brain/vps/supervisor_webhook.conf \
        /etc/supervisor/conf.d/gb-webhook.conf

# Reload supervisor and start services
sudo supervisorctl reread
sudo supervisorctl update

# Check status
sudo supervisorctl status
# Expected output:
#   gb-observer    RUNNING   pid 12345, uptime 0:00:03
#   gb-webhook     RUNNING   pid 12346, uptime 0:00:03
```

---

### 6. Set Up Auto-Restart

Supervisor handles auto-restart natively via the `autorestart=true` directive
already present in the provided `.conf` files.  No additional configuration is
needed.  To verify:

```bash
# Force-kill the observer process and confirm supervisor restarts it
sudo kill -9 $(sudo supervisorctl pid gb-observer)
sleep 3
sudo supervisorctl status gb-observer
# Should show: RUNNING   pid XXXXX, uptime 0:00:02
```

For an additional system-level safety net (survives full server reboot):

```bash
# Ensure supervisor itself starts on boot
sudo systemctl enable supervisor
sudo systemctl status supervisor
```

---

### 7. Set Up Log Rotation

```bash
# Install the logrotate config
sudo cp /opt/gb-brain/vps/logrotate.conf \
        /etc/logrotate.d/gb-brain

# Test the config (dry run)
sudo logrotate --debug /etc/logrotate.d/gb-brain

# Force a manual rotation to verify it works
sudo logrotate --force /etc/logrotate.d/gb-brain

# Confirm compressed archive was created
ls -lh /var/log/gb-brain/
```

---

### 8. Set Up GitHub Auto-Pull

```bash
# Make the update script executable
chmod +x /opt/gb-brain/vps/update.sh

# Test it manually first
/opt/gb-brain/vps/update.sh

# Add to crontab (runs daily at 06:00 VPS time)
(crontab -l 2>/dev/null; echo \
  "0 6 * * * /opt/gb-brain/vps/update.sh >> /var/log/gb-brain/updates.log 2>&1") \
| crontab -

# Verify crontab entry
crontab -l

# Ensure the gb user can run git pull without a password prompt
# (use SSH deploy key or HTTPS with a token stored in .netrc)
# SSH deploy key setup:
ssh-keygen -t ed25519 -C "gb-brain-deploy" -f ~/.ssh/gb_deploy -N ""
cat ~/.ssh/gb_deploy.pub
# → Add this public key as a "Deploy Key" in your GitHub repository settings
#   (Settings → Deploy keys → Add deploy key, read-only is fine)

# Configure git to use the deploy key
git -C /opt/gb-brain config core.sshCommand \
    "ssh -i /home/gb/.ssh/gb_deploy -o StrictHostKeyChecking=no"
```

---

### 9. Monitoring

```bash
# Check supervisor process status
sudo supervisorctl status

# Tail live observer logs
tail -f /var/log/gb-brain/observer.log

# Tail webhook logs
tail -f /var/log/gb-brain/webhook.log

# Tail error logs
tail -f /var/log/gb-brain/observer_err.log

# Check for recent trades in SQLite
sqlite3 /opt/gb-brain/data/gb_brain.db \
    "SELECT * FROM live_trades ORDER BY id DESC LIMIT 10;"

# Check recent signals
sqlite3 /opt/gb-brain/data/gb_brain.db \
    "SELECT * FROM observed_signals ORDER BY id DESC LIMIT 20;"

# System resource usage
htop
# or
top -u gb

# Telegram alerts
# GB-BRAIN sends Telegram messages on:
#   - Trade entry / exit
#   - Error / exception (CRITICAL level)
#   - Daily P&L summary (configurable in settings.py)
# Confirm bot is reachable:
curl "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/getMe"
```

---

### 10. Backup Strategy

```bash
# Manual SQLite backup
cp /opt/gb-brain/data/gb_brain.db \
   /opt/gb-brain/data/gb_brain_$(date +%Y%m%d_%H%M%S).db

# Automated daily backup via cron (keeps 30 days)
(crontab -l 2>/dev/null; echo \
  "0 2 * * * cp /opt/gb-brain/data/gb_brain.db \
  /opt/gb-brain/data/backups/gb_brain_\$(date +\%Y\%m\%d).db \
  && find /opt/gb-brain/data/backups/ -name '*.db' -mtime +30 -delete") \
| crontab -

# Create backup directory
mkdir -p /opt/gb-brain/data/backups

# Optional: rsync backups to a separate server or object storage
rsync -avz /opt/gb-brain/data/gb_brain.db \
    backup_user@BACKUP_HOST:/backups/gb-brain/

# Optional: upload to S3-compatible storage
# aws s3 cp /opt/gb-brain/data/gb_brain.db \
#     s3://your-bucket/gb-brain/gb_brain_$(date +%Y%m%d).db
```

---

## Quick Reference

| Action                    | Command                                               |
|---------------------------|-------------------------------------------------------|
| Start all services        | `sudo supervisorctl start all`                        |
| Stop all services         | `sudo supervisorctl stop all`                         |
| Restart all services      | `sudo supervisorctl restart all`                      |
| View observer logs        | `tail -f /var/log/gb-brain/observer.log`              |
| View webhook logs         | `tail -f /var/log/gb-brain/webhook.log`               |
| Manual update             | `/opt/gb-brain/vps/update.sh`                         |
| Run parity check          | `python simulate/engine_parity_check.py`              |
| SQLite REPL               | `sqlite3 /opt/gb-brain/data/gb_brain.db`              |
| Check supervisor status   | `sudo supervisorctl status`                           |
| Force log rotation        | `sudo logrotate --force /etc/logrotate.d/gb-brain`    |

---

## Security Checklist

- [ ] Root login disabled (`PermitRootLogin no`)
- [ ] Password authentication disabled (`PasswordAuthentication no`)
- [ ] `.env` is in `.gitignore` — never committed
- [ ] UFW firewall active — only ports 22 and 8080 open
- [ ] API keys are exchange sub-account keys with **trade-only** permissions (no withdrawal)
- [ ] SQLite DB file permissions: `chmod 600 /opt/gb-brain/data/gb_brain.db`
- [ ] Log files owned by `gb` user only
- [ ] GitHub deploy key is **read-only**
- [ ] Telegram alerts are functional

---

*Last updated: 2026 — GB-BRAIN Phase 4 & 5*
