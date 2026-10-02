"""Reads the few problem.yaml fields the walkthrough tools need, using the `yaml` npm package via node."""
import json
import subprocess


def load(path):
    code = "const Y=require('yaml');const fs=require('fs');process.stdout.write(JSON.stringify(Y.parse(fs.readFileSync(process.argv[1],'utf8'))))"
    out = subprocess.run(["node", "-e", code, path], capture_output=True, text=True, cwd=__import__("os").path.abspath(__import__("os").path.join(__import__("os").path.dirname(__file__), "..", "..", "..", "..", "..")))
    return json.loads(out.stdout)
