<script>
  import { onMount, tick } from "svelte";

  let prompt = "";
  const chips = ["오늘 감정 기록", "5분 호흡 루틴", "수면 루틴 제안", "하루 정리 질문", "불안 완화 체크인", "집중 회복 플랜"];
  let messages = [];
  let sessions = [];
  let inputRef;
  let threadRef;
  let sessionId = null;
  let isSending = false;
  let loadingSession = false;
  let loadingSessions = false;
  let loadingMessages = false;
  let error = "";
  let loggedIn = false;
  let userId = null;

  const labelMap = {
    normal: "정상",
    depression: "우울",
    suicide: "자살 위험",
    anxiety: "불안",
  };

  const nowTime = () =>
    new Date().toLocaleTimeString("ko-KR", { hour: "2-digit", minute: "2-digit" });

  const formatLabel = (label) => labelMap[label] ?? label;

  const formatClock = (value) => {
    if (!value) return "";
    const d = new Date(value);
    return isNaN(d) ? "" : d.toLocaleTimeString("ko-KR", { hour: "2-digit", minute: "2-digit" });
  };

  const formatDate = (value) => {
    if (!value) return "";
    const d = new Date(value);
    return isNaN(d) ? "" : d.toLocaleString("ko-KR", { month: "short", day: "numeric", hour: "2-digit", minute: "2-digit" });
  };

  const topScores = (scores) =>
    scores ? Object.entries(scores).sort((a, b) => b[1] - a[1]).slice(0, 3) : [];

  const scrollToBottom = async () => {
    await tick();
    if (threadRef) threadRef.scrollTop = threadRef.scrollHeight;
  };

  const addMessage = (role, text, meta = null, timeOverride = null) => {
    const trimmed = text.trim();
    if (!trimmed) return;
    messages = [...messages, { id: crypto.randomUUID(), role, text: trimmed, time: timeOverride ?? nowTime(), meta }];
    scrollToBottom();
  };

  const fetchJson = async (input, init) => {
    const res = await fetch(input, init);
    const ct = res.headers.get("content-type") ?? "";
    const data = ct.includes("application/json") ? await res.json() : await res.text();
    if (!res.ok) throw new Error(typeof data === "string" ? data : (data.detail ?? "요청에 실패했습니다."));
    return data;
  };

  const loadMessages = async (targetSessionId) => {
    loadingMessages = true;
    error = "";
    try {
      const history = await fetchJson(`/api/v1/messages?session_id=${targetSessionId}`);
      messages = history.map((item) => ({
        id: item.id,
        role: item.role === "assistant" ? "assistant" : "user",
        text: item.content,
        time: formatClock(item.created_at),
        meta: item.meta ?? null,
      }));
      scrollToBottom();
    } catch (err) {
      error = err.message || "메시지를 불러오지 못했습니다.";
    } finally {
      loadingMessages = false;
    }
  };

  const refreshSessions = async () => {
    if (!userId) return;
    loadingSessions = true;
    error = "";
    try {
      sessions = await fetchJson(`/api/v1/sessions?user_id=${userId}`);
    } catch (err) {
      error = err.message || "세션을 불러오지 못했습니다.";
    } finally {
      loadingSessions = false;
    }
  };

  const createSession = async () => {
    loadingSession = true;
    error = "";
    try {
      const session = await fetchJson("/api/v1/sessions", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: userId, severity_score: 0 }),
      });
      sessionId = session.id;
      messages = [];
      if (loggedIn) await refreshSessions();
      return session;
    } catch (err) {
      error = err.message || "세션을 준비하지 못했습니다.";
      return null;
    } finally {
      loadingSession = false;
    }
  };

  const activateSession = async (targetSessionId) => {
    sessionId = targetSessionId;
    await loadMessages(targetSessionId);
  };

  const handleSend = async () => {
    const trimmed = prompt.trim();
    if (!trimmed || isSending) return;

    addMessage("user", trimmed);
    prompt = "";
    error = "";

    if (!sessionId) {
      error = "세션이 준비되지 않았어요. 잠시 후 다시 시도해 주세요.";
      return;
    }

    isSending = true;
    try {
      const data = await fetchJson("/api/v1/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: trimmed, session_id: sessionId }),
      });
      addMessage("assistant", data.reply, {
        label: data.label,
        scores: data.scores,
        confidence: data.confidence,
      });
    } catch (err) {
      error = err.message || "메시지 전송에 실패했습니다.";
    } finally {
      isSending = false;
    }
  };

  const handleKeydown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleChip = (chip) => {
    prompt = chip;
    inputRef?.focus();
  };

  const handleQuick = (text) => {
    prompt = text;
    inputRef?.focus();
  };

  onMount(async () => {
    const value = new URLSearchParams(window.location.search).get("prompt");
    if (value) prompt = value;

    if (typeof localStorage !== "undefined") {
      const storedUserId = localStorage.getItem("user_id");
      if (storedUserId) {
        loggedIn = true;
        userId = Number(storedUserId);
      }
    }

    if (loggedIn) {
      await refreshSessions();
      if (sessions.length > 0) {
        await activateSession(sessions[0].id);
        return;
      }
    }

    const session = await createSession();
    if (session) await loadMessages(session.id);
  });
