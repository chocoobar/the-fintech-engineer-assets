#!/usr/bin/env python3
"""Rasterize a self-contained HTML card to a tightly-cropped PNG via headless Chrome.

Renders on an oversized pure-white canvas, screenshots at a high device
scale for crisp embedding, then autocrops the flat-white margin so the
output fits snugly around whatever card/doc the HTML actually draws.
"""
import argparse
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

CHROME_CANDIDATES = [
    # macOS
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    # Windows
    "C:/Program Files/Google/Chrome/Application/chrome.exe",
    "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe",
    # Linux (apt/dnf google-chrome-stable, Debian/Ubuntu chromium package,
    # and Playwright/Puppeteer's bundled Chromium — covers most cloud
    # sandboxes/CI containers, including a Claude Code cloud session)
    "/usr/bin/google-chrome-stable",
    "/usr/bin/google-chrome",
    "/usr/bin/chromium-browser",
    "/usr/bin/chromium",
    "/snap/bin/chromium",
]

# An explicit override always wins (set this if Chrome lives somewhere
# none of the above or PATH lookup finds — e.g. a nonstandard sandbox
# install).
_env_override = os.environ.get("CHROME_PATH") or os.environ.get("PUPPETEER_EXECUTABLE_PATH")

CHROME = (
    _env_override
    or next((p for p in CHROME_CANDIDATES if pathlib.Path(p).exists()), None)
    or shutil.which("google-chrome-stable")
    or shutil.which("google-chrome")
    or shutil.which("chromium-browser")
    or shutil.which("chromium")
    or CHROME_CANDIDATES[0]
)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("html_path")
    ap.add_argument("png_path")
    ap.add_argument("--scale", type=float, default=2.0)
    ap.add_argument("--window", default="1600,2400", help="oversized window WxH the card renders inside")
    args = ap.parse_args()

    html_path = pathlib.Path(args.html_path).resolve()
    out_path = pathlib.Path(args.png_path).resolve()

    with tempfile.TemporaryDirectory() as td:
        raw_png = pathlib.Path(td) / "raw.png"
        cmd = [
            CHROME,
            "--headless=new",
            "--disable-gpu",
            # Harmless on macOS/Windows; required on most Linux containers/
            # cloud sandboxes, where Chrome usually runs as root and its
            # sandbox refuses to start without this. We're only ever
            # rendering our own local file:// HTML here, never browsing
            # untrusted external content, so this doesn't weaken anything
            # that actually matters for this use case.
            "--no-sandbox",
            "--hide-scrollbars",
            "--force-device-scale-factor=%s" % args.scale,
            "--default-background-color=FFFFFFFF",
            "--virtual-time-budget=3000",
            "--run-all-compositor-stages-before-draw",
            f"--screenshot={raw_png}",
            f"--window-size={args.window}",
            f"file://{html_path}",
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
        if result.returncode != 0 or not raw_png.exists():
            sys.exit(f"Chrome headless screenshot failed (exit {result.returncode}).\n"
                      f"stdout: {result.stdout}\nstderr: {result.stderr}")

        from PIL import Image, ImageChops

        im = Image.open(raw_png).convert("RGB")
        bg = Image.new("RGB", im.size, (255, 255, 255))
        diff = ImageChops.difference(im, bg)
        bbox = diff.getbbox()
        if bbox:
            pad = 24
            l, t, r, b = bbox
            l = max(0, l - pad)
            t = max(0, t - pad)
            r = min(im.width, r + pad)
            b = min(im.height, b + pad)
            im = im.crop((l, t, r, b))
        out_path.parent.mkdir(parents=True, exist_ok=True)
        im.save(out_path)

    print(f"wrote {out_path} ({out_path.stat().st_size} bytes, {im.size[0]}x{im.size[1]})")


if __name__ == "__main__":
    main()
