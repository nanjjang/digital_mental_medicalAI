<script>
  import { onMount } from "svelte";
  import { browser } from "$app/environment";
  import { goto } from "$app/navigation";
  import { auth, initFromStorage, setAuth } from "$lib/stores/auth";
  let username = "";
  let name = "";
  let email = "";
  let password = "";
  let passwordConfirm = "";
  let error = "";
  let success = "";
  let loading = false;
  let termsAccepted = false;
  let privacyAccepted = false;
  let safetyAccepted = false;

  onMount(() => {
    initFromStorage();
  });

  $: if (browser && $auth?.isLoggedIn) {
    goto("/chat");
  }
  async function handleSubmit(event) {
    event.preventDefault();
    error = "";
    success = "";

    if (!username) {
      error = "아이디를 입력해 주세요.";
      return;
    }

    if (username.length < 3) {
      error = "아이디는 최소 3자 이상이어야 합니다.";
      return;
    }

    if (!termsAccepted || !privacyAccepted || !safetyAccepted) {
      error = "필수 약관에 동의해 주세요.";
      return;
    }

    if (password !== passwordConfirm) {
      error = "비밀번호가 일치하지 않습니다.";
      return;
    }

    if (password.length < 8) {
      error = "비밀번호는 최소 8자 이상이어야 합니다.";
      return;
    }

    loading = true;

    try {
      const response = await fetch("http://127.0.0.1:8000/api/v1/auth/signup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          username,
          display_name: name,
          email,
          password,
          terms_accepted: termsAccepted,
          privacy_accepted: privacyAccepted,
          safety_accepted: safetyAccepted
        })
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.detail || "회원가입에 실패했습니다.");
      }

      // 로컬스토리지에 토큰 저장
      if (typeof localStorage !== "undefined") {
        localStorage.setItem("auth_token", data.token);
        localStorage.setItem("user_id", String(data.user.id));
        localStorage.setItem("user_email", data.user.email);
        localStorage.setItem("user_username", data.user.username);
      }

      setAuth({
        username: data.user.username,
        email: data.user.email
      });

      success = "회원가입이 완료되었습니다!";
      
      // 2초 후 대시보드로 이동
      setTimeout(() => {
        goto("/");
      }, 1500);
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
      <span class="label">아이디</span>
      <input type="text" bind:value={username} placeholder="3자 이상" required />
    </label>
    <label class="field">
      <span class="label">표시 이름</span>
      <input type="text" bind:value={name} placeholder="선택사항" />
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
      <input type="checkbox" bind:checked={safetyAccepted} />
      안전 및 위기 상황 안내 동의 (필수)
    </label>

    <button class="btn" type="submit" disabled={loading}>
      {loading ? "가입 중..." : "회원가입"}
    </button>
  </form>
  <div class="form-footer">
    <span class="soft-text">이미 계정이 있나요?</span>
    <a class="btn text" href="/login">로그인</a>
  </div>
</section>


<style>
  .form-footer {
    margin-top: 1rem;
    display: flex;
    gap: 0.5rem;
    align-items: center;
    justify-content: center;
  }
</style>