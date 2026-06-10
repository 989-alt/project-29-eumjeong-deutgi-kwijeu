#!/usr/bin/env python3
"""Playwright e2e for project-29 음정 듣기 퀴즈.

Verifies:
  - page loads with no console/page errors
  - start overlay unlocks audio + dismisses
  - segmented controls switch state (aria-pressed)
  - clicking a choice records attempt and updates score
  - feedback area appears with result
  - difficulty change resets question + choices count
  - mode switch (single/compare/chord) changes choice labels
  - reset clears score
  - keyboard SVG highlights at least one key after answer
Saves screenshots under tests/screenshots/.
"""
import json
import os
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright, expect

ROOT = Path(__file__).resolve().parent.parent
SCREENSHOTS = ROOT / "tests" / "screenshots"
SCREENSHOTS.mkdir(parents=True, exist_ok=True)

URL = os.environ.get("APP_URL", "http://127.0.0.1:5181/")

# Noise filter: external CDN warnings, autoplay policy info, etc.
ENV_NOISE_SUBSTR = [
    "cdn.tailwindcss.com",
    "Autoplay",
    "AudioContext",
    "favicon",
    "fonts.googleapis.com",
    "fonts.gstatic.com",
    "ERR_CERT_AUTHORITY_INVALID",
    "unpkg.com/tone",
    "Tone.js failed to load",
    "Audio init deferred",
    "Failed to load resource",
]


def is_noise(msg: str) -> bool:
    return any(s in msg for s in ENV_NOISE_SUBSTR)


def shot(page, name: str) -> None:
    p = SCREENSHOTS / f"{name}.png"
    page.screenshot(path=str(p), full_page=True)
    print(f"  shot: {p.name}")


