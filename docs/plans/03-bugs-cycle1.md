# Bugs — Cycle 1

## Found
1. **[env-blocker] Tone.js CDN cert error in headless Chromium**
   - Repro: `playwright chromium` → goto page → console error `ERR_CERT_AUTHORITY_INVALID` from `unpkg.com/tone`.
   - Cause: harness-installed chromium-headless-shell doesn't trust Cloudflare cert chain.
   - Action: environment noise per spec; filtered in test (no fix in source).

2. **[P0] First question never rendered after start click**
   - Repro: click "시작하기" → overlay shows "재시도" / no choices.
   - Cause: `ensureAudio()` threw (Tone.js failed to load due to #1), error path replaced button text and skipped `nextQuestion()`.
   - Fix: in `index.html` — always dismiss overlay and render question; downgrade audio failure to a warning. Big ▶ button retries audio later.

3. **[P1] Panel segmented buttons wrap awkwardly (label characters stacked vertically)**
   - Repro: 1280px viewport → "두 음 비교" / "세 음 코드" wrap one character per line.
   - Cause: 4-column grid with 1fr 1fr 1fr auto split gave each segment too narrow a track.
   - Fix: panel → flex-wrap with `gap: 28px 32px`, `seg button { white-space: nowrap }`, segments size to their natural content.

## Outcome
P0/P1: **0 remaining**. e2e: **0 fail, 0 errors** (filtered). 1 cycle, terminated cleanly.
