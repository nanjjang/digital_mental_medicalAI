<script>
  let name = "";
  let email = "";
  let password = "";
  let passwordConfirm = "";
  let error = "";
  let success = "";
  let loading = false;
  let termsAccepted = false;
  let privacyAccepted = false;
  let crisisAccepted = false;

  async function handleSubmit(event) {
    event.preventDefault();
    error = "";
    success = "";

    if (!termsAccepted || !privacyAccepted || !crisisAccepted) {
      error = "필수 약관에 동의해 주세요.";
      return;
    }

    if (password !== passwordConfirm) {
      error = "비밀번호가 일치하지 않습니다.";
      return;
    }

    loading = true;

    try {
      const response = await fetch("/api/v1/auth/signup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name,
          email,
          password,
          terms_accepted: termsAccepted,
          privacy_accepted: privacyAccepted,
          crisis_accepted: crisisAccepted
        })
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.detail || "회원가입에 실패했습니다.");
      }

      success = "회원가입이 완료되었습니다. 로그인해 주세요.";
      name = "";
      email = "";
      password = "";
      passwordConfirm = "";
      termsAccepted = false;
      privacyAccepted = false;
      crisisAccepted = false;
    } catch (err) {
      error = err.message;
    } finally {
      loading = false;
    }
  }
</script>

<section class="card">
  <h1 class="section-title">회원가입</h1>
  <p class="soft-text">계정을 만들고 서비스를 이용하세요.</p>

  {#if error}
    <div class="error">{error}</div>
  {/if}
  {#if success}
    <div class="notice">{success}</div>
  {/if}

  <form class="form" on:submit={handleSubmit}>
    <label class="field">
      <span class="label">이름</span>
      <input type="text" bind:value={name} required />
    </label>
    <label class="field">
      <span class="label">이메일</span>
      <input type="email" bind:value={email} required />
    </label>
    <label class="field">
      <span class="label">비밀번호</span>
      <input type="password" bind:value={password} required />
    </label>
    <label class="field">
      <span class="label">비밀번호 확인</span>
      <input type="password" bind:value={passwordConfirm} required />
    </label>

    <h2 class="section-title" style="margin-top: 1rem;">약관 동의</h2>
    <label class="check">
      <input type="checkbox" bind:checked={termsAccepted} />
      서비스 이용약관 동의 (필수)
    </label>
    <label class="check">
      <input type="checkbox" bind:checked={privacyAccepted} />
      개인정보 처리방침 동의 (필수)
    </label>
    <label class="check">
      <input type="checkbox" bind:checked={crisisAccepted} />
      위기 상황 대응 안내 동의 (필수)
    </label>

    <button class="btn" type="submit" disabled={loading}>
      {loading ? "가입 중..." : "회원가입"}
    </button>
  </form>
</section>
