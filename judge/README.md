# Ren judge server

Runs DSA **Run** and **Submit** for the hosted site, the same way `npm start` runs them on your Mac: Python, Java, C++ and C, the same harnesses, every hidden test.

```
Browser ──► Vercel (server.js) ──HTTPS + JUDGE_SECRET──► judge server (judge/server.mjs)
             pages, accounts, SQL                         backend/practice/dsa/tools/judge.mjs
                                                          each run inside a bubblewrap sandbox
```

Vercel can't do this itself: it has no Python, Java or C compilers, the hidden tests are about 1.4 GB, and people's code must never run unsandboxed next to the site's secrets. SQL doesn't need this server; it runs on Vercel directly.

It's built for a free **Oracle Cloud Always Free** ARM VM (4 cores, 24 GB RAM, Ubuntu 24.04).

## Files

| File | What it does |
|---|---|
| `server.mjs` | The HTTP server: `POST /run`, `POST /submit`, `GET /languages`, `GET /health`. Allows one run per person at a time and 60 per 10 minutes, runs at most `cores - 1` at once, and holds up to 20 more in a queue |
| `setup.sh` | One-time server setup: packages, the `ren-judge` user, the sandbox, the service, HTTPS, the firewall |
| `deploy.sh` | Run from your Mac: sends your last commit and the built tests, then restarts the server |
| `sandbox-test.mjs` | Run on the server: sends code that tries to escape, and checks that every attempt fails |

## The sandbox

When `REN_SANDBOX=1`, every program that runs someone's code starts inside [bubblewrap](https://github.com/containers/bubblewrap). That covers the Python runner, the compiled C/C++ program, the JVM and the compilers. The wrapper is `jailed()` in `backend/practice/dsa/tools/lib/run.mjs`.

- **No network.** It runs in its own network namespace with no interfaces.
- **No secrets.** The environment is cleared, `/etc` isn't mounted (except what the linker and Java need), and the hidden tests aren't mounted.
- **Read-only system.** `/usr` is read-only. The program sees only its own folder; a compiler can write only into its own output folder.
- **Its own process tree.** Killing the sandbox kills everything inside it.
- **Limits.** 6 GB of address space, 256 processes, 50 s of CPU, 50 s of wall clock, 64 MB files.

Compiled programs are cached by a hash of their code, so Submit right after Run doesn't compile again. Entries unused for a day are deleted.

## Setting it up (once)

### 1. Create the free VM on Oracle Cloud

1. Sign up at [cloud.oracle.com](https://cloud.oracle.com). A card is needed to verify your identity; Always Free resources aren't charged. Pick a **home region** close to Vercel's default (US East, Ashburn), because you can't change it later.
2. Recommended: **Upgrade to Pay As You Go** (Billing → Upgrade). Always Free resources stay free, and Oracle stops reclaiming "idle" free VMs. Then add a **budget alert** of $1 (Billing → Budgets), so anything unexpected emails you.
3. **Compute → Instances → Create instance**:
   - Image: **Canonical Ubuntu 24.04**
   - Shape: **Ampere → VM.Standard.A1.Flex**, **4 OCPUs, 24 GB memory** (the Always Free maximum)
   - Networking: keep the defaults, with a public IPv4 address
   - SSH keys: upload your public key (`~/.ssh/id_ed25519.pub`; make one with `ssh-keygen -t ed25519` if you don't have one)
   - If it says *out of capacity*, try another availability domain or try again later.
4. Open the ports: the instance's **subnet → Security List → Add Ingress Rules**: source `0.0.0.0/0`, TCP, destination ports **80** and **443**.
5. Note the instance's **public IP**.

### 2. Set up the server

From the repo on your Mac:

```sh
scp judge/setup.sh ubuntu@<ip>:
ssh ubuntu@<ip> bash setup.sh <ip>
```

At the end it prints `JUDGE_URL` and `JUDGE_SECRET`. Keep them for step 5.

### 3. Send the code and tests

The tests are in `backend/practice/dsa/build/tests/`. If you don't have them yet, build them first: `npm run check:dsa -- --write-expected --jobs 6 --quiet`. Then:

```sh
judge/deploy.sh ubuntu@<ip>
```

The first upload is about 1.4 GB (compressed on the way). Later runs only send what changed. It ends by printing `{"ok":true,...}`.

### 4. Check the sandbox

```sh
ssh ubuntu@<ip>
cd /srv/ren/app && sudo -u ren-judge env $(sudo cat /etc/ren-judge.env | xargs) node judge/sandbox-test.mjs
```

Every line must be ✓ and it must end with *The sandbox holds.* If not, don't do step 5.

### 5. Connect the site

In Vercel → your project → **Settings → Environment Variables**, add:

| Name | Value |
|---|---|
| `JUDGE_URL` | `https://<ip-with-dashes>.sslip.io`, as `setup.sh` printed it |
| `JUDGE_SECRET` | as `setup.sh` printed it |

Then **Deployments → ⋯ → Redeploy**. Problem pages now offer all four languages, and Run and Submit go to the judge.

## Day to day

- **After adding or changing problems:** commit, rebuild the tests locally (`npm run check:dsa -- --write-expected ...`), then `judge/deploy.sh ubuntu@<ip>`.
- **Is it up?** `curl https://<ip-with-dashes>.sslip.io/health`
- **Logs:** `ssh ubuntu@<ip> journalctl -u ren-judge -f` (and `-u caddy` for HTTPS).
- **Change the secret:** edit `/etc/ren-judge.env`, then `sudo systemctl restart ren-judge`, then update it in Vercel and redeploy.
- **If the judge is down,** the site keeps working; Run and Submit say *"The code runner is offline right now."*

## Trying it on your Mac

There's no sandbox on macOS, so this is for checking the wiring only:

```sh
JUDGE_SECRET=$(openssl rand -hex 32) PORT=8080 node judge/server.mjs
# in another terminal, with the same secret:
JUDGE_URL=http://127.0.0.1:8080 JUDGE_SECRET=<same> npm start
```
