#!/usr/bin/env python3
"""Checks the store before umbrelOS reads it.

umbrelOS skips an app whose ID doesn't start with the store's ID, and shows
Umbrel's own gallery images unless the manifest points to ours, so mistakes
here don't fail loudly on the device.
"""

import re
import sys
from pathlib import Path

import yaml

RAW = "https://raw.githubusercontent.com/accordion-suite/accordion-umbrel/main/"
root = Path(__file__).resolve().parent.parent
problems = []


def load(path):
    try:
        return yaml.safe_load(path.read_text()) or {}
    except (OSError, yaml.YAMLError) as e:
        problems.append(f"{path.relative_to(root)}: {e}")
        return {}


def check_image_url(app, field, url):
    if not isinstance(url, str) or not url.startswith(RAW):
        problems.append(f"{app}: {field} should start with {RAW}, not {url!r}")
        return
    if not (root / url[len(RAW):]).is_file():
        problems.append(f"{app}: {field} points to {url[len(RAW):]}, which isn't in the repo")


store = load(root / "umbrel-app-store.yml")
store_id = store.get("id")
if not store_id or not store.get("name"):
    problems.append("umbrel-app-store.yml: needs an id and a name")

for manifest in sorted(root.glob("*/umbrel-app.yml")):
    folder = manifest.parent.name
    app = load(manifest)
    if app.get("id") != folder:
        problems.append(f"{folder}: id is {app.get('id')!r}, but it has to match its folder")
    if store_id and not folder.startswith(f"{store_id}-"):
        problems.append(f"{folder}: the app's ID has to start with {store_id}-")
    check_image_url(folder, "icon", app.get("icon"))
    for i, url in enumerate(app.get("gallery") or []):
        check_image_url(folder, f"gallery[{i}]", url)

    compose = load(manifest.parent / "docker-compose.yml")
    for name, service in (compose.get("services") or {}).items():
        image = (service or {}).get("image")
        # umbrelOS supplies app_proxy's image itself.
        if image is not None and not re.search(r":[^/@]+@sha256:[0-9a-f]{64}$", image):
            problems.append(f"{folder}: service {name} should pin its image by tag and digest, not {image!r}")

for p in problems:
    print(p, file=sys.stderr)
sys.exit(1 if problems else 0)