def main() -> int:
    errors: list[str] = []
    bugs: list[str] = []

    with sync_playwright() as pw:
        browser = pw.chromium.launch(args=[
            "--autoplay-policy=no-user-gesture-required",
            "--use-fake-ui-for-media-stream",
        ])
        context = browser.new_context(viewport={"width": 1280, "height": 900})
        page = context.new_page()

        page.on("pageerror", lambda exc: errors.append(f"pageerror: {exc}"))

        def on_console(msg):
            if msg.type in ("error", "warning"):
                text = msg.text
                if not is_noise(text):
                    errors.append(f"console.{msg.type}: {text}")

        page.on("console", on_console)
        page.on("requestfailed", lambda req: None if is_noise(req.url) else errors.append(f"requestfailed: {req.url} {req.failure}"))

        print(f"→ navigating {URL}")
        page.goto(URL, wait_until="domcontentloaded")
        page.wait_for_load_state("networkidle", timeout=10000)
        shot(page, "01-loaded")

        # 1. Start overlay visible
        overlay = page.locator("#start-overlay")
        if not overlay.is_visible():
            bugs.append("[P0] start overlay should be visible on first load")
        page.locator("#btn-start").click()
        page.wait_for_timeout(400)
        if overlay.is_visible():
            bugs.append("[P0] start overlay should disappear after clicking start")
        shot(page, "02-first-question")

        # 2. Choices appear (3 buttons for default 3-note single mode)
        choices = page.locator("#choices .choice")
        expect(choices).to_have_count(3, timeout=3000)

        # 3. Click first choice → score updates, feedback appears
        choices.nth(0).click()
        page.wait_for_timeout(300)
        fb = page.locator("#feedback")
        if not fb.is_visible():
            bugs.append("[P0] feedback area should appear after answering")
        attempt = page.locator("#s-attempt").inner_text()
        if attempt != "1":
            bugs.append(f"[P0] attempt counter should be 1, got {attempt!r}")
        rate_text = page.locator("#s-rate").inner_text()
        if rate_text == "—" or not rate_text.endswith("%"):
            bugs.append(f"[P1] rate should be % after first answer, got {rate_text!r}")
        # Mini keyboard should have a lit key
        lit = page.locator("[data-midi].lit").count()
        if lit < 1:
            bugs.append("[P1] mini keyboard should highlight at least 1 key after answer")
        shot(page, "03-after-answer")

        # 4. Next question
        page.locator("#btn-next").click()
        page.wait_for_timeout(300)
        if fb.is_visible():
            bugs.append("[P1] feedback should hide on next question")
        cap = page.locator("#quiz-caption").inner_text()
        if "2" not in cap:
            bugs.append(f"[P1] question number should advance to 2, caption={cap!r}")

        # 5. Switch difficulty to 7
        page.locator('#seg-diff button[data-value="7"]').click()
        page.wait_for_timeout(200)
        choices = page.locator("#choices .choice")
        expect(choices).to_have_count(7, timeout=3000)
        shot(page, "04-difficulty-7")

        # 6. Switch mode to compare (3 buttons)
        page.locator('#seg-mode button[data-value="compare"]').click()
        page.wait_for_timeout(200)
        choices = page.locator("#choices .choice")
        expect(choices).to_have_count(3, timeout=3000)
        # Verify labels include 같다/올라감/내려감
        labels = choices.all_inner_texts()
        if not any("같다" in l for l in labels):
            bugs.append(f"[P1] compare mode should have '같다' choice, got {labels}")
        if not any("올라" in l for l in labels):
            bugs.append(f"[P1] compare mode should have '올라감' choice, got {labels}")
        shot(page, "05-mode-compare")

        # Answer one compare question
        choices.nth(1).click()
        page.wait_for_timeout(300)
        attempt = page.locator("#s-attempt").inner_text()
        if int(attempt) < 2:
            bugs.append(f"[P0] attempt should increment after compare answer, got {attempt}")

        # 7. Switch mode to chord (difficulty 7 → 4 chord types)
        page.locator('#btn-next').click()
        page.wait_for_timeout(200)
        page.locator('#seg-mode button[data-value="chord"]').click()
        page.wait_for_timeout(200)
        choices = page.locator("#choices .choice")
        ct = choices.count()
        if ct < 2:
            bugs.append(f"[P0] chord mode should have ≥2 choices, got {ct}")
        labels = choices.all_inner_texts()
        if not any("화음" in l or "코드" in l for l in labels):
            bugs.append(f"[P1] chord choices should mention 화음/코드, got {labels}")
        shot(page, "06-mode-chord")

        # 8. Reset clears score
        page.locator("#btn-reset").click()
        page.wait_for_timeout(300)
        attempt = page.locator("#s-attempt").inner_text()
        correct = page.locator("#s-correct").inner_text()
        if attempt != "0" or correct != "0":
            bugs.append(f"[P0] reset should zero counters, got attempt={attempt} correct={correct}")
        shot(page, "07-after-reset")

        # 9. Length segmented control (no question reset needed)
        page.locator('#seg-len button[data-value="1.5"]').click()
        page.wait_for_timeout(150)
        pressed = page.locator('#seg-len button[data-value="1.5"]').get_attribute("aria-pressed")
        if pressed != "true":
            bugs.append(f"[P1] length button should be aria-pressed=true, got {pressed!r}")

        # 10. Hero text present
        h1 = page.locator("h1.display").inner_text()
        if "음정" not in h1:
            bugs.append(f"[P1] h1 should contain '음정', got {h1!r}")

        # 11. Replay button works without error
        page.locator("#btn-reset").click()
        page.wait_for_timeout(200)
        # Answer a question first to enable replay flow
        page.locator('#seg-mode button[data-value="single"]').click()
        page.wait_for_timeout(200)
        page.locator("#choices .choice").nth(0).click()
        page.wait_for_timeout(200)
        page.locator("#btn-replay").click()
        page.wait_for_timeout(400)

        # 12. Mobile viewport
        page.set_viewport_size({"width": 390, "height": 844})
        page.wait_for_timeout(300)
        shot(page, "08-mobile")

        browser.close()

    print()
    print("──────── RESULT ────────")
    print(f"console/page errors (filtered): {len(errors)}")
    for e in errors:
        print(f"  • {e}")
    print(f"bugs: {len(bugs)}")
    for b in bugs:
        print(f"  • {b}")
    summary = {
        "errors": errors,
        "bugs": bugs,
        "url": URL,
    }
    (ROOT / "tests" / "last-run.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2))

    if bugs or errors:
        return 1
    print("OK — 0 bugs, 0 errors")
    return 0


if __name__ == "__main__":
    sys.exit(main())
