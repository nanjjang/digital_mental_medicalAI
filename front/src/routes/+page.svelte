<script>
  const rowOne = [
    "오늘 감정 상태를 기록해 줘",
    "최근 불안이 커졌는데 원인을 정리해 줘",
    "수면 루틴을 다시 만들고 싶어",
    "집중이 흐트러질 때 돌아오는 방법을 알려 줘",
    "감정 일기를 간단히 시작하고 싶어",
    "내일 하루를 차분하게 계획해 줘"
  ];

  const rowTwo = [
    "기분이 가라앉을 때 도움이 되는 말이 필요해",
    "자존감을 회복하는 질문 리스트를 알려 줘",
    "스트레스를 줄이는 저녁 루틴을 짜 줘",
    "긴장 완화를 위한 5분 호흡 루틴",
    "하루 감사 기록을 3줄로 정리해 줘",
    "불안이 올라올 때 대처법을 알려 줘"
  ];

  const rowThree = [
    "자기 돌봄 체크리스트를 만들어 줘",
    "이직 준비로 지친 마음을 정리해 줘",
    "한 주 감정 보고서를 만들어 줘",
    "오늘 나에게 필요한 한 문장을 써 줘",
    "업무 과부하를 줄이는 계획",
    "회복을 위한 주말 루틴을 추천해 줘"
  ];

  const toLink = (text) => `/chat?prompt=${encodeURIComponent(text)}`;
</script>

<section class="section">
  <div class="hero-center">
    <div class="pill">DigitalMentalMedicalAI</div>
    <h1 class="headline">차분하게, 안전하게, 당신의 마음을 기록합니다.</h1>
    <p class="soft-text hero-subtitle">
      서비스 소개부터 온보딩, 리소스, 고객센터까지 한 페이지에서 확인하세요. AI 모듈만 연결하면
      바로 운영 가능한 구조로 설계했습니다.
    </p>
    <div class="hero-actions">
      <a class="btn" href="/signup">시작하기</a>
      <a class="btn text" href="/#features">자세히 알아보기</a>
    </div>
    <div class="hero-links">
      <a href="/#intro">소개</a>
      <a href="/#features">기능</a>
      <a href="/#how">활용법</a>
      <a href="/#support">고객센터</a>
    </div>
  </div>

  <div class="marquee">
    <div class="row">
      <div class="marquee-track">
        {#each [...rowOne, ...rowOne] as item}
          <a class="prompt-card" href={toLink(item)}>{item}</a>
        {/each}
      </div>
    </div>
    <div class="row reverse">
      <div class="marquee-track">
        {#each [...rowTwo, ...rowTwo] as item}
          <a class="prompt-card" href={toLink(item)}>{item}</a>
        {/each}
      </div>
    </div>
    <div class="row">
      <div class="marquee-track">
        {#each [...rowThree, ...rowThree] as item}
          <a class="prompt-card" href={toLink(item)}>{item}</a>
        {/each}
      </div>
    </div>
  </div>
</section>

<section id="intro" class="section">
  <div class="grid two">
    <div>
      <h2 class="section-title">소개</h2>
      <p class="soft-text">
        DigitalMentalMedicalAI는 감정 기록과 안전한 상담을 동시에 제공하는 디지털 멘탈 케어
        플랫폼입니다. 사용자의 페이스에 맞춰 질문과 리소스를 제안하며, AI 모듈을 연결하면
        개인화된 상담으로 확장됩니다.
      </p>
    </div>
    <div class="card">
      <h3 class="section-title">핵심 가치</h3>
      <div class="grid">
        <div class="card">프라이버시 우선 설계</div>
        <div class="card">안정적인 사용자 경험</div>
        <div class="card">치료 여정을 위한 기록</div>
      </div>
    </div>
  </div>
</section>

<section id="features" class="section">
  <div class="grid two">
    <div class="card">
      <h2 class="section-title">기능</h2>
      <p class="soft-text">매일 5분 체크인과 간단한 대화로 마음의 변화 추이를 확인합니다.</p>
      <a class="btn secondary" href="/features">기능 자세히 보기</a>
    </div>
    <div>
      <h3 class="section-title">주요 구성</h3>
      <div class="grid">
        <div class="card">감정 기록과 요약 리포트</div>
        <div class="card">심리 상태 추세 그래프</div>
        <div class="card">맞춤 리소스 추천</div>
      </div>
    </div>
  </div>
</section>

<section id="how" class="section">
  <div class="grid two">
    <div>
      <h2 class="section-title">활용법</h2>
      <p class="soft-text">일상 기록과 진단형 질문으로 스스로의 상태를 이해하고 회복을 시작하세요.</p>
    </div>
    <div class="card">
      <h3 class="section-title">사용 순서</h3>
      <div class="grid">
        <div class="card">계정 생성 및 약관 동의</div>
        <div class="card">초기 상태 체크</div>
        <div class="card">맞춤 리소스 연결</div>
      </div>
    </div>
  </div>
</section>

<section id="support" class="section">
  <div class="grid two">
    <div>
      <h2 class="section-title">고객센터</h2>
      <p class="soft-text">문의, 공지사항, FAQ를 한 곳에서 확인할 수 있습니다.</p>
      <a class="btn secondary" href="/support">고객센터로 이동</a>
    </div>
    <div class="card">
      <h3 class="section-title">지원 항목</h3>
      <div class="grid">
        <div class="card">문의 접수 및 답변</div>
        <div class="card">자주 묻는 질문</div>
        <div class="card">공지사항</div>
      </div>
    </div>
  </div>
</section>

<style>
  .marquee {
    margin-top: 4rem;
    display: grid;
    gap: 1rem;
  }

  .row {
    overflow: hidden;
  }

  .marquee-track {
    display: flex;
    gap: 1rem;
    width: max-content;
    animation: scroll-left 32s linear infinite;
  }

  .row.reverse .marquee-track {
    animation: scroll-right 32s linear infinite;
  }

  .row:hover .marquee-track {
    animation-play-state: paused;
  }

  .prompt-card {
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1rem 1.2rem;
    color: var(--muted);
    background: #f8f8f8;
    min-width: 220px;
  }

  .prompt-card:hover {
    background: #f2f2f2;
    color: var(--ink);
  }

  @keyframes scroll-left {
    0% {
      transform: translateX(0);
    }
    100% {
      transform: translateX(-50%);
    }
  }

  @keyframes scroll-right {
    0% {
      transform: translateX(-50%);
    }
    100% {
      transform: translateX(0);
    }
  }
</style>
