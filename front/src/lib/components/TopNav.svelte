<nav class="nav">
  <a class="brand" href="/">
    <img class="logo" src="/Gemini_Generated_Image_n90k8wn90k8wn90k-removebg-preview.png" alt="DigitalMentalMedicalAI logo" />
    <strong>DigitalMentalMedicalAI</strong>
  </a>
  <div class="links">
    <a href="/">소개</a>
    <a href="/features">기능</a>
    <a href="/how">활용법</a>
    <a href="/business">비즈니스</a>
    <a href="/pricing">가격</a>
    <a href="/download">다운로드</a>
  </div>
  <div class="actions">
    <a class="btn secondary" href="/login">로그인</a>
    <a class="btn" href="/signup">회원 가입</a>
  </div>
</nav>

<style>
  .nav {
    position: sticky;
    top: 0;
    z-index: 10;
    display: grid;
    grid-template-columns: auto 1fr auto;
    align-items: center;
    gap: 1.5rem;
    padding: 1.2rem 1.5rem;
    width:1500px;
    max-height: 80px;
    /* max-width: var(--max-width); */
    margin: 0 auto;
    background: rgba(255, 255, 255, 0.92);
    backdrop-filter: blur(12px);
    border-bottom: 1px solid var(--border);
  }

  .brand {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    font-weight: 700;
  }

  .logo {
    width: 28px;
    height: 28px;
    object-fit: contain;
  }

  .links {
    display: flex;
    gap: 1rem;
    justify-content: center;
    color: var(--muted);
    font-size: 0.95rem;
  }

  .links a:hover {
    color: var(--ink);
  }

  .actions {
    display: flex;
    gap: 0.6rem;
  }

  @media (max-width: 960px) {
    .nav {
      grid-template-columns: 1fr;
      align-items: flex-start;
    }

    .links {
      flex-wrap: wrap;
      justify-content: flex-start;
    }
  }
</style>
