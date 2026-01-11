<script>
  import SeverityBar from "$lib/components/SeverityBar.svelte";

  let score = 32;
</script>

<section class="section">
  <div class="feature-hero">
    <div class="hero-copy">
      <div class="pill">Daily Check-in</div>
      <h1 class="headline">오늘의 감정을 빠르게 기록하세요.</h1>
      <p class="soft-text">
        심각도 게이지와 질문을 통해 현재 상태를 파악합니다. 기록은 요약 리포트로 자동 저장됩니다.
      </p>
    </div>
    <div class="hero-visual">
      <div class="glass-panel">
        <SeverityBar value={score} />
        <div style="margin-top: 1.2rem;">
          <label class="label">오늘의 심각도</label>
          <input type="range" min="0" max="100" bind:value={score} />
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="card">
    <h2 class="section-title">체크인 질문</h2>
    <form class="form">
      <label class="field">
        <span class="label">지금 감정은 어떤가요?</span>
        <input type="text" placeholder="예: 불안, 피로, 안정" />
      </label>
      <label class="field">
        <span class="label">오늘 가장 큰 스트레스 요인은?</span>
        <input type="text" placeholder="업무, 인간관계, 건강 등" />
      </label>
      <label class="field">
        <span class="label">오늘 나를 도와준 것은?</span>
        <textarea rows="3" placeholder="예: 산책, 휴식, 대화"></textarea>
      </label>
      <label class="field">
        <span class="label">한 줄 요약</span>
        <textarea rows="2" placeholder="오늘을 한 문장으로 정리해 주세요."></textarea>
      </label>
      <button class="btn" type="button">기록 저장</button>
    </form>
  </div>
</section>
