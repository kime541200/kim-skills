# Manager report formats

## Shared rules

- Lead with business or product results, then give only the background needed to explain them.
- Translate implementation into user, release, cost, risk, compliance, or delivery impact when the evidence supports that connection.
- State the direct engineering result when business impact is not evidenced.
- Explain the first useful technical term in plain language and omit implementation detail that does not explain impact.
- Put the highest-impact result first and compress infrastructure, documentation, internal tools, and experience capture into supporting work unless they affect delivery or risk.
- Include a risk, blocker, decision, dependency, or next step only when commit evidence supports it.
- Let the evidence determine item count. For a low-signal scope, state the low activity and omit empty sections.
- Replace `<範圍標籤>` with the resolved label, such as `本週`, `上月`, a concrete date range, or a revision name.

## precise

Use this structure:

```markdown
**<範圍標籤>重點（TL;DR）**
1-3 句總結最重要的結果；只在有證據時補充下一步或風險。

**主要進展**
- 結果或業務影響作為主題標題
    - 影響：對上線、使用者、成本、風險、合規或交付的具體影響
    - 背景：理解結果所需的一句背景；不需要時省略

**風險與阻塞**
- 需要管理層注意且有證據的待決事項、卡點、決策或外部依賴；沒有時省略整段。

**其他工作**
支援性工作合併成最多 1-2 行；沒有時省略整段。
```

Use at most five main topics and fewer whenever the evidence supports fewer.

## short

Use this structure:

```markdown
**<範圍標籤>重點（TL;DR）**
1-2 句總結最重要的結果。

**亮點**
- 1-5 條有證據的結果，每條一句。

**風險與阻塞**
- 只列有證據且需要注意的項目；沒有時省略整段。
```

## full

Use this structure:

```markdown
### <範圍標籤>重點（TL;DR）
2-3 句總結結果；只在有證據時補充下一步或風險。

### 主要進展
依重要性分段。每段先講結果或業務影響，再說明必要背景與影響範圍。

### 風險與阻塞
逐項說明有證據的待決事項、卡點或外部依賴及其影響；沒有時省略。

### 其他工作
將支援性工作合併為最多一段；沒有時省略。

### 附錄：技術細節
只有主管可能需要追問且證據足夠時才加入，並與主文分離。
```

## Quality gates

- The first topic is the strongest supported management impact.
- Every translated impact preserves the technical evidence without exaggeration.
- Technical detail appears only where it clarifies a decision, consequence, or risk.
- Optional risk, next-step, supporting-work, and appendix sections appear only when supported.
