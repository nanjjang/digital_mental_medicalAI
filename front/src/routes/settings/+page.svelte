<script>
  import { onMount } from "svelte";
  import { browser } from "$app/environment";
  import { initFromStorage } from "$lib/stores/auth";

  let userId = null;
  let loading = true;
  let saving = false;
  let error = "";
  let success = "";

  const toneOptions = [
    { value: "gentle", label: "부드러운 톤" },
    { value: "neutral", label: "중립적 톤" },
    { value: "direct", label: "직관적 톤" },
    { value: "coach", label: "코치형 톤" }
  ];

  const languageOptions = [
    { value: "ko-KR", label: "한국어" },
    { value: "en-US", label: "English" }
  ];

  const timezoneOptions = [
    "Asia/Seoul",
    "Asia/Tokyo",
    "America/Los_Angeles",
    "America/New_York",
    "Europe/London"
  ];

  let profile = {
    username: "",
    display_name: "",
    email: "",
    phone: "",
    location: "",
    avatar_url: "",
    bio: ""
  };

  let settings = {
    tone: "gentle",
    notifications_enabled: true,
    daily_checkin_enabled: true,
    weekly_report_enabled: true,
    summary_autosave: false,
    language: "ko-KR",
    timezone: "Asia/Seoul",
    data_retention_days: 365,
    marketing_opt_in: false,
    crisis_alerts_enabled: true,
    privacy_mode: false,
    guardian_contact: ""
  };

  const loadProfile = async () => {
    const response = await fetch(`/api/v1/users/${userId}`);
    if (!response.ok) {
      throw new Error("프로필 정보를 불러오지 못했습니다.");
    }
    const data = await response.json();
    profile = {
      username: data.username || "",
      display_name: data.display_name || "",
      email: data.email || "",
      phone: data.phone || "",
      location: data.location || "",
      avatar_url: data.avatar_url || "",
      bio: data.bio || ""
    };
  };

  const loadSettings = async () => {
    const response = await fetch(`/api/v1/settings/${userId}`);
    if (!response.ok) {
      return;
    }
    const data = await response.json();
    if (!data) return;
    settings = {
      tone: data.tone ?? settings.tone,
      notifications_enabled: data.notifications_enabled ?? settings.notifications_enabled,
      daily_checkin_enabled: data.daily_checkin_enabled ?? settings.daily_checkin_enabled,
      weekly_report_enabled: data.weekly_report_enabled ?? settings.weekly_report_enabled,
      summary_autosave: data.summary_autosave ?? settings.summary_autosave,
      language: data.language ?? settings.language,
      timezone: data.timezone ?? settings.timezone,
      data_retention_days: data.data_retention_days ?? settings.data_retention_days,
      marketing_opt_in: data.marketing_opt_in ?? settings.marketing_opt_in,
      crisis_alerts_enabled: data.crisis_alerts_enabled ?? settings.crisis_alerts_enabled,
      privacy_mode: data.privacy_mode ?? settings.privacy_mode,
      guardian_contact: data.guardian_contact ?? settings.guardian_contact
    };
  };

  const saveAll = async () => {
    if (!userId) {
      error = "로그인 후 저장할 수 있습니다.";
      return;
    }
    error = "";
    success = "";
    saving = true;
    try {
      const profileResponse = await fetch(`/api/v1/users/${userId}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          display_name: profile.display_name,
          email: profile.email || null,
          phone: profile.phone || null,
          location: profile.location || null,
          avatar_url: profile.avatar_url || null,
          bio: profile.bio || null
        })
      });

      if (!profileResponse.ok) {
        const detail = await profileResponse.json().catch(() => ({}));
        throw new Error(detail.detail || "프로필 저장에 실패했습니다.");
      }

      const settingsResponse = await fetch("/api/v1/settings", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_id: Number(userId),
          tone: settings.tone,
          notifications_enabled: settings.notifications_enabled,
          daily_checkin_enabled: settings.daily_checkin_enabled,
          weekly_report_enabled: settings.weekly_report_enabled,
          summary_autosave: settings.summary_autosave,
          language: settings.language,
          timezone: settings.timezone,
          data_retention_days: Number(settings.data_retention_days) || 365,
          marketing_opt_in: settings.marketing_opt_in,
          crisis_alerts_enabled: settings.crisis_alerts_enabled,
          privacy_mode: settings.privacy_mode,
          guardian_contact: settings.guardian_contact || null
        })
      });

      if (!settingsResponse.ok) {
        const detail = await settingsResponse.json().catch(() => ({}));
        throw new Error(detail.detail || "설정 저장에 실패했습니다.");
      }

      success = "프로필과 설정이 저장되었습니다.";
    } catch (err) {
      error = err.message;
    } finally {
      saving = false;
    }
  };

  onMount(() => {
    initFromStorage();
    if (!browser) return;
    userId = localStorage.getItem("user_id");
    if (!userId) {
      loading = false;
      return;
    }
    Promise.all([loadProfile(), loadSettings()])
      .catch((err) => {
        error = err.message;
      })
      .finally(() => {
        loading = false;
      });
  });
</script>

<section class="section">
  <div class="card">
    <h1 class="section-title">설정</h1>
    <p class="soft-text">프로필과 개인화 옵션을 관리하세요.</p>

    {#if !userId}
      <div class="notice">
        로그인 후 프로필과 설정을 저장할 수 있습니다. <a class="btn text" href="/login">로그인하기</a>
      </div>
    {/if}

    {#if loading}
      <p class="soft-text">설정 정보를 불러오는 중입니다...</p>
    {/if}

    {#if error}
      <div class="error">{error}</div>
    {/if}
    {#if success}
      <div class="notice">{success}</div>
    {/if}

    <form class="form" on:submit|preventDefault={saveAll}>
      <div class="settings-grid">
        <div class="card settings-card">
          <h2 class="section-title">프로필</h2>
          <label class="field">
            <span class="label">아이디</span>
            <input type="text" bind:value={profile.username} readonly />
          </label>
          <label class="field">
            <span class="label">표시 이름</span>
            <input type="text" bind:value={profile.display_name} placeholder="표시 이름" />
          </label>
          <label class="field">
            <span class="label">이메일</span>
            <input type="email" bind:value={profile.email} placeholder="name@example.com" />
          </label>
          <label class="field">
            <span class="label">연락처</span>
            <input type="text" bind:value={profile.phone} placeholder="010-1234-5678" />
          </label>
          <label class="field">
            <span class="label">지역</span>
            <input type="text" bind:value={profile.location} placeholder="Seoul, Korea" />
          </label>
          <label class="field">
            <span class="label">프로필 이미지 URL</span>
            <input type="url" bind:value={profile.avatar_url} placeholder="https://..." />
          </label>
          <label class="field">
            <span class="label">소개</span>
            <textarea rows="3" bind:value={profile.bio} placeholder="자기소개를 입력하세요."></textarea>
          </label>
        </div>

        <div class="card settings-card">
          <h2 class="section-title">알림</h2>
          <label class="check">
            <input type="checkbox" bind:checked={settings.notifications_enabled} />
            전체 알림 받기
          </label>
          <label class="check">
            <input type="checkbox" bind:checked={settings.daily_checkin_enabled} />
            매일 체크인 알림
          </label>
          <label class="check">
            <input type="checkbox" bind:checked={settings.weekly_report_enabled} />
            주간 리포트 알림
          </label>
          <label class="check">
            <input type="checkbox" bind:checked={settings.summary_autosave} />
            상담 요약 자동 저장
          </label>
        </div>

        <div class="card settings-card">
          <h2 class="section-title">개인화</h2>
          <label class="field">
            <span class="label">응답 톤</span>
            <select bind:value={settings.tone}>
              {#each toneOptions as option}
                <option value={option.value}>{option.label}</option>
              {/each}
            </select>
          </label>
          <label class="field">
            <span class="label">기본 언어</span>
            <select bind:value={settings.language}>
              {#each languageOptions as option}
                <option value={option.value}>{option.label}</option>
              {/each}
            </select>
          </label>
          <label class="field">
            <span class="label">시간대</span>
            <select bind:value={settings.timezone}>
              {#each timezoneOptions as tz}
                <option value={tz}>{tz}</option>
              {/each}
            </select>
          </label>
          <label class="field">
            <span class="label">데이터 보관 기간(일)</span>
            <input type="number" min="7" max="3650" bind:value={settings.data_retention_days} />
          </label>
          <label class="check">
            <input type="checkbox" bind:checked={settings.marketing_opt_in} />
            신규 기능/이벤트 알림 수신
          </label>
        </div>

        <div class="card settings-card">
          <h2 class="section-title">보안 · 안전</h2>
          <label class="check">
            <input type="checkbox" bind:checked={settings.privacy_mode} />
            프라이버시 모드 (민감 데이터 최소 저장)
          </label>
          <label class="check">
            <input type="checkbox" bind:checked={settings.crisis_alerts_enabled} />
            위기 상황 알림 활성화
          </label>
          <label class="field">
            <span class="label">보호자 연락처</span>
            <input type="text" bind:value={settings.guardian_contact} placeholder="guardian@email.com" />
          </label>
        </div>
      </div>

      <div class="form-actions">
        <button class="btn" type="submit" disabled={saving || !userId}>
          {saving ? "저장 중..." : "설정 저장"}
        </button>
      </div>
    </form>
  </div>
</section>

<style>
  .settings-grid {
    display: grid;
    gap: 1.6rem;
    margin-top: 1.5rem;
  }

  .settings-card {
    box-shadow: none;
  }

  .settings-card .field {
    width: 100%;
  }

  .form-actions {
    margin-top: 1.5rem;
    display: flex;
    justify-content: flex-end;
  }

  select {
    width: 100%;
    padding: 0.7rem 0.9rem;
    border-radius: 12px;
    border: 1px solid var(--border);
    font: inherit;
    background: #ffffff;
  }

  textarea {
    resize: vertical;
  }

  @media (min-width: 980px) {
    .settings-grid {
      grid-template-columns: repeat(2, 1fr);
    }
  }
</style>