</script>

<section class="chat">
  <div class="header">
    <p class="eyebrow">AI 대화 공간</p>
    <h1 class="title">지금 떠오르는 생각을 편하게 말해 보세요.</h1>
    <p class="subtitle">
      정신 건강 AI가 당신의 말 속 감정을 분석하고, 상황에 맞는 응답을 제공합니다.
    </p>
    {#if error}
      <p class="notice error">{error}</p>
    {/if}
    {#if loadingSession}
      <p class="notice">대화 세션을 준비 중입니다...</p>
    {/if}
    {#if !loggedIn}
      <p class="notice">게스트 모드로 채팅을 시작합니다.</p>
    {/if}
  </div>

  <div class="workspace">
    {#if loggedIn}
      <aside class="sessions">
        <div class="session-header">
          <h2>최근 세션</h2>
          <button class="ghost" type="button" on:click={createSession} disabled={loadingSession}>새 세션</button>
        </div>
        {#if loadingSessions}
          <p class="muted">불러오는 중...</p>
        {:else if sessions.length === 0}
          <p class="muted">저장된 세션이 없어요.</p>
        {/if}
        <div class="session-list">
          {#each sessions as session (session.id)}
            <button
              class="session-item {session.id === sessionId ? 'active' : ''}"
              type="button"
              on:click={() => activateSession(session.id)}
            >
              <div class="session-title">세션 #{session.id}</div>
              <div class="session-meta">
                <span>{formatDate(session.started_at)}</span>
                <span class="dot">•</span>
                <span>{session.status}</span>
              </div>
            </button>
          {/each}
        </div>
      </aside>
    {:else}
      <aside class="sessions guest">
        <div class="session-header">
          <h2>게스트 모드</h2>
          <button class="ghost" type="button" on:click={createSession} disabled={loadingSession}>새 세션</button>
        </div>
        <p class="muted">로그인 없이 대화를 시작합니다. 기록은 이 브라우저에만 유지됩니다.</p>
      </aside>
    {/if}

    <div class="conversation">
      <div class="session-banner">
        <div>
          <strong>현재 세션</strong>
          <span>{sessionId ? `#${sessionId}` : "-"}</span>
        </div>
        {#if loggedIn}
          <button class="ghost" type="button" on:click={refreshSessions} disabled={loadingSessions}>새로고침</button>
        {/if}
      </div>

      <div class="thread" bind:this={threadRef}>
        {#if loadingMessages}
          <div class="empty">메시지를 불러오는 중입니다...</div>
        {:else if messages.length === 0}
          <div class="empty">아직 대화가 없습니다. 아래에서 시작해 보세요.</div>
        {/if}
        {#each messages as message (message.id)}
          <div class="bubble {message.role}">
            <p style="white-space: pre-wrap">{message.text}</p>
            {#if message.role === "assistant" && message.meta}
              <div class="meta">
                <div class="meta-row">
                  <span class="badge">{formatLabel(message.meta.label)}</span>
                  {#if message.meta.confidence != null}
                    <span class="confidence">확신 {Math.round(message.meta.confidence * 100)}%</span>
                  {/if}
                </div>
                {#if message.meta.scores}
                  <div class="score-row">
                    {#each topScores(message.meta.scores) as [lbl, score]}
                      <span>{formatLabel(lbl)} {Math.round(score * 100)}%</span>
                    {/each}
                  </div>
                {/if}
              </div>
            {/if}
            {#if message.time}
              <span class="time">{message.time}</span>
            {/if}
          </div>
        {/each}
        {#if isSending}
          <div class="bubble assistant typing">
            <span class="dot-anim"></span>
            <span class="dot-anim"></span>
            <span class="dot-anim"></span>
          </div>
        {/if}
      </div>

      <div class="composer">
        <textarea
          rows="4"
          bind:this={inputRef}
          bind:value={prompt}
          disabled={!sessionId || isSending}
          placeholder="오늘 마음을 한 문장으로 적어 보세요. 예: 오늘은 불안이 커서 잠이 오지 않았어요."
          on:keydown={handleKeydown}
        ></textarea>
        <div class="composer-actions">
          <div class="chip-row">
            {#each chips as chip}
              <button class="chip" type="button" on:click={() => handleChip(chip)} disabled={isSending}>
                {chip}
              </button>
            {/each}
          </div>
          <button class="send" type="button" aria-label="전송" on:click={handleSend} disabled={!sessionId || isSending}>
            {#if isSending}
              <span class="spinner"></span>
            {:else}
              ↑
            {/if}
          </button>
        </div>
      </div>
    </div>
  </div>

  <div class="cards">
    <button class="card" type="button" on:click={() => handleQuick("오늘 감정 기록을 시작하고 싶어요.")}>오늘 감정 기록 시작하기</button>
    <button class="card" type="button" on:click={() => handleQuick("5분 호흡 루틴을 안내해 주세요.")}>5분 호흡 루틴 요청</button>
    <button class="card" type="button" on:click={() => handleQuick("수면 루틴을 점검해 주세요.")}>수면 루틴 점검</button>
    <button class="card" type="button" on:click={() => handleQuick("불안 상황을 정리하는 질문을 해 주세요.")}>불안 상황 정리하기</button>
  </div>
</section>

<style>
  .chat {
    display: grid;
    gap: 2rem;
  }

  .header {
    text-align: center;
    display: grid;
    gap: 0.6rem;
  }

  .eyebrow {
    text-transform: uppercase;
    letter-spacing: 0.12em;
    font-size: 0.75rem;
    color: var(--muted);
  }

  .title {
    margin: 0;
    font-size: clamp(1.8rem, 3vw, 2.6rem);
  }

  .subtitle {
    max-width: 640px;
    margin: 0 auto;
    color: var(--muted);
    line-height: 1.7;
  }

  .notice {
    font-size: 0.85rem;
    color: var(--muted);
    margin: 0;
  }

  .notice.error {
    color: #dc2626;
  }

  .workspace {
    display: grid;
    gap: 1.5rem;
    grid-template-columns: minmax(220px, 280px) minmax(0, 1fr);
    align-items: start;
  }

  .sessions {
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 1.2rem;
    background: #ffffff;
    display: grid;
    gap: 1rem;
    box-shadow: 0 18px 40px rgba(15, 23, 42, 0.08);
  }

  .sessions.guest {
    background: #f8fafc;
  }

  .session-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.5rem;
  }

  .session-header h2 {
    margin: 0;
    font-size: 1rem;
  }

  .ghost {
    border: 1px solid var(--border);
    background: #f8f8f8;
    border-radius: 999px;
    padding: 0.35rem 0.8rem;
    font-size: 0.8rem;
    cursor: pointer;
    transition: background 0.15s;
  }

  .ghost:hover:not(:disabled) {
    background: #efefef;
  }

  .ghost:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .muted {
    color: var(--muted);
    margin: 0;
    font-size: 0.85rem;
  }

  .session-list {
    display: grid;
    gap: 0.6rem;
  }

  .session-item {
    text-align: left;
    border: 1px solid var(--border);
    background: #f8f8f8;
    border-radius: 12px;
    padding: 0.75rem;
    cursor: pointer;
    display: grid;
    gap: 0.3rem;
    transition: border-color 0.15s, background 0.15s;
  }

  .session-item:hover {
    background: #f0f0f0;
  }

  .session-item.active {
    border-color: #111827;
    background: #eef2ff;
  }

  .session-title {
    font-weight: 700;
    font-size: 0.9rem;
  }

  .session-meta {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    font-size: 0.78rem;
    color: var(--muted);
  }

  .dot {
    font-size: 0.55rem;
  }

  .conversation {
    display: grid;
    gap: 1rem;
  }

  .session-banner {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.8rem 1rem;
    border-radius: 14px;
    border: 1px solid var(--border);
    background: #ffffff;
    font-size: 0.9rem;
  }

  .session-banner strong {
    margin-right: 0.4rem;
  }

  .thread {
    display: flex;
    flex-direction: column;
    gap: 0.8rem;
    max-height: 520px;
    overflow-y: auto;
    padding-right: 0.25rem;
    scroll-behavior: smooth;
  }

  .empty {
    color: var(--muted);
    text-align: center;
    padding: 1.5rem 0;
    font-size: 0.9rem;
  }

  .bubble {
    max-width: min(70%, 560px);
    padding: 0.9rem 1.1rem;
    border-radius: 18px;
    border: 1px solid var(--border);
    background: #f8f8f8;
    display: grid;
    gap: 0.5rem;
  }

  .bubble.user {
    margin-left: auto;
    background: #111827;
    color: #ffffff;
    border-color: #111827;
  }

  .bubble p {
    margin: 0;
    line-height: 1.6;
    font-size: 0.95rem;
  }

  .bubble.typing {
    display: flex;
    align-items: center;
    gap: 0.35rem;
    padding: 0.75rem 1.1rem;
    width: fit-content;
  }

  .dot-anim {
    display: inline-block;
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: var(--muted, #94a3b8);
    animation: blink 1.2s infinite ease-in-out;
  }

  .dot-anim:nth-child(2) { animation-delay: 0.2s; }
  .dot-anim:nth-child(3) { animation-delay: 0.4s; }

  @keyframes blink {
    0%, 80%, 100% { opacity: 0.2; transform: scale(0.85); }
    40% { opacity: 1; transform: scale(1); }
  }

  .meta {
    display: grid;
    gap: 0.3rem;
    font-size: 0.8rem;
    color: var(--muted);
  }

  .meta-row {
    display: flex;
    align-items: center;
    gap: 0.6rem;
  }

  .badge {
    background: rgba(14, 116, 144, 0.12);
    color: #0e7490;
    padding: 0.2rem 0.6rem;
    border-radius: 999px;
    font-weight: 600;
    font-size: 0.78rem;
  }

  .confidence {
    font-weight: 600;
    color: var(--muted);
  }

  .score-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
  }

  .time {
    font-size: 0.72rem;
    color: rgba(255, 255, 255, 0.6);
    justify-self: end;
  }

  .bubble.assistant .time {
    color: var(--muted);
  }

  .composer {
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 1.2rem;
    background: #ffffff;
    box-shadow: 0 18px 40px rgba(15, 23, 42, 0.08);
    display: grid;
    gap: 1rem;
  }

  textarea {
    width: 100%;
    border: none;
    resize: none;
    font: inherit;
    outline: none;
    font-size: 0.95rem;
    line-height: 1.6;
  }

  textarea:disabled {
    background: transparent;
    color: var(--muted);
    cursor: not-allowed;
  }

  .composer-actions {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    flex-wrap: wrap;
  }

  .chip-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
  }

  .chip {
    border: 1px solid var(--border);
    background: #f8f8f8;
    border-radius: 999px;
    padding: 0.35rem 0.85rem;
    font-size: 0.82rem;
    cursor: pointer;
    transition: background 0.15s;
  }

  .chip:hover:not(:disabled) {
    background: #efefef;
  }

  .chip:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .send {
    width: 44px;
    height: 44px;
    border-radius: 50%;
    border: none;
    background: var(--accent, #111827);
    color: #ffffff;
    font-size: 1.1rem;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    transition: opacity 0.15s;
  }

  .send:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .spinner {
    display: inline-block;
    width: 16px;
    height: 16px;
    border: 2px solid rgba(255, 255, 255, 0.35);
    border-top-color: #fff;
    border-radius: 50%;
    animation: spin 0.7s linear infinite;
  }

  @keyframes spin {
    to { transform: rotate(360deg); }
  }

  .cards {
    display: grid;
    gap: 0.8rem;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  }

  .card {
    padding: 1rem 1.2rem;
    border-radius: 16px;
    border: 1px solid var(--border);
    color: var(--muted);
    background: #f8f8f8;
    font-weight: 600;
    font-size: 0.9rem;
    text-align: left;
    cursor: pointer;
    transition: color 0.15s, background 0.15s;
  }

  .card:hover {
    color: var(--ink);
    background: #f1f1f1;
  }

  @media (max-width: 900px) {
    .workspace {
      grid-template-columns: 1fr;
    }
  }
</style>
