#!/usr/bin/env bash
# Send the judge your last commit and the built DSA tests, then restart it.
# Run from your Mac, after judge/setup.sh, and again whenever problems change:
#
#   judge/deploy.sh ubuntu@<server-ip>
#
# The repo is private, so the server never pulls from GitHub: the code goes
# over SSH (git archive of HEAD, so uncommitted changes aren't sent) and the
# tests go with rsync (only changed files after the first time).
set -euo pipefail

SERVER=${1:?Usage: judge/deploy.sh ubuntu@<server-ip>}
cd "$(dirname "$0")/.."
TESTS=backend/practice/dsa/build/tests

if [ ! -d "$TESTS" ]; then
  echo "No $TESTS yet. Build it first: npm run check:dsa -- --write-expected --jobs 6 --quiet"
  exit 1
fi
git diff --quiet HEAD -- judge backend/practice/dsa package.json ||
  echo "Note: you have uncommitted changes; the server gets your last commit ($(git rev-parse --short HEAD))."

echo "== Code ($(git rev-parse --short HEAD))"
git archive --format=tar HEAD judge backend/practice/dsa package.json package-lock.json |
  ssh "$SERVER" 'set -e
    sudo -u ren-judge rm -rf /srv/ren/app.next
    sudo -u ren-judge mkdir /srv/ren/app.next
    sudo -u ren-judge tar -x -C /srv/ren/app.next
    sudo -u ren-judge ln -s /srv/ren/build /srv/ren/app.next/backend/practice/dsa/build
    cd /srv/ren/app.next && sudo -H -u ren-judge npm ci --omit=dev --silent --no-audit --no-fund'

echo "== Tests (about 1.4 GB the first time, compressed on the way)"
rsync -az --delete --rsync-path="sudo -u ren-judge rsync" "$TESTS/" "$SERVER:/srv/ren/build/tests/"

echo "== Switch over and restart"
ssh "$SERVER" 'set -e
  sudo -u ren-judge rm -rf /srv/ren/app.old
  if [ -d /srv/ren/app ]; then sudo -u ren-judge mv /srv/ren/app /srv/ren/app.old; fi
  sudo -u ren-judge mv /srv/ren/app.next /srv/ren/app
  sudo systemctl restart ren-judge
  sleep 2
  curl -fsS localhost:8080/health && echo
  sudo -u ren-judge rm -rf /srv/ren/app.old'
