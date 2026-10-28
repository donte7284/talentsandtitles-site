#!/usr/bin/env bash
# One-time setup per container for the HyperFrames engine (fonts, GSAP, CLI, a headless Chrome).
# Writes the Chrome path to hf/.chrome so build.py can find it.
set -e
cd "$(dirname "$0")"
npm install --no-fund --no-audit --loglevel=error
CHROME="${HYPERFRAMES_BROWSER_PATH:-}"
# 1) a Playwright Chromium the environment already installed
[ -z "$CHROME" ] && CHROME=$(ls -d ~/.cache/ms-playwright/chromium-*/chrome-linux*/chrome 2>/dev/null | tail -1 || true)
# 2) the Chromium that ships inside the @sparticuz/chromium npm package (no extra download)
[ -z "$CHROME" ] && CHROME=$(node --input-type=module -e "import c from '@sparticuz/chromium'; console.log(await c.executablePath())" 2>/dev/null || true)
# 3) HyperFrames' own download
[ -z "$CHROME" ] && CHROME=$(npx hyperframes browser path 2>/dev/null | tail -1 || true)
echo "$CHROME" > .chrome
HYPERFRAMES_BROWSER_PATH="$CHROME" npx hyperframes doctor 2>&1 | grep -E "Chrome|FFmpeg" || true
echo "chrome: $CHROME"
