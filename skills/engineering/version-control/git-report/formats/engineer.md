# Engineer report formats

## Shared rules

- Group commits by technical topic and preserve the cause, tradeoff, mechanism, and maintenance effect supported by evidence.
- For an important topic, use the applicable parts of problem -> approach -> impact.
- Name concrete modules, mechanisms, interfaces, or rules when they explain the change.
- Compress routine cleanup and low-risk documentation into one sentence.
- Let the evidence determine item count and state low activity directly.
- Replace `<範圍標籤>` with the resolved label when a format uses it.

## precise

Use a Markdown nested bullet list with two or three levels:

- First level: technical work topic in plain language.
- Second level: the evidenced problem, approach, and impact; include only applicable labels.
- Third level: implementation detail required to explain cause or maintenance impact.

Return the list without a preface or closing paragraph.

## short

Use first-level bullets only. Write one sentence per supported topic, combining the most important technical change and impact. Use at most five bullets and fewer when activity is low.

## full

Use this structure and omit empty sections:

```markdown
### <範圍標籤>主要進展
依主題說明有證據的問題、做法與影響。

### 重要技術與流程變更
記錄值得單獨保留的架構、規則、介面或工作流演進。

### 補充項目
合併較次要但仍有維護價值的修正、文件或支援性工作。
```

## Quality gates

- Each important topic preserves enough technical cause and effect for a maintainer.
- Problem, approach, tradeoff, and impact labels appear only when their evidence exists.
- The report reads as grouped engineering progress rather than a commit-by-commit log.
- Routine work is compressed without hiding a meaningful compatibility, deployment, or maintenance consequence.
