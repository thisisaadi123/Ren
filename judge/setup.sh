#!/usr/bin/env bash
# One-time setup of the Ren judge on a fresh Ubuntu 24.04 server (an Oracle
# Cloud Always Free ARM VM). From your Mac:
#
#   scp judge/setup.sh ubuntu@<server-ip>:
#   ssh ubuntu@<server-ip> bash setup.sh <server-ip>
#
# Then send the code and tests with judge/deploy.sh. Safe to run again.
set -euo pipefail

IP=${1:?Usage: bash setup.sh <server public IP>}
HOST="${IP//./-}.sslip.io" # free hostname that points at the IP, so HTTPS works without a domain
ROOT=/srv/ren

echo "== Packages: Python, clang, Java 21, bubblewrap (the sandbox), Caddy (HTTPS)"
sudo apt-get update -q
sudo DEBIAN_FRONTEND=noninteractive apt-get install -yq python3 clang openjdk-21-jdk-headless bubblewrap caddy rsync curl ca-certificates iptables-persistent

echo "== Node.js 22"
if ! node -v 2>/dev/null | grep -qE '^v(2[2-9]|[3-9][0-9])\.'; then
  curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
  sudo DEBIAN_FRONTEND=noninteractive apt-get install -yq nodejs
fi

echo "== The ren-judge user and its folders"
id ren-judge >/dev/null 2>&1 || sudo useradd --system --home-dir "$ROOT" --shell /usr/sbin/nologin ren-judge
sudo mkdir -p "$ROOT/app" "$ROOT/build/tests"
sudo chown -R ren-judge:ren-judge "$ROOT"

echo "== Let the sandbox make its namespaces (Ubuntu 24.04 blocks this by default)"
sudo tee /etc/apparmor.d/ren-bwrap >/dev/null <<'EOF'
abi <abi/4.0>,
include <tunables/global>

profile ren-bwrap /usr/bin/bwrap flags=(unconfined) {
  userns,
}
EOF
sudo apparmor_parser -r /etc/apparmor.d/ren-bwrap || true
sandbox_ok() { sudo -u ren-judge bwrap --unshare-all --ro-bind /usr /usr --symlink usr/bin /bin --symlink usr/lib /lib --proc /proc --dev /dev -- /usr/bin/true; }
if ! sandbox_ok; then
  echo "   AppArmor profile wasn't enough; allowing unprivileged user namespaces instead"
  echo "kernel.apparmor_restrict_unprivileged_userns=0" | sudo tee /etc/sysctl.d/60-ren-userns.conf >/dev/null
  sudo sysctl -q --system
  sandbox_ok || { echo "The sandbox still can't start. Stopping here."; exit 1; }
fi
echo "   sandbox works"

echo "== Settings and secret (/etc/ren-judge.env)"
if ! sudo test -f /etc/ren-judge.env; then
  SECRET=$(openssl rand -hex 32)
  JAVA_HOME=$(dirname "$(dirname "$(readlink -f "$(command -v javac)")")")
  sudo tee /etc/ren-judge.env >/dev/null <<EOF
JUDGE_SECRET=$SECRET
REN_SANDBOX=1
PORT=8080
HOST=127.0.0.1
JAVA_HOME=$JAVA_HOME
EOF
  sudo chown root:ren-judge /etc/ren-judge.env
  sudo chmod 640 /etc/ren-judge.env
fi

echo "== The service (starts once judge/deploy.sh has sent the code)"
sudo tee /etc/systemd/system/ren-judge.service >/dev/null <<'EOF'
[Unit]
Description=Ren judge: DSA Run and Submit for the hosted site
After=network-online.target

[Service]
User=ren-judge
WorkingDirectory=/srv/ren/app
EnvironmentFile=/etc/ren-judge.env
ExecStart=/usr/bin/node judge/server.mjs
Restart=always
RestartSec=2
ProtectSystem=full
ProtectHome=yes
PrivateTmp=yes
MemoryMax=20G
TasksMax=4096

[Install]
WantedBy=multi-user.target
EOF
sudo systemctl daemon-reload
sudo systemctl enable ren-judge >/dev/null

echo "== HTTPS at https://$HOST"
sudo tee /etc/caddy/Caddyfile >/dev/null <<EOF
$HOST {
	reverse_proxy 127.0.0.1:8080
}
EOF
sudo systemctl restart caddy

echo "== Firewall: open 80 and 443 (Oracle's image only allows SSH)"
for port in 80 443; do
  if ! sudo iptables -C INPUT -p tcp --dport $port -m state --state NEW -j ACCEPT 2>/dev/null; then
    at=$(sudo iptables -L INPUT --line-numbers | awk '/REJECT/ {print $1; exit}')
    sudo iptables -I INPUT "${at:-1}" -p tcp --dport $port -m state --state NEW -j ACCEPT
  fi
done
sudo netfilter-persistent save >/dev/null

echo
echo "Done. Next, from your Mac:  judge/deploy.sh ubuntu@$IP"
echo "Then add these to Vercel (Settings > Environment Variables) and redeploy:"
echo "  JUDGE_URL=https://$HOST"
echo "  JUDGE_SECRET=$(sudo grep '^JUDGE_SECRET=' /etc/ren-judge.env | cut -d= -f2)"
