# Day 29 — 음정 듣기 퀴즈 (Pitch Ear-Training Quiz)

## 토픽 (from 100-vibecoding-topics.md #029)
- **주제·목표**: 도-미-솔 등 음 듣고 어느 음인지 맞추기. 음감 기초.
- **포함 기능**:
  - 난이도 (3음 / 5음 / 7음)
  - 한 음 모드 / 두 음 비교 모드 / 세 음 코드 모드
  - 점수·정답률 표시
- **배제 기능**: 학생별 점수 서버 저장
- **기술 스택**: HTML/CSS/JS + Tone.js
- **저장 방식**: 휘발성 (세션 내 점수만)
- **AI 사용**: ✕ (Gemini 미사용)
- **대상**: 4~6학년 · **환경**: 1:1
- **DESIGN.md**: ElevenLabs (editorial off-white, gradient orbs)

## 구현 제약
- 단일 `index.html` + vanilla CSS + vanilla JS (단순 토픽).
- Tone.js만 CDN(`unpkg.com/tone`) 의존.
- 빌드 단계 없음 → GitHub Pages root 직접 호스팅.
- Web Audio API는 사용자 첫 제스처 후 init 필요 (autoplay policy).
- WCAG AA: 명도 대비 4.5:1, 키보드 조작, focus state, aria-label.
