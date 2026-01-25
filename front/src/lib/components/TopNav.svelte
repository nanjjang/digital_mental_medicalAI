<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { browser } from '$app/environment';
  import { auth, initFromStorage, clearAuth } from '$lib/stores/auth';

  let showProfileMenu = false;
  let hydrated = false;

  onMount(() => {
    hydrated = true;
    initFromStorage();
  });

  function handleLogout() {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('user_id');
    localStorage.removeItem('user_email');
    localStorage.removeItem('user_username');
    clearAuth();
    showProfileMenu = false;
    goto('/');
  }

  function toggleProfileMenu() {
    showProfileMenu = !showProfileMenu;
  }
</script>

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
    {#if browser && hydrated}
      {#if $auth.isLoggedIn}
        <div class="profile-menu">
          <button class="profile-btn" on:click={toggleProfileMenu}>
            <span class="avatar">👤</span>
            <span class="username">{$auth.username}</span>
          </button>
          {#if showProfileMenu}
            <div class="dropdown">
              <div class="dropdown-header">{$auth.username}</div>
              <div class="dropdown-email">{$auth.email}</div>
              <hr />
              <a href="/settings" on:click={() => (showProfileMenu = false)}>설정</a>
              <a href="/history" on:click={() => (showProfileMenu = false)}>기록</a>
              <hr />
              <button class="logout-btn" on:click={handleLogout}>로그아웃</button>
            </div>
          {/if}
        </div>
      {:else}
        <a class="btn secondary" href="/login">로그인</a>
        <a class="btn" href="/signup">회원 가입</a>
      {/if}
    {/if}
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
    width: 100%;
    max-width: var(--max-width);
    max-height: 80px;
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
    flex-wrap: wrap;
  }

  .links a:hover {
    color: var(--ink);
  }

  .actions {
    display: flex;
    gap: 0.6rem;
    align-items: center;
  }

  .profile-menu {
    position: relative;
  }

  .profile-btn {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    background: var(--bg-secondary);
    border: 1px solid var(--border);
    border-radius: 8px;
    cursor: pointer;
    font-size: 0.95rem;
    transition: all 0.2s ease;
  }

  .profile-btn:hover {
    background: var(--bg-tertiary);
    border-color: var(--primary);
  }

  .avatar {
    font-size: 1.2rem;
  }

  .email {
    max-width: 150px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .username {
    max-width: 120px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    font-weight: 600;
  }

  .dropdown-header {
    padding: 0.75rem 1rem;
    font-weight: 600;
    color: var(--ink);
    border-bottom: 1px solid var(--border);
  }

  .dropdown-email {
    padding: 0.5rem 1rem;
    font-size: 0.85rem;
    color: var(--muted);
  }

  .dropdown {
    position: absolute;
    top: 100%;
    right: 0;
    margin-top: 0.5rem;
    background: white;
    border: 1px solid var(--border);
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    min-width: 180px;
    z-index: 20;
  }

  .dropdown a,
  .logout-btn {
    display: block;
    width: 100%;
    padding: 0.75rem 1rem;
    text-align: left;
    color: var(--ink);
    text-decoration: none;
    border: none;
    background: none;
    cursor: pointer;
    font-size: 0.95rem;
    transition: background-color 0.2s ease;
  }

  .dropdown a:hover,
  .logout-btn:hover {
    background-color: var(--bg-secondary);
  }

  .dropdown hr {
    margin: 0.5rem 0;
    border: none;
    border-top: 1px solid var(--border);
  }

  .logout-btn {
    color: #d32f2f;
    font-weight: 500;
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
