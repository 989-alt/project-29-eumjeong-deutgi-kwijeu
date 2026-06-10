# UI/UX — Day 29 음정 듣기 퀴즈 (ElevenLabs 브랜드)

## 브랜드 적용 요지
- 캔버스 `#f5f5f5` 위 따뜻한 잉크 `#0c0a09`, 흰 카드 `#ffffff` + 1px 헤어라인 `#e7e5e4`.
- 디스플레이는 serif 300weight (Waldenburg 대체 → `Georgia, 'Times New Roman', serif`, 또는 `EB Garamond` Google Font).
- 본문은 Inter 400/500 (Google Font), letter-spacing +0.16px.
- CTA = 잉크 알약 (background `#292524`, on-primary `#fff`, `border-radius: 9999px`).
- 보조 CTA = transparent outline pill.
- **시그니처**: 부드러운 파스텔 그라디언트 오브 (mint #a7e5d3, peach #f4c5a8, lavender #c8b8e0, sky #a8c8e8, rose #e8b8c4) — 배경 atmosphere로만, 절대 버튼 채움색·텍스트 색·컴포넌트 배경 X.
- 96px section padding, 24px 카드 padding, `rounded.xl` 16px 카드, `rounded.xxl` 24px atmospheric 카드.

## 화면 구조 (single-page, 단일 뷰)
1. **Hero band** (canvas, padding 64px/24px): 작은 caption-uppercase "EAR TRAINING · 음감 훈련" + 큰 serif h1 "음정 듣기 퀴즈" (display-xl 48px / 모바일 32px) + 한 줄 sub-copy (Inter 16px body) + 배경에 lavender→mint 그라디언트 오브 atmospheric (절대 텍스트와 겹치게 진하지 않음).
2. **Control panel card** (surface-card, rounded.xl, hairline border): 가로 3섹션 — `난이도 (3 / 5 / 7)`, `모드 (한 음 / 두 음 / 코드)`, `음 길이 (짧음 / 보통 / 김)` 모두 caption-uppercase 라벨 + pill segmented buttons. 우측에 "초기화" tertiary text.
3. **Quiz card** (surface-card, rounded.xl, 32px padding): 가운데 큰 동그란 play 버튼 (잉크 background, 흰 ▶, 96px), 그 아래 caption "문제 N" / Inter title-md "이 음정은 어떤 음일까요?" / 보기 그리드 (모드별 동적). 정답 공개 후: 큰 결과 텍스트 (display-md, 정답이면 success-green tinted, 오답이면 error 톤은 ink + 작은 빨간 dot으로 절제) + 정답 라벨 + 가로 2버튼 ("다시 듣기" outline, "다음 문제" primary pill).
4. **Score row**: 캡션 라벨 3개 — 시도 / 정답 / 정답률 — display-sm 숫자.
5. **Mini keyboard** (audio-waveform-card 유사 surface-card, 24px padding): SVG 1옥타브 (도~도). 정답 공개 시 해당 음 키가 mint 그라디언트로 일시 강조.
6. **Footer**: 작은 Inter body-sm 한 줄 — "Day 29 · 1일 1바이브코딩 · ElevenLabs design".

## 주요 컴포넌트
- **Segmented pill group**: 3개의 pill 버튼이 한 row. 선택 = ink 채움 + 흰 텍스트. 비선택 = transparent + 1px hairline-strong border + ink 텍스트. 키보드 좌/우/탭 이동.
- **Big play button (96px)**: ink fill, ▶ 흰 글리프, 호버시 살짝 scale, focus 시 2px ink ring outside.
- **Choice button (note)**: outline pill, 60px 너비, 음명("도", "레"...). 정답 공개시 정답 버튼은 mint orb halo, 오답 선택은 rose orb halo. 답 제출 후 비활성화.
- **Comparison button (두 음 모드)**: 3개 outline pill — "같다" / "올라감 ↑" / "내려감 ↓".
- **Chord choice (세 음 모드)**: 4개 outline pill — "장3화음 (도미솔)" / "단3화음 (도♭미솔)" / "장7화음 (도미솔시)" / "감3화음 (도♭미♭솔)". (난이도에 따라 가짓수 조정)
- **Mini keyboard**: 7 흰 건반 + 5 검은 건반 SVG. ARIA hidden (장식적). 정답 음만 강조.

## 접근성
- 모든 버튼 키보드 조작 가능, focus ring 2px ink outside.
- 색만으로 정/오 구분하지 않음 — 텍스트 "정답!" / "오답" 표시 + 큰 글리프 (✓/✕는 안 쓰고 단순 라벨).
- 명도 대비: 본문 `#4e4e4e` on `#f5f5f5` = 7.4:1 통과. ink on canvas = 14:1.
- 그라디언트 orb는 매우 흐림 → 배경 텍스트 대비 영향 최소.
- 오디오 unlock 안내 명시 ("처음 한 번 ▶ 시작 버튼을 눌러주세요").
- aria-live="polite" 영역에 점수·정답 결과 announce.
- prefers-reduced-motion 시 orb drift 애니메이션 정지.

## design.md vs ui-ux-pro-max 충돌 시
- design.md 우선 — Waldenburg/Inter, 잉크 pill, 그라디언트 orb, 96px section 모두 design.md가 권위.
