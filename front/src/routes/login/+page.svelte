<script>
  let email = "";
  let password = "";
  let error = "";
  let success = "";
  let loading = false;

  async function handleSubmit(event) {
    event.preventDefault();
    error = "";
    success = "";
    loading = true;

    try {
      const response = await fetch("/api/v1/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.detail || "로그인에 실패했습니다.");
      }

      if (typeof localStorage !== "undefined") {
        localStorage.setItem("auth_token", data.token);
        localStorage.setItem("user_id", String(data.user.id));
      }
      success = "로그인에 성공했습니다.";
    } catch (err) {
      error = err.message;
    } finally {
      loading = false;
    }
  }
</script>

<section class="card">
  <h1 class="section-title">로그인</h1>
  <p class="soft-text">계정 정보를 입력하고 서비스를 시작하세요.</p>

  {#if error}
    <div class="error">{error}</div>
  {/if}
  {#if success}
    <div class="notice">{success}</div>
  {/if}

  <form class="form" on:submit={handleSubmit}>
    <label class="field">
      <span class="label">이메일</span>
      <input type="email" bind:value={email} required />
    </label>
    <label class="field">
      <span class="label">비밀번호</span>
      <input type="password" bind:value={password} required />
    </label>
    <button class="btn" type="submit" disabled={loading}>
      {loading ? "로그인 중..." : "로그인"}
    </button>
  </form>
</section>
