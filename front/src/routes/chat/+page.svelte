<script>
  import { onMount } from "svelte";

  let prompt = "";
  const chips = ["오늘 감정 기록", "5분 호흡 루틴", "수면 루틴 제안", "하루 정리 질문", "불안 완화 체크인", "집중 회복 플랜"];
  let messages = [];
  let inputRef;

  const nowTime = () => {
    const date = new Date();
    return date.toLocaleTimeString("ko-KR", { hour: "2-digit", minute: "2-digit" });
  };

  const addMessage = (role, text) => {
    const trimmed = text.trim();
    if (!trimmed) return;
    messages = [...messages, { id: crypto.randomUUID(), role, text: trimmed, time: nowTime() }];
  };

  const handleSend = () => {
    addMessage("user", prompt);
    prompt = "";
  };

  const handleChip = (chip) => {
    prompt = chip;
    inputRef?.focus();
  };

  const handleQuick = (text) => {
    prompt = text;
    inputRef?.focus();
  };

  onMount(() => {
    const params = new URLSearchParams(window.location.search);
    const value = params.get("prompt");
    if (value) {
      prompt = value;
    }
  });
</script>

<section class="chat">
  <div class="header">
    <p class="eyebrow">AI 대화 공간</p>
    <h1 class="title">지금 떠오르는 생각을 편하게 말해 보세요.</h1>
    <p class="subtitle">
      카카오톡과 GPT, Gemini의 장점을 분석해 만든 집중형 채팅 화면입니다. 핵심 질문을 빠르게 입력하고
      기록으로 남길 수 있습니다.
    </p>
  </div>

  <div class="thread">
    {#if messages.length === 0}
      <div class="empty">아직 대화가 없습니다. 아래에서 시작해 보세요.</div>
    {/if}
    {#each messages as message (message.id)}
      <div class="bubble {message.role}">
        <p>{message.text}</p>
        <span class="time">{message.time}</span>
      </div>
    {/each}
  </div>

  <div class="composer">
    <textarea
      rows="4"
      bind:this={inputRef}
      bind:value={prompt}
      placeholder="오늘 마음을 한 문장으로 적어 보세요. 예: 오늘은 불안이 커서 잠이 오지 않았어요."
    ></textarea>
    <div class="composer-actions">
      <div class="chip-row">
        {#each chips as chip}
          <button class="chip" type="button" on:click={() => handleChip(chip)}>
            {chip}
          </button>
        {/each}
      </div>
      <button class="send" type="button" aria-label="전송" on:click={handleSend}>
        ↑
      </button>
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

  .thread {
    display: grid;
    gap: 0.8rem;
  }

  .empty {
    color: var(--muted);
    text-align: center;
    padding: 1.2rem 0;
  }

  .bubble {
    max-width: min(70%, 560px);
    padding: 0.9rem 1.1rem;
    border-radius: 18px;
    border: 1px solid var(--border);
    background: #f8f8f8;
    display: grid;
    gap: 0.4rem;
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
  }

  .time {
    font-size: 0.75rem;
    color: rgba(255, 255, 255, 0.7);
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
    padding: 0.35rem 0.8rem;
    font-size: 0.85rem;
  }

  .send {
    width: 44px;
    height: 44px;
    border-radius: 50%;
    border: none;
    background: var(--accent);
    color: #ffffff;
    font-size: 1.1rem;
    cursor: pointer;
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
    text-align: left;
    cursor: pointer;
  }

  .card:hover {
    color: var(--ink);
    background: #f1f1f1;
  }
</style>
