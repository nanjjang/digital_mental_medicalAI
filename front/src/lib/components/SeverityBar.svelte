<script>
  export let value = null;

  const bands = [
    { max: 24, label: "안정", color: "#4aa96c" },
    { max: 49, label: "주의", color: "#f2c94c" },
    { max: 74, label: "높음", color: "#f2994a" },
    { max: 100, label: "위험", color: "#eb5757" }
  ];

  $: hasValue = typeof value === "number" && !Number.isNaN(value);
  $: clamped = hasValue ? Math.max(0, Math.min(100, value)) : 0;
  $: band = bands.find((b) => clamped <= b.max) ?? bands[bands.length - 1];
</script>

<div class="bar-wrap" role="status" aria-label="심각도 게이지">
  <div class="label">
    <span class="tag">심각도</span>
    <strong>{hasValue ? band.label : "데이터 없음"}</strong>
  </div>
  <div class="meter" aria-hidden="true">
    <div
      class="meter-fill"
      style="width: {clamped}%; background: {hasValue ? band.color : '#cfcfcf'}"
    ></div>
  </div>
  <div class="value">{hasValue ? `${clamped}/100` : "-"}</div>
</div>

<style>
  .bar-wrap {
    display: grid;
    grid-template-columns: auto 1fr auto;
    gap: 0.8rem;
    align-items: center;
    padding: 0.75rem 1rem;
    border-radius: 999px;
    background: #ffffff;
    border: 1px solid var(--border);
    font-family: var(--sans);
  }

  .label {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }

  .tag {
    font-size: 0.75rem;
    letter-spacing: 0.08em;
    color: #777777;
  }

  .meter {
    height: 0.55rem;
    background: #ededed;
    border-radius: 999px;
    overflow: hidden;
  }

  .meter-fill {
    height: 100%;
    transition: width 0.3s ease;
  }

  .value {
    font-weight: 700;
    color: #333333;
  }

  @media (max-width: 720px) {
    .bar-wrap {
      grid-template-columns: 1fr;
      gap: 0.4rem;
      text-align: left;
    }
  }
</style>
